<script lang="ts">
	import { onMount } from 'svelte';
	import { auth } from '$lib/stores/auth';
	import { goto } from '$app/navigation';
	import Sidebar from '$lib/components/layout/Sidebar.svelte';
	import { transactionsApi, type Transaction, type TransactionCreate } from '$lib/api/transactions';
	import { accountsApi, type Account } from '$lib/api/accounts';
	import { categoriesApi, type Category } from '$lib/api/categories';

	let transactions = $state<Transaction[]>([]);
	let accounts = $state<Account[]>([]);
	let categories = $state<Category[]>([]);
	let loading = $state(true);
	let error = $state('');
	let showCreateModal = $state(false);

	// Form state
	let accountId = $state(0);
	let categoryId = $state<number | null>(null);
	let amount = $state(0);
	let description = $state('');
	let merchant = $state('');
	let transactionType = $state('expense');
	let transactionDate = $state(new Date().toISOString().split('T')[0]);
	let creating = $state(false);

	onMount(async () => {
		if (!$auth.user) {
			goto('/login');
			return;
		}

		await Promise.all([loadTransactions(), loadAccounts(), loadCategories()]);
	});

	async function loadTransactions() {
		try {
			loading = true;
			transactions = await transactionsApi.getAll({ limit: 100 });
		} catch (err: any) {
			error = 'Failed to load transactions';
			console.error(err);
		} finally {
			loading = false;
		}
	}

	async function loadAccounts() {
		try {
			accounts = await accountsApi.getAll();
			if (accounts.length > 0) {
				accountId = accounts[0].id;
			}
		} catch (err: any) {
			console.error('Failed to load accounts:', err);
		}
	}

	async function loadCategories() {
		try {
			categories = await categoriesApi.getAll();
		} catch (err: any) {
			console.error('Failed to load categories:', err);
		}
	}

	async function handleCreateTransaction() {
		error = '';
		creating = true;

		try {
			const transactionData: TransactionCreate = {
				account_id: accountId,
				category_id: categoryId,
				amount: amount,
				description: description,
				merchant: merchant || null,
				transaction_type: transactionType,
				transaction_date: new Date(transactionDate).toISOString()
			};

			await transactionsApi.create(transactionData);
			await loadTransactions();

			// Reset form and close modal
			resetForm();
			showCreateModal = false;
		} catch (err: any) {
			error = err.response?.data?.detail || 'Failed to create transaction';
		} finally {
			creating = false;
		}
	}

	async function handleDeleteTransaction(id: number) {
		if (!confirm('Are you sure you want to delete this transaction?')) return;

		try {
			await transactionsApi.delete(id);
			await loadTransactions();
		} catch (err: any) {
			error = err.response?.data?.detail || 'Failed to delete transaction';
		}
	}

	function resetForm() {
		if (accounts.length > 0) {
			accountId = accounts[0].id;
		}
		categoryId = null;
		amount = 0;
		description = '';
		merchant = '';
		transactionType = 'expense';
		transactionDate = new Date().toISOString().split('T')[0];
	}

	function formatCurrency(amount: number): string {
		return new Intl.NumberFormat('en-US', {
			style: 'currency',
			currency: 'USD'
		}).format(amount);
	}

	function formatDate(dateString: string): string {
		const date = new Date(dateString);
		return new Intl.DateTimeFormat('en-US', {
			month: 'short',
			day: 'numeric',
			year: 'numeric'
		}).format(date);
	}

	function getCategoryName(id: number | null): string {
		if (!id) return 'Uncategorized';
		const cat = categories.find(c => c.id === id);
		return cat ? `${cat.icon || ''} ${cat.name}` : 'Uncategorized';
	}

	function getAccountName(id: number): string {
		const acc = accounts.find(a => a.id === id);
		return acc?.account_name || 'Unknown';
	}

	let filteredCategories = $derived(categories.filter(c => c.category_type === transactionType));
</script>

