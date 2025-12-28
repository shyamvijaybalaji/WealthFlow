<script lang="ts">
	import { onMount } from 'svelte';
	import { auth } from '$lib/stores/auth';
	import { goto } from '$app/navigation';
	import Sidebar from '$lib/components/layout/Sidebar.svelte';
	import { budgetsApi, type BudgetWithSpending, type BudgetCreate } from '$lib/api/budgets';
	import { categoriesApi, type Category } from '$lib/api/categories';

	let budgets = $state<BudgetWithSpending[]>([]);
	let categories = $state<Category[]>([]);
	let loading = $state(true);
	let error = $state('');
	let showCreateModal = $state(false);

	// Form state
	let categoryId = $state(0);
	let amount = $state(0);
	let period = $state('monthly');
	let alertThreshold = $state(0.80);
	let creating = $state(false);

	onMount(async () => {
		if (!$auth.user) {
			goto('/login');
			return;
		}

		await Promise.all([loadBudgets(), loadCategories()]);
	});

	async function loadBudgets() {
		try {
			loading = true;
			budgets = await budgetsApi.getAll();
		} catch (err: any) {
			error = 'Failed to load budgets';
			console.error(err);
		} finally {
			loading = false;
		}
	}

	async function loadCategories() {
		try {
			categories = await categoriesApi.getAll();
			const expenseCategories = categories.filter(c => c.category_type === 'expense');
			if (expenseCategories.length > 0) {
				categoryId = expenseCategories[0].id;
			}
		} catch (err: any) {
			console.error('Failed to load categories:', err);
		}
	}

	async function handleCreateBudget() {
		error = '';
		creating = true;

		try {
			// Automatically set start date to first day of current month
			const startDate = new Date();
			startDate.setDate(1);
			startDate.setHours(0, 0, 0, 0);

			const budgetData: BudgetCreate = {
				category_id: categoryId,
				amount: amount,
				period: period,
				alert_threshold: alertThreshold,
				start_date: startDate.toISOString()
			};

			await budgetsApi.create(budgetData);
			await loadBudgets();

			// Reset form and close modal
			resetForm();
			showCreateModal = false;
		} catch (err: any) {
			error = err.response?.data?.detail || 'Failed to create budget';
		} finally {
			creating = false;
		}
	}

	async function handleDeleteBudget(id: number) {
		if (!confirm('Are you sure you want to delete this budget?')) return;

		try {
			await budgetsApi.delete(id);
			await loadBudgets();
		} catch (err: any) {
			error = err.response?.data?.detail || 'Failed to delete budget';
		}
	}

	function resetForm() {
		const expenseCategories = categories.filter(c => c.category_type === 'expense');
		if (expenseCategories.length > 0) {
			categoryId = expenseCategories[0].id;
		}
		amount = 0;
		period = 'monthly';
		alertThreshold = 0.80;
	}

	function formatCurrency(amount: number): string {
		return new Intl.NumberFormat('en-US', {
			style: 'currency',
			currency: 'USD'
		}).format(amount);
	}

	function getCategoryName(id: number): string {
		const cat = categories.find(c => c.id === id);
		return cat ? `${cat.icon || ''} ${cat.name}` : 'Unknown';
	}

	function getStatusColor(status: string): string {
		switch (status) {
			case 'ok':
				return 'bg-emerald';
			case 'warning':
				return 'bg-yellow-500';
			case 'exceeded':
				return 'bg-red-500';
			default:
				return 'bg-gray-500';
		}
	}

	function getStatusText(status: string): string {
		switch (status) {
			case 'ok':
				return 'On Track';
			case 'warning':
				return 'Warning';
			case 'exceeded':
				return 'Over Budget';
			default:
				return 'Unknown';
		}
	}

	let expenseCategories = $derived(categories.filter(c => c.category_type === 'expense'));
</script>

