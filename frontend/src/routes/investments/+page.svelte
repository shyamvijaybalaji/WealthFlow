<script lang="ts">
	import { onMount } from 'svelte';
	import { auth } from '$lib/stores/auth';
	import { goto } from '$app/navigation';
	import Sidebar from '$lib/components/layout/Sidebar.svelte';
	import DonutChart from '$lib/components/charts/DonutChart.svelte';
	import { investmentsApi, type InvestmentWithROI, type PortfolioSummary, type InvestmentCreate } from '$lib/api/investments';

	let investments = $state<InvestmentWithROI[]>([]);
	let summary = $state<PortfolioSummary | null>(null);
	let loading = $state(true);
	let error = $state('');
	let showCreateModal = $state(false);

	// Form state
	let assetType = $state('stock');
	let symbol = $state('');
	let quantity = $state(0);
	let purchasePrice = $state(0);
	let currentPrice = $state(0);
	let purchaseDate = $state(new Date().toISOString().split('T')[0]);
	let creating = $state(false);

	const assetTypes = [
		{ value: 'stock', label: 'Stock', icon: '📈' },
		{ value: 'crypto', label: 'Cryptocurrency', icon: '₿' },
		{ value: 'bond', label: 'Bond', icon: '📜' },
		{ value: 'etf', label: 'ETF', icon: '📊' },
		{ value: 'mutual_fund', label: 'Mutual Fund', icon: '🏦' }
	];

	onMount(async () => {
		if (!$auth.user) {
			goto('/login');
			return;
		}

		await loadInvestments();
	});

	async function loadInvestments() {
		try {
			loading = true;
			const [investmentsData, summaryData] = await Promise.all([
				investmentsApi.getAll(),
				investmentsApi.getSummary()
			]);
			investments = investmentsData;
			summary = summaryData;
		} catch (err: any) {
			error = 'Failed to load investments';
			console.error(err);
		} finally {
			loading = false;
		}
	}

	async function handleCreateInvestment() {
		error = '';
		creating = true;

		try {
			const investmentData: InvestmentCreate = {
				asset_type: assetType,
				symbol: symbol.toUpperCase(),
				quantity: quantity,
				purchase_price: purchasePrice,
				current_price: currentPrice || null,
				purchase_date: new Date(purchaseDate).toISOString()
			};

			await investmentsApi.create(investmentData);
			await loadInvestments();

			// Reset form and close modal
			resetForm();
			showCreateModal = false;
		} catch (err: any) {
			error = err.response?.data?.detail || 'Failed to create investment';
		} finally {
			creating = false;
		}
	}

	async function handleDeleteInvestment(id: number) {
		if (!confirm('Are you sure you want to delete this investment?')) return;

		try {
			await investmentsApi.delete(id);
			await loadInvestments();
		} catch (err: any) {
			error = err.response?.data?.detail || 'Failed to delete investment';
		}
	}

	function resetForm() {
		assetType = 'stock';
		symbol = '';
		quantity = 0;
		purchasePrice = 0;
		currentPrice = 0;
		purchaseDate = new Date().toISOString().split('T')[0];
	}

	function formatCurrency(amount: number): string {
		return new Intl.NumberFormat('en-US', {
			style: 'currency',
			currency: 'USD'
		}).format(amount);
	}

	function getAssetIcon(type: string): string {
		const found = assetTypes.find(t => t.value === type);
		return found?.icon || '📊';
	}

	function getAssetLabel(type: string): string {
		const found = assetTypes.find(t => t.value === type);
		return found?.label || type;
	}

	let chartLabels = $derived(summary ? Object.keys(summary.investments_by_type).map(type => `${getAssetIcon(type)} ${getAssetLabel(type)}`) : []);
	let chartData = $derived(summary ? Object.values(summary.investments_by_type).map(v => v.total_value) : []);
	let chartColors = $derived(['#FF6B6B', '#4ECDC4', '#FFD93D', '#6BCB77', '#AA96DA']);
</script>

