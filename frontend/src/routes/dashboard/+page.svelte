<script lang="ts">
	import { onMount } from 'svelte';
	import { auth } from '$lib/stores/auth';
	import { goto } from '$app/navigation';
	import Sidebar from '$lib/components/layout/Sidebar.svelte';
	import DonutChart from '$lib/components/charts/DonutChart.svelte';
	import { dashboardApi, type DashboardSummary } from '$lib/api/dashboard';

	let summary = $state<DashboardSummary | null>(null);
	let loading = $state(true);
	let error = $state('');

	onMount(async () => {
		// Redirect if not logged in
		if (!$auth.user) {
			goto('/login');
			return;
		}

		// Fetch dashboard summary
		try {
			summary = await dashboardApi.getSummary();
		} catch (err: any) {
			error = 'Failed to load dashboard data';
			console.error(err);
		} finally {
			loading = false;
		}
	});

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

	let chartLabels = $derived(summary?.expense_by_category.map(c => `${c.category_icon} ${c.category_name}`) || []);
	let chartData = $derived(summary?.expense_by_category.map(c => Number(c.total)) || []);
	let chartColors = $derived(summary?.expense_by_category.map(c => c.category_color) || []);
	let totalExpenses = $derived(chartData.reduce((sum, val) => sum + val, 0));
</script>

