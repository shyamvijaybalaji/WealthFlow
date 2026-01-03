<script lang="ts">
	import { onMount } from 'svelte';
	import { auth } from '$lib/stores/auth';
	import { goto } from '$app/navigation';
	import Sidebar from '$lib/components/layout/Sidebar.svelte';
	import { savingsGoalsApi, type SavingsGoalWithProgress, type SavingsGoalCreate } from '$lib/api/savings-goals';

	let goals = $state<SavingsGoalWithProgress[]>([]);
	let loading = $state(true);
	let error = $state('');
	let showCreateModal = $state(false);
	let showUpdateModal = $state(false);
	let selectedGoal = $state<SavingsGoalWithProgress | null>(null);

	// Form state
	let goalName = $state('');
	let targetAmount = $state(0);
	let currentAmount = $state(0);
	let deadline = $state('');
	let icon = $state('💰');
	let creating = $state(false);
	let updating = $state(false);

	const iconOptions = ['💰', '🏠', '🚗', '✈️', '🎓', '💍', '🏖️', '📱', '🎯', '⭐'];

	onMount(async () => {
		if (!$auth.user) {
			goto('/login');
			return;
		}

		await loadGoals();
	});

	async function loadGoals() {
		try {
			loading = true;
			goals = await savingsGoalsApi.getAll();
		} catch (err: any) {
			error = 'Failed to load savings goals';
			console.error(err);
		} finally {
			loading = false;
		}
	}

	async function handleCreateGoal() {
		error = '';
		creating = true;

		try {
			const goalData: SavingsGoalCreate = {
				goal_name: goalName,
				target_amount: targetAmount,
				current_amount: currentAmount,
				deadline: deadline || null,
				icon: icon
			};

			await savingsGoalsApi.create(goalData);
			await loadGoals();

			// Reset form and close modal
			resetForm();
			showCreateModal = false;
		} catch (err: any) {
			error = err.response?.data?.detail || 'Failed to create savings goal';
		} finally {
			creating = false;
		}
	}

	async function handleUpdateGoal() {
		if (!selectedGoal) return;

		error = '';
		updating = true;

		try {
			await savingsGoalsApi.update(selectedGoal.id, {
				current_amount: currentAmount
			});
			await loadGoals();

			showUpdateModal = false;
			selectedGoal = null;
		} catch (err: any) {
			error = err.response?.data?.detail || 'Failed to update savings goal';
		} finally {
			updating = false;
		}
	}

	async function handleDeleteGoal(id: number) {
		if (!confirm('Are you sure you want to delete this savings goal?')) return;

		try {
			await savingsGoalsApi.delete(id);
			await loadGoals();
		} catch (err: any) {
			error = err.response?.data?.detail || 'Failed to delete savings goal';
		}
	}

	function openUpdateModal(goal: SavingsGoalWithProgress) {
		selectedGoal = goal;
		currentAmount = goal.current_amount;
		showUpdateModal = true;
	}

	function resetForm() {
		goalName = '';
		targetAmount = 0;
		currentAmount = 0;
		deadline = '';
		icon = '💰';
	}

	function formatCurrency(amount: number): string {
		return new Intl.NumberFormat('en-US', {
			style: 'currency',
			currency: 'USD'
		}).format(amount);
	}

	function formatDate(dateString: string | null): string {
		if (!dateString) return 'No deadline';
		const date = new Date(dateString);
		return new Intl.DateTimeFormat('en-US', {
			month: 'short',
			day: 'numeric',
			year: 'numeric'
		}).format(date);
	}
</script>