<div class="flex min-h-screen">
	<Sidebar />

	<main class="flex-1 p-8">
		<!-- Header -->
		<div class="flex items-center justify-between mb-8">
			<div>
				<h1 class="text-4xl font-bold gradient-text mb-2">Investment Portfolio</h1>
				<p class="text-white/70">Track your stocks, crypto, and other investments</p>
			</div>
			<button onclick={() => showCreateModal = true} class="btn-primary">
				+ Add Investment
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
				<p class="text-white/70 text-lg">Loading portfolio...</p>
			</div>
		{:else if !summary || investments.length === 0}
			<div class="glass-card p-12 text-center">
				<div class="text-6xl mb-4">📈</div>
				<h2 class="text-2xl font-bold mb-4">No Investments Yet</h2>
				<p class="text-white/70 mb-6">
					Start building your investment portfolio by adding your first holding.
				</p>
				<button onclick={() => showCreateModal = true} class="btn-primary">
					+ Add Your First Investment
				</button>
			</div>
		{:else}
			<!-- Portfolio Summary Cards -->
			<div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
				<!-- Total Invested -->
				<div class="glass-card glass-card-hover p-6">
					<p class="text-white/60 text-sm mb-2">Total Invested</p>
					<p class="text-3xl font-bold text-cyan">{formatCurrency(summary.total_invested)}</p>
				</div>

				<!-- Current Value -->
				<div class="glass-card glass-card-hover p-6">
					<p class="text-white/60 text-sm mb-2">Current Value</p>
					<p class="text-3xl font-bold gradient-text">{formatCurrency(summary.current_value)}</p>
				</div>

				<!-- Profit/Loss -->
				<div class="glass-card glass-card-hover p-6">
					<p class="text-white/60 text-sm mb-2">Profit/Loss</p>
					<p class="text-3xl font-bold {summary.total_profit_loss >= 0 ? 'text-emerald' : 'text-red-400'}">
						{summary.total_profit_loss >= 0 ? '+' : ''}{formatCurrency(summary.total_profit_loss)}
					</p>
				</div>

				<!-- ROI % -->
				<div class="glass-card glass-card-hover p-6">
					<p class="text-white/60 text-sm mb-2">ROI</p>
					<p class="text-3xl font-bold {summary.roi_percentage >= 0 ? 'text-emerald' : 'text-red-400'}">
						{summary.roi_percentage >= 0 ? '+' : ''}{summary.roi_percentage.toFixed(2)}%
					</p>
				</div>
			</div>

			<!-- Asset Allocation Chart -->
			{#if Object.keys(summary.investments_by_type).length > 0}
				<div class="glass-card p-6 mb-8">
					<h2 class="text-2xl font-bold mb-6">Asset Allocation</h2>
					<div class="h-80">
						<DonutChart
							labels={chartLabels}
							data={chartData}
							colors={chartColors}
						/>
					</div>
				</div>
			{/if}

			<!-- Investments Table -->
			<div class="glass-card p-6">
				<h2 class="text-2xl font-bold mb-6">Holdings</h2>

				<div class="overflow-x-auto">
					<table class="w-full">
						<thead>
							<tr class="border-b border-white/10">
								<th class="text-left py-3 px-4 text-white/70 font-medium">Asset</th>
								<th class="text-left py-3 px-4 text-white/70 font-medium">Symbol</th>
								<th class="text-right py-3 px-4 text-white/70 font-medium">Quantity</th>
								<th class="text-right py-3 px-4 text-white/70 font-medium">Purchase Price</th>
								<th class="text-right py-3 px-4 text-white/70 font-medium">Current Price</th>
								<th class="text-right py-3 px-4 text-white/70 font-medium">Total Value</th>
								<th class="text-right py-3 px-4 text-white/70 font-medium">Profit/Loss</th>
								<th class="text-right py-3 px-4 text-white/70 font-medium">ROI</th>
								<th class="text-right py-3 px-4 text-white/70 font-medium">Actions</th>
							</tr>
						</thead>
						<tbody>
							{#each investments as investment}
								<tr class="border-b border-white/5 hover:bg-white/5">
									<td class="py-4 px-4">
										<div class="flex items-center gap-2">
											<span class="text-2xl">{getAssetIcon(investment.asset_type)}</span>
											<span class="capitalize">{getAssetLabel(investment.asset_type)}</span>
										</div>
									</td>
									<td class="py-4 px-4 font-mono font-bold">{investment.symbol}</td>
									<td class="py-4 px-4 text-right">{investment.quantity}</td>
									<td class="py-4 px-4 text-right">{formatCurrency(investment.purchase_price)}</td>
									<td class="py-4 px-4 text-right">
										{investment.current_price ? formatCurrency(investment.current_price) : '-'}
									</td>
									<td class="py-4 px-4 text-right font-semibold">{formatCurrency(investment.current_value)}</td>
									<td class="py-4 px-4 text-right font-semibold {investment.profit_loss >= 0 ? 'text-emerald' : 'text-red-400'}">
										{investment.profit_loss >= 0 ? '+' : ''}{formatCurrency(investment.profit_loss)}
									</td>
									<td class="py-4 px-4 text-right font-semibold {investment.roi_percentage >= 0 ? 'text-emerald' : 'text-red-400'}">
										{investment.roi_percentage >= 0 ? '+' : ''}{investment.roi_percentage.toFixed(2)}%
									</td>
									<td class="py-4 px-4 text-right">
										<button
											onclick={() => handleDeleteInvestment(investment.id)}
											class="text-white/50 hover:text-red-400 transition-colors"
										>
											🗑️
										</button>
									</td>
								</tr>
							{/each}
						</tbody>
					</table>
				</div>
			</div>
		{/if}

		<!-- Create Investment Modal -->
		{#if showCreateModal}
			<div class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 z-50">
				<div class="glass-card p-8 w-full max-w-md max-h-[90vh] overflow-y-auto">
					<h2 class="text-2xl font-bold gradient-text mb-6">Add Investment</h2>

					<form onsubmit={handleCreateInvestment} class="space-y-6">
						<!-- Asset Type -->
						<div>
							<label for="assetType" class="block text-sm font-medium text-white/90 mb-2">
								Asset Type
							</label>
							<select
								id="assetType"
								bind:value={assetType}
								class="input-glass"
								disabled={creating}
							>
								{#each assetTypes as type}
									<option value={type.value}>{type.icon} {type.label}</option>
								{/each}
							</select>
						</div>

						<!-- Symbol -->
						<div>
							<label for="symbol" class="block text-sm font-medium text-white/90 mb-2">
								Symbol / Ticker
							</label>
							<input
								id="symbol"
								type="text"
								bind:value={symbol}
								required
								class="input-glass uppercase"
								placeholder="e.g., AAPL, BTC"
								disabled={creating}
							/>
						</div>

						<!-- Quantity -->
						<div>
							<label for="quantity" class="block text-sm font-medium text-white/90 mb-2">
								Quantity
							</label>
							<input
								id="quantity"
								type="number"
								step="0.00000001"
								bind:value={quantity}
								required
								class="input-glass"
								placeholder="10"
								disabled={creating}
							/>
						</div>

						<!-- Purchase Price -->
						<div>
							<label for="purchasePrice" class="block text-sm font-medium text-white/90 mb-2">
								Purchase Price (per unit)
							</label>
							<input
								id="purchasePrice"
								type="number"
								step="0.01"
								bind:value={purchasePrice}
								required
								class="input-glass"
								placeholder="150.00"
								disabled={creating}
							/>
						</div>

						<!-- Current Price -->
						<div>
							<label for="currentPrice" class="block text-sm font-medium text-white/90 mb-2">
								Current Price (Optional)
							</label>
							<input
								id="currentPrice"
								type="number"
								step="0.01"
								bind:value={currentPrice}
								class="input-glass"
								placeholder="185.50"
								disabled={creating}
							/>
							<p class="text-xs text-white/60 mt-1">Leave empty to use purchase price</p>
						</div>

						<!-- Purchase Date -->
						<div>
							<label for="purchaseDate" class="block text-sm font-medium text-white/90 mb-2">
								Purchase Date
							</label>
							<input
								id="purchaseDate"
								type="date"
								bind:value={purchaseDate}
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
								{creating ? 'Adding...' : 'Add Investment'}
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
