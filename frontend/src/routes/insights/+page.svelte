<script lang="ts">
	import { onMount } from 'svelte';
	import { auth } from '$lib/stores/auth';
	import { goto } from '$app/navigation';
	import Sidebar from '$lib/components/layout/Sidebar.svelte';
	import { insightsApi, type Insight } from '$lib/api/insights';

	let insights = $state<Insight[]>([]);
	let loading = $state(true);
	let error = $state('');

	onMount(async () => {
		if (!$auth.user) {
			goto('/login');
			return;
		}

		await loadInsights();
	});

	async function loadInsights() {
		try {
			loading = true;
			insights = await insightsApi.getAll();
		} catch (err: any) {
			error = 'Failed to load insights';
			console.error(err);
		} finally {
			loading = false;
		}
	}

	function getCardStyle(type: string): string {
		switch (type) {
			case 'success':
				return 'border-emerald/50 bg-emerald/10';
			case 'warning':
				return 'border-yellow-500/50 bg-yellow-500/10';
			case 'info':
				return 'border-cyan/50 bg-cyan/10';
			case 'tip':
				return 'border-purple-500/50 bg-purple-500/10';
			default:
				return 'border-white/10 bg-charcoal/40';
		}
	}

	function getIconBgStyle(type: string): string {
		switch (type) {
			case 'success':
				return 'bg-emerald/20 text-emerald';
			case 'warning':
				return 'bg-yellow-500/20 text-yellow-500';
			case 'info':
				return 'bg-cyan/20 text-cyan';
			case 'tip':
				return 'bg-purple-500/20 text-purple-500';
			default:
				return 'bg-white/10 text-white';
		}
	}
</script>

<div class="flex min-h-screen">
	<Sidebar />

	<main class="flex-1 px-4 pt-20 pb-4 sm:p-6 md:p-8">
		<!-- Header -->
		<div class="mb-6 md:mb-8">
			<h1 class="text-3xl md:text-4xl font-bold gradient-text mb-1 md:mb-2">AI Financial Insights</h1>
			<p class="text-sm md:text-base text-white/70">Personalized recommendations based on your spending patterns</p>
		</div>

		<!-- Error Message -->
		{#if error}
			<div class="mb-6 p-4 bg-red-500/20 border border-red-500/50 rounded-lg">
				<p class="text-red-300">{error}</p>
			</div>
		{/if}

		{#if loading}
			<div class="flex items-center justify-center h-64">
				<p class="text-white/70 text-lg">Analyzing your financial data...</p>
			</div>
		{:else if insights.length === 0}
			<div class="glass-card p-12 text-center">
				<div class="text-6xl mb-4">🤖</div>
				<h2 class="text-2xl font-bold mb-4">No Insights Available Yet</h2>
				<p class="text-white/70 mb-6">
					Add some transactions, budgets, and financial data to receive personalized insights.
				</p>
			</div>
		{:else}
			<!-- Insights Grid -->
			<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
				{#each insights as insight}
					<div class="glass-card p-6 border {getCardStyle(insight.type)} transition-all duration-300 hover:scale-105">
						<div class="flex items-start gap-4">
							<!-- Icon -->
							<div class="flex-shrink-0 w-12 h-12 rounded-full {getIconBgStyle(insight.type)} flex items-center justify-center text-2xl">
								{insight.icon}
							</div>

							<!-- Content -->
							<div class="flex-1">
								<h3 class="text-xl font-bold mb-2">{insight.title}</h3>
								<p class="text-white/80 leading-relaxed">{insight.message}</p>
							</div>
						</div>
					</div>
				{/each}
			</div>

			<!-- Refresh Button -->
			<div class="mt-8 text-center">
				<button onclick={loadInsights} class="btn-secondary" disabled={loading}>
					🔄 Refresh Insights
				</button>
			</div>
		{/if}

		<!-- Info Section -->
		<div class="mt-12 glass-card p-6 border border-cyan/30">
			<div class="flex items-start gap-4">
				<div class="text-3xl">💡</div>
				<div>
					<h3 class="text-lg font-bold mb-2">How AI Insights Work</h3>
					<p class="text-white/70 text-sm leading-relaxed">
						Our AI analyzes your spending patterns, income, budgets, and savings goals to provide
						personalized financial recommendations. Insights are updated based on your last 30 days
						of financial activity. The more data you provide, the better the recommendations become.
					</p>
				</div>
			</div>
		</div>
	</main>
</div>