<div class="flex min-h-screen">
	<Sidebar />

	<main class="flex-1 px-4 pt-20 pb-4 sm:p-6 md:p-8">
		<!-- Header -->
		<div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6 md:mb-8">
			<div>
				<h1 class="text-3xl md:text-4xl font-bold gradient-text mb-1 md:mb-2">Savings Goals</h1>
				<p class="text-sm md:text-base text-white/70">Track progress toward your financial goals</p>
			</div>
			<button onclick={() => showCreateModal = true} class="btn-primary whitespace-nowrap">
				+ Create Goal
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
				<p class="text-white/70 text-lg">Loading savings goals...</p>
			</div>
		{:else if goals.length === 0}
			<div class="glass-card p-12 text-center">
				<div class="text-6xl mb-4">🎯</div>
				<h2 class="text-2xl font-bold mb-4">No Savings Goals Yet</h2>
				<p class="text-white/70 mb-6">
					Start planning your financial future by setting savings goals.
				</p>
				<button onclick={() => showCreateModal = true} class="btn-primary">
					+ Create Your First Goal
				</button>
			</div>
		{:else}
			<!-- Goals Grid -->
			<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
				{#each goals as goal}
					<div class="glass-card glass-card-hover p-6">
						<!-- Header -->
						<div class="flex items-start justify-between mb-6">
							<div class="text-5xl">{goal.icon || '💰'}</div>
							<button
								onclick={() => handleDeleteGoal(goal.id)}
								class="text-white/50 hover:text-red-400 transition-colors"
							>
								🗑️
							</button>
						</div>

						<!-- Goal Name -->
						<h3 class="text-xl font-bold mb-4">{goal.goal_name}</h3>

						<!-- Circular Progress -->
						<div class="flex items-center justify-center mb-6">
							<div class="relative w-32 h-32">
								<!-- Background Circle -->
								<svg class="w-full h-full transform -rotate-90">
									<circle
										cx="64"
										cy="64"
										r="56"
										stroke="currentColor"
										stroke-width="8"
										fill="none"
										class="text-charcoal/60"
									/>
									<!-- Progress Circle -->
									<circle
										cx="64"
										cy="64"
										r="56"
										stroke="currentColor"
										stroke-width="8"
										fill="none"
										class="text-emerald transition-all duration-500"
										stroke-dasharray="351.86"
										stroke-dashoffset="{351.86 - (351.86 * Math.min(goal.progress_percentage, 100)) / 100}"
										stroke-linecap="round"
									/>
								</svg>
								<!-- Percentage Text -->
								<div class="absolute inset-0 flex items-center justify-center">
									<span class="text-2xl font-bold gradient-text">
										{goal.progress_percentage.toFixed(0)}%
									</span>
								</div>
							</div>
						</div>

						<!-- Amounts -->
						<div class="space-y-2 mb-4">
							<div class="flex justify-between text-sm">
								<span class="text-white/60">Current</span>
								<span class="font-semibold text-emerald">{formatCurrency(goal.current_amount)}</span>
							</div>
							<div class="flex justify-between text-sm">
								<span class="text-white/60">Target</span>
								<span class="font-semibold">{formatCurrency(goal.target_amount)}</span>
							</div>
							<div class="flex justify-between text-sm">
								<span class="text-white/60">Remaining</span>
								<span class="font-semibold text-cyan">{formatCurrency(goal.remaining)}</span>
							</div>
						</div>

						<!-- Deadline -->
						<div class="pt-4 border-t border-white/10 text-sm text-white/60 mb-4">
							<p>⏰ {formatDate(goal.deadline)}</p>
						</div>

						<!-- Update Button -->
						<button
							onclick={() => openUpdateModal(goal)}
							class="btn-secondary w-full"
						>
							Update Progress
						</button>
					</div>
				{/each}
			</div>
		{/if}

		<!-- Create Goal Modal -->
		{#if showCreateModal}
			<div class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 z-50">
				<div class="glass-card p-8 w-full max-w-md">
					<h2 class="text-2xl font-bold gradient-text mb-6">Create Savings Goal</h2>

					<form onsubmit={handleCreateGoal} class="space-y-6">
						<!-- Icon Selection -->
						<div>
							<label class="block text-sm font-medium text-white/90 mb-2">
								Icon
							</label>
							<div class="grid grid-cols-5 gap-2">
								{#each iconOptions as iconOption}
									<button
										type="button"
										onclick={() => icon = iconOption}
										class="text-3xl p-2 rounded-lg transition-all {icon === iconOption
											? 'bg-emerald/20 border-2 border-emerald'
											: 'bg-charcoal/40 border border-white/10 hover:bg-white/10'}"
									>
										{iconOption}
									</button>
								{/each}
							</div>
						</div>

						<!-- Goal Name -->
						<div>
							<label for="goalName" class="block text-sm font-medium text-white/90 mb-2">
								Goal Name
							</label>
							<input
								id="goalName"
								type="text"
								bind:value={goalName}
								required
								class="input-glass"
								placeholder="e.g., Emergency Fund"
								disabled={creating}
							/>
						</div>

						<!-- Target Amount -->
						<div>
							<label for="targetAmount" class="block text-sm font-medium text-white/90 mb-2">
								Target Amount
							</label>
							<input
								id="targetAmount"
								type="number"
								step="0.01"
								bind:value={targetAmount}
								required
								class="input-glass"
								placeholder="10000.00"
								disabled={creating}
							/>
						</div>

						<!-- Current Amount -->
						<div>
							<label for="currentAmount" class="block text-sm font-medium text-white/90 mb-2">
								Current Amount
							</label>
							<input
								id="currentAmount"
								type="number"
								step="0.01"
								bind:value={currentAmount}
								class="input-glass"
								placeholder="0.00"
								disabled={creating}
							/>
						</div>

						<!-- Deadline -->
						<div>
							<label for="deadline" class="block text-sm font-medium text-white/90 mb-2">
								Deadline (Optional)
							</label>
							<input
								id="deadline"
								type="date"
								bind:value={deadline}
								class="input-glass"
								disabled={creating}
							/>
						</div>

						<!-- Buttons -->
						<div class="flex flex-col sm:flex-row gap-3 sm:gap-4">
							<button
								type="submit"
								class="btn-primary flex-1"
								disabled={creating}
							>
								{creating ? 'Creating...' : 'Create Goal'}
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

		<!-- Update Progress Modal -->
		{#if showUpdateModal && selectedGoal}
			<div class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 z-50">
				<div class="glass-card p-8 w-full max-w-md">
					<h2 class="text-2xl font-bold gradient-text mb-6">Update Progress</h2>
					<p class="text-white/70 mb-6">Goal: {selectedGoal.goal_name}</p>

					<form onsubmit={handleUpdateGoal} class="space-y-6">
						<!-- Current Amount -->
						<div>
							<label for="updateAmount" class="block text-sm font-medium text-white/90 mb-2">
								Current Amount
							</label>
							<input
								id="updateAmount"
								type="number"
								step="0.01"
								bind:value={currentAmount}
								required
								class="input-glass"
								disabled={updating}
							/>
							<p class="text-xs text-white/60 mt-1">
								Previous: {formatCurrency(selectedGoal.current_amount)}
							</p>
						</div>

						<!-- Buttons -->
						<div class="flex flex-col sm:flex-row gap-3 sm:gap-4">
							<button
								type="submit"
								class="btn-primary flex-1"
								disabled={updating}
							>
								{updating ? 'Updating...' : 'Update'}
							</button>
							<button
								type="button"
								onclick={() => { showUpdateModal = false; selectedGoal = null; }}
								class="btn-secondary flex-1"
								disabled={updating}
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