<div class="flex min-h-screen">
	<Sidebar />

	<main class="flex-1 p-8">
		<!-- Header -->
		<div class="flex items-center justify-between mb-8">
			<div>
				<h1 class="text-4xl font-bold gradient-text mb-2">Transactions</h1>
				<p class="text-white/70">Track your income and expenses</p>
			</div>
			{#if accounts.length > 0}
				<button onclick={() => showCreateModal = true} class="btn-primary">
					+ Add Transaction
				</button>
			{/if}
		</div>

		<!-- Error Message -->
		{#if error}
			<div class="mb-6 p-4 bg-red-500/20 border border-red-500/50 rounded-lg">
				<p class="text-red-300">{error}</p>
			</div>
		{/if}

		{#if loading}
			<div class="flex items-center justify-center h-64">
				<p class="text-white/70 text-lg">Loading transactions...</p>
			</div>
		{:else if accounts.length === 0}
			<div class="glass-card p-12 text-center">
				<div class="text-6xl mb-4">🏦</div>
				<h2 class="text-2xl font-bold mb-4">No Accounts Yet</h2>
				<p class="text-white/70 mb-6">
					You need to create an account before adding transactions.
				</p>
				<a href="/accounts" class="btn-primary">
					+ Create Your First Account
				</a>
			</div>
		{:else if transactions.length === 0}
			<div class="glass-card p-12 text-center">
				<div class="text-6xl mb-4">💸</div>
				<h2 class="text-2xl font-bold mb-4">No Transactions Yet</h2>
				<p class="text-white/70 mb-6">
					Start tracking your finances by adding your first transaction.
				</p>
				<button onclick={() => showCreateModal = true} class="btn-primary">
					+ Add Your First Transaction
				</button>
			</div>
		{:else}
			<!-- Transactions List -->
			<div class="glass-card p-6">
				<div class="space-y-3">
					{#each transactions as transaction}
						<div class="glass-card p-4 flex items-center justify-between hover:bg-charcoal/60 transition-all">
							<div class="flex items-center gap-4 flex-1">
								<div class="text-2xl">
									{transaction.transaction_type === 'income' ? '💵' : '💸'}
								</div>
								<div class="flex-1">
									<p class="font-medium text-white">{transaction.description}</p>
									<p class="text-sm text-white/60">
										{getCategoryName(transaction.category_id)} • {getAccountName(transaction.account_id)}
									</p>
									<p class="text-xs text-white/50">
										{formatDate(transaction.transaction_date)}
										{#if transaction.merchant}
											• {transaction.merchant}
										{/if}
									</p>
								</div>
							</div>
							<div class="flex items-center gap-4">
								<div class="text-right">
									<p class="font-bold {transaction.transaction_type === 'income' ? 'text-emerald' : 'text-red-400'}">
										{transaction.transaction_type === 'income' ? '+' : '-'}{formatCurrency(Math.abs(transaction.amount))}
									</p>
								</div>
								<button
									onclick={() => handleDeleteTransaction(transaction.id)}
									class="text-white/50 hover:text-red-400 transition-colors"
								>
									🗑️
								</button>
							</div>
						</div>
					{/each}
				</div>
			</div>
		{/if}

		<!-- Create Transaction Modal -->
		{#if showCreateModal}
			<div class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 z-50">
				<div class="glass-card p-8 w-full max-w-md max-h-[90vh] overflow-y-auto">
					<h2 class="text-2xl font-bold gradient-text mb-6">Add Transaction</h2>

					<form onsubmit={handleCreateTransaction} class="space-y-6">
						<!-- Transaction Type -->
						<div>
							<label class="block text-sm font-medium text-white/90 mb-2">
								Type
							</label>
							<div class="flex gap-4">
								<button
									type="button"
									onclick={() => transactionType = 'expense'}
									class="flex-1 py-3 rounded-lg transition-all {transactionType === 'expense'
										? 'bg-red-500/20 border-2 border-red-500 text-red-300'
										: 'bg-charcoal/40 border border-white/10 text-white/70'}"
								>
									💸 Expense
								</button>
								<button
									type="button"
									onclick={() => transactionType = 'income'}
									class="flex-1 py-3 rounded-lg transition-all {transactionType === 'income'
										? 'bg-emerald/20 border-2 border-emerald text-emerald'
										: 'bg-charcoal/40 border border-white/10 text-white/70'}"
								>
									💵 Income
								</button>
							</div>
						</div>

						<!-- Account -->
						<div>
							<label for="account" class="block text-sm font-medium text-white/90 mb-2">
								Account
							</label>
							<select
								id="account"
								bind:value={accountId}
								class="input-glass"
								disabled={creating}
							>
								{#each accounts as account}
									<option value={account.id}>{account.account_name}</option>
								{/each}
							</select>
						</div>

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
								<option value={null}>Uncategorized</option>
								{#each filteredCategories as category}
									<option value={category.id}>
										{category.icon || ''} {category.name}
									</option>
								{/each}
							</select>
						</div>

						<!-- Amount -->
						<div>
							<label for="amount" class="block text-sm font-medium text-white/90 mb-2">
								Amount
							</label>
							<input
								id="amount"
								type="number"
								step="0.01"
								bind:value={amount}
								required
								class="input-glass"
								placeholder="0.00"
								disabled={creating}
							/>
						</div>

						<!-- Description -->
						<div>
							<label for="description" class="block text-sm font-medium text-white/90 mb-2">
								Description
							</label>
							<input
								id="description"
								type="text"
								bind:value={description}
								required
								class="input-glass"
								placeholder="e.g., Grocery shopping"
								disabled={creating}
							/>
						</div>

						<!-- Merchant -->
						<div>
							<label for="merchant" class="block text-sm font-medium text-white/90 mb-2">
								Merchant (Optional)
							</label>
							<input
								id="merchant"
								type="text"
								bind:value={merchant}
								class="input-glass"
								placeholder="e.g., Walmart"
								disabled={creating}
							/>
						</div>

						<!-- Date -->
						<div>
							<label for="date" class="block text-sm font-medium text-white/90 mb-2">
								Date
							</label>
							<input
								id="date"
								type="date"
								bind:value={transactionDate}
								required
								class="input-glass"
								disabled={creating}
							/>
						</div>

						<!-- Buttons -->
						<div class="flex gap-4">
							<button
								type="submit"
								class="btn-primary flex-1"
								disabled={creating}
							>
								{creating ? 'Adding...' : 'Add Transaction'}
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