<div class="flex min-h-screen">
	<Sidebar />

	<main class="flex-1 p-8">
		<!-- Header -->
		<div class="flex items-center justify-between mb-8">
			<div>
				<h1 class="text-4xl font-bold gradient-text mb-2">Budgets</h1>
				<p class="text-white/70">Track and manage your spending limits</p>
			</div>
			<button onclick={() => showCreateModal = true} class="btn-primary">
				+ Create Budget
			</button>
		</div>

		<!-- Error Message -->
		{#if error}
			<div class="mb-6 p-4 bg-red-500/20 border border-red-500/50 rounded-lg">
				<p class="text-red-300">{error}</p>
			</div>
		{/if}

		{#if loading}
			<div class="flex items-center justify-center h-64">
				<p class="text-white/70 text-lg">Loading budgets...</p>
			</div>
		{:else if budgets.length === 0}
			<div class="glass-card p-12 text-center">
				<div class="text-6xl mb-4">🎯</div>
				<h2 class="text-2xl font-bold mb-4">No Budgets Yet</h2>
				<p class="text-white/70 mb-6">
					Start controlling your spending by setting budget limits for different categories.
				</p>
				<button onclick={() => showCreateModal = true} class="btn-primary">
					+ Create Your First Budget
				</button>
			</div>
		{:else}
			<!-- Budgets Grid -->
			<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
				{#each budgets as budget}
					<div class="glass-card p-6">
						<!-- Header -->
						<div class="flex items-start justify-between mb-4">
							<div>
								<h3 class="text-xl font-bold">{getCategoryName(budget.category_id)}</h3>
								<p class="text-white/60 text-sm capitalize">{budget.period}</p>
							</div>
							<div class="flex items-center gap-2">
								<span class="px-3 py-1 rounded-full text-xs font-semibold {getStatusColor(budget.status)} text-white">
									{getStatusText(budget.status)}
								</span>
								<button
									onclick={() => handleDeleteBudget(budget.id)}
									class="text-white/50 hover:text-red-400 transition-colors"
								>
									🗑️
								</button>
							</div>
						</div>

						<!-- Budget vs Spent -->
						<div class="mb-4">
							<div class="flex justify-between text-sm mb-2">
								<span class="text-white/70">Spent</span>
								<span class="font-semibold">{formatCurrency(budget.spent)} / {formatCurrency(budget.amount)}</span>
							</div>

							<!-- Progress Bar -->
							<div class="w-full bg-charcoal/60 rounded-full h-3 overflow-hidden">
								<div
									class="h-full transition-all duration-300 {getStatusColor(budget.status)}"
									style="width: {Math.min(budget.percentage, 100)}%"
								></div>
							</div>

							<div class="flex justify-between text-xs mt-2">
								<span class="text-white/50">{budget.percentage.toFixed(1)}% used</span>
								<span class="text-white/50">
									{budget.remaining >= 0 ? `${formatCurrency(budget.remaining)} left` : `${formatCurrency(Math.abs(budget.remaining))} over`}
								</span>
							</div>
						</div>

						<!-- Details -->
						<div class="pt-4 border-t border-white/10 text-sm text-white/60">
							<p>Alert at {(budget.alert_threshold * 100).toFixed(0)}% • Started {new Date(budget.start_date).toLocaleDateString()}</p>
						</div>
					</div>
				{/each}
			</div>
		{/if}

		<!-- Create Budget Modal -->
		{#if showCreateModal}
			<div class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 z-50">
				<div class="glass-card p-8 w-full max-w-md">
					<h2 class="text-2xl font-bold gradient-text mb-6">Create Budget</h2>

					<form onsubmit={handleCreateBudget} class="space-y-6">
						<!-- Category -->
						<div>
							<label for="category" class="block text-sm font-medium text-white/90 mb-2">
								Category
							</label>
							<select
								id="category"
								bind:value={categoryId}
								class="input-glass"
								disabled={creating}
							>
								{#each expenseCategories as category}
									<option value={category.id}>
										{category.icon || ''} {category.name}
									</option>
								{/each}
							</select>
						</div>

						<!-- Budget Amount -->
						<div>
							<label for="amount" class="block text-sm font-medium text-white/90 mb-2">
								Budget Amount
							</label>
							<input
								id="amount"
								type="number"
								step="0.01"
								bind:value={amount}
								required
								class="input-glass"
								placeholder="500.00"
								disabled={creating}
							/>
						</div>

						<!-- Period -->
						<div>
							<label for="period" class="block text-sm font-medium text-white/90 mb-2">
								Period
							</label>
							<select
								id="period"
								bind:value={period}
								class="input-glass"
								disabled={creating}
							>
								<option value="monthly">Monthly</option>
								<option value="yearly">Yearly</option>
							</select>
						</div>

						<!-- Alert Threshold -->
						<div>
							<label for="threshold" class="block text-sm font-medium text-white/90 mb-2">
								Alert Threshold ({(alertThreshold * 100).toFixed(0)}%)
							</label>
							<input
								id="threshold"
								type="range"
								min="0.5"
								max="1.0"
								step="0.05"
								bind:value={alertThreshold}
								class="w-full"
								disabled={creating}
							/>
							<p class="text-xs text-white/60 mt-1">Get warned when spending reaches this percentage</p>
						</div>

						<!-- Buttons -->
						<div class="flex gap-4">
							<button
								type="submit"
								class="btn-primary flex-1"
								disabled={creating}
							>
								{creating ? 'Creating...' : 'Create Budget'}
							</button>
							<button
								type="button"
								onclick={() => { showCreateModal = false; resetForm(); }}
								class="btn-secondary flex-1"
								disabled={creating}
							>
								Cancel
							</button>
						</div>
					</form>
				</div>
			</div>
		{/if}
	</main>
</div>