<div class="flex min-h-screen">
	<!-- Sidebar -->
	<Sidebar />

	<!-- Main Content -->
	<main class="flex-1 px-4 pt-20 pb-4 sm:p-6 md:p-8">
		<!-- Header -->
		<div class="mb-6 md:mb-8">
			<h1 class="text-3xl md:text-4xl font-bold gradient-text mb-1 md:mb-2">Dashboard</h1>
			<p class="text-sm md:text-base text-white/70">Welcome back, {$auth.user?.full_name || $auth.user?.email}!</p>
		</div>

		{#if loading}
			<div class="flex items-center justify-center h-64">
				<p class="text-white/70 text-lg">Loading dashboard...</p>
			</div>
		{:else if error}
			<div class="glass-card p-6 bg-red-500/10 border-red-500/50">
				<p class="text-red-300">{error}</p>
			</div>
		{:else if summary}
			<!-- Stats Cards Row 1 -->
			<div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
				<!-- Total Balance Card -->
				<div class="glass-card glass-card-hover p-6">
					<div class="flex items-center gap-4">
						<div class="text-4xl flex-shrink-0">💰</div>
						<div class="flex-1 min-w-0">
							<p class="text-white/60 text-sm">Total Balance</p>
							<p class="text-2xl sm:text-3xl font-bold gradient-text truncate">
								{formatCurrency(Number(summary.total_balance))}
							</p>
						</div>
					</div>
				</div>

				<!-- Total Accounts Card -->
				<div class="glass-card glass-card-hover p-6">
					<div class="flex items-center gap-4">
						<div class="text-4xl">🏦</div>
						<div class="flex-1">
							<p class="text-white/60 text-sm">Accounts</p>
							<p class="text-3xl font-bold text-cyan">
								{summary.total_accounts}
							</p>
						</div>
					</div>
				</div>

				<!-- Total Transactions Card -->
				<div class="glass-card glass-card-hover p-6">
					<div class="flex items-center gap-4">
						<div class="text-4xl">📊</div>
						<div class="flex-1">
							<p class="text-white/60 text-sm">Transactions</p>
							<p class="text-3xl font-bold text-emerald">
								{summary.total_transactions}
							</p>
						</div>
					</div>
				</div>
			</div>

			<!-- Budget Summary Card -->
			{#if summary.total_budget > 0}
				<div class="glass-card p-6 mb-8 border border-cyan/30">
					<div class="flex items-center justify-between mb-4">
						<div class="flex items-center gap-3">
							<div class="text-3xl">🎯</div>
							<div>
								<h3 class="text-xl font-bold">Budget Overview</h3>
								<p class="text-white/60 text-sm">Total across all budgets</p>
							</div>
						</div>
					</div>

					<div class="grid grid-cols-1 md:grid-cols-3 gap-6">
						<!-- Total Budget -->
						<div class="text-center p-4 rounded-lg bg-charcoal/40">
							<p class="text-white/60 text-sm mb-1">Total Budget</p>
							<p class="text-2xl font-bold text-cyan">{formatCurrency(Number(summary.total_budget))}</p>
						</div>

						<!-- Total Spent -->
						<div class="text-center p-4 rounded-lg bg-charcoal/40">
							<p class="text-white/60 text-sm mb-1">Total Spent</p>
							<p class="text-2xl font-bold text-yellow-500">{formatCurrency(Number(summary.total_spent))}</p>
						</div>

						<!-- Budget Remaining -->
						<div class="text-center p-4 rounded-lg bg-charcoal/40">
							<p class="text-white/60 text-sm mb-1">Remaining</p>
							<p class="text-2xl font-bold {Number(summary.budget_remaining) >= 0 ? 'text-emerald' : 'text-red-400'}">
								{formatCurrency(Number(summary.budget_remaining))}
							</p>
						</div>
					</div>

					<!-- Progress Bar -->
					<div class="mt-6">
						<div class="flex justify-between text-sm mb-2">
							<span class="text-white/70">Budget Usage</span>
							<span class="font-semibold">
								{((Number(summary.total_spent) / Number(summary.total_budget)) * 100).toFixed(1)}% used
							</span>
						</div>
						<div class="w-full bg-charcoal/60 rounded-full h-3 overflow-hidden">
							<div
								class="h-full transition-all duration-300 {
									(Number(summary.total_spent) / Number(summary.total_budget)) >= 1.0 ? 'bg-red-500' :
									(Number(summary.total_spent) / Number(summary.total_budget)) >= 0.8 ? 'bg-yellow-500' :
									'bg-emerald'
								}"
								style="width: {Math.min((Number(summary.total_spent) / Number(summary.total_budget)) * 100, 100)}%"
							></div>
						</div>
					</div>
				</div>
			{/if}

			<!-- Expense Breakdown Chart -->
			{#if summary.expense_by_category.length > 0}
				<div class="glass-card p-6 mb-8">
					<div class="flex items-center justify-between mb-6">
						<div>
							<h2 class="text-2xl font-bold">Expense Breakdown</h2>
							<p class="text-white/60 text-sm">Total expenses: {formatCurrency(totalExpenses)}</p>
						</div>
					</div>

					<div class="h-80">
						<DonutChart
							labels={chartLabels}
							data={chartData}
							colors={chartColors}
						/>
					</div>

					<!-- Category List -->
					<div class="mt-6 grid grid-cols-1 md:grid-cols-2 gap-3">
						{#each summary.expense_by_category as category, index}
							<div class="flex items-center justify-between p-3 rounded-lg bg-charcoal/40">
								<div class="flex items-center gap-3">
									<div class="w-4 h-4 rounded-full" style="background-color: {category.category_color}"></div>
									<span class="text-sm">{category.category_icon} {category.category_name}</span>
								</div>
								<div class="text-right">
									<p class="font-semibold text-sm">{formatCurrency(Number(category.total))}</p>
									<p class="text-xs text-white/60">{((Number(category.total) / totalExpenses) * 100).toFixed(1)}%</p>
								</div>
							</div>
						{/each}
					</div>
				</div>
			{/if}

			<!-- Recent Transactions -->
			<div class="glass-card p-6">
				<h2 class="text-2xl font-bold mb-6">Recent Transactions</h2>

				{#if summary.recent_transactions.length === 0}
					<div class="text-center py-12">
						<p class="text-white/60 mb-4">No transactions yet</p>
						<a href="/transactions" class="btn-primary">
							Add Your First Transaction
						</a>
					</div>
				{:else}
					<div class="space-y-3">
						{#each summary.recent_transactions as transaction}
							<div class="glass-card p-4 flex items-center justify-between hover:bg-charcoal/60 transition-all">
								<div class="flex items-center gap-4">
									<div class="text-2xl">
										{transaction.transaction_type === 'income' ? '💵' : '💸'}
									</div>
									<div>
										<p class="font-medium text-white">{transaction.description}</p>
										<p class="text-sm text-white/60">
											{transaction.merchant || 'N/A'} • {formatDate(transaction.transaction_date)}
										</p>
									</div>
								</div>
								<div class="text-right">
									<p class="font-bold {transaction.transaction_type === 'income' ? 'text-emerald' : 'text-red-400'}">
										{transaction.transaction_type === 'income' ? '+' : '-'}{formatCurrency(Math.abs(transaction.amount))}
									</p>
									<p class="text-xs text-white/60 capitalize">{transaction.transaction_type}</p>
								</div>
							</div>
						{/each}
					</div>

					<div class="mt-6 text-center">
						<a href="/transactions" class="btn-secondary">
							View All Transactions
						</a>
					</div>
				{/if}
			</div>
		{/if}
	</main>
</div>
