<script lang="ts">
	import { onMount } from 'svelte';
	import { auth } from '$lib/stores/auth';
	import { goto } from '$app/navigation';
	import Sidebar from '$lib/components/layout/Sidebar.svelte';
	import { accountsApi, type Account, type AccountCreate } from '$lib/api/accounts';

	let accounts = $state<Account[]>([]);
	let loading = $state(true);
	let error = $state('');
	let showCreateModal = $state(false);

	// Form state
	let accountName = $state('');
	let accountType = $state('checking');
	let balance = $state(0);
	let currency = $state('USD');
	let creating = $state(false);

	const accountTypes = [
		{ value: 'checking', label: 'Checking Account', icon: '🏦' },
		{ value: 'savings', label: 'Savings Account', icon: '💰' },
		{ value: 'credit_card', label: 'Credit Card', icon: '💳' },
		{ value: 'investment', label: 'Investment Account', icon: '📈' }
	];

	onMount(async () => {
		if (!$auth.user) {
			goto('/login');
			return;
		}

		await loadAccounts();
	});

	async function loadAccounts() {
		try {
			loading = true;
			accounts = await accountsApi.getAll();
		} catch (err: any) {
			error = 'Failed to load accounts';
			console.error(err);
		} finally {
			loading = false;
		}
	}

	async function handleCreateAccount() {
		error = '';
		creating = true;

		try {
			const accountData: AccountCreate = {
				account_name: accountName,
				account_type: accountType,
				balance: balance,
				currency: currency
			};

			await accountsApi.create(accountData);
			await loadAccounts();

			// Reset form and close modal
			accountName = '';
			accountType = 'checking';
			balance = 0;
			currency = 'USD';
			showCreateModal = false;
		} catch (err: any) {
			error = err.response?.data?.detail || 'Failed to create account';
		} finally {
			creating = false;
		}
	}

	async function handleDeleteAccount(id: number) {
		if (!confirm('Are you sure you want to delete this account?')) return;

		try {
			await accountsApi.delete(id);
			await loadAccounts();
		} catch (err: any) {
			error = err.response?.data?.detail || 'Failed to delete account';
		}
	}

	function formatCurrency(amount: number): string {
		return new Intl.NumberFormat('en-US', {
			style: 'currency',
			currency: 'USD'
		}).format(amount);
	}

	function getAccountIcon(type: string): string {
		const found = accountTypes.find(t => t.value === type);
		return found?.icon || '💼';
	}
</script>

<div class="flex min-h-screen">
	<Sidebar />

	<main class="flex-1 p-8">
		<!-- Header -->
		<div class="flex items-center justify-between mb-8">
			<div>
				<h1 class="text-4xl font-bold gradient-text mb-2">Accounts</h1>
				<p class="text-white/70">Manage your bank accounts and credit cards</p>
			</div>
			<button onclick={() => showCreateModal = true} class="btn-primary">
				+ Add Account
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
				<p class="text-white/70 text-lg">Loading accounts...</p>
			</div>
		{:else if accounts.length === 0}
			<div class="glass-card p-12 text-center">
				<div class="text-6xl mb-4">🏦</div>
				<h2 class="text-2xl font-bold mb-4">No Accounts Yet</h2>
				<p class="text-white/70 mb-6">
					Start by adding your first account to track your finances.
				</p>
				<button onclick={() => showCreateModal = true} class="btn-primary">
					+ Add Your First Account
				</button>
			</div>
		{:else}
			<!-- Accounts Grid -->
			<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
				{#each accounts as account}
					<div class="glass-card glass-card-hover p-6">
						<div class="flex items-start justify-between mb-4">
							<div class="text-4xl">{getAccountIcon(account.account_type)}</div>
							<button
								onclick={() => handleDeleteAccount(account.id)}
								class="text-white/50 hover:text-red-400 transition-colors"
							>
								🗑️
							</button>
						</div>
						<h3 class="text-xl font-bold mb-2">{account.account_name}</h3>
						<p class="text-white/60 text-sm mb-4 capitalize">
							{account.account_type.replace('_', ' ')}
						</p>
						<p class="text-3xl font-bold gradient-text">
							{formatCurrency(account.balance)}
						</p>
					</div>
				{/each}
			</div>
		{/if}

		<!-- Create Account Modal -->
		{#if showCreateModal}
			<div class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 z-50">
				<div class="glass-card p-8 w-full max-w-md">
					<h2 class="text-2xl font-bold gradient-text mb-6">Add New Account</h2>

					<form onsubmit={handleCreateAccount} class="space-y-6">
						<!-- Account Name -->
						<div>
							<label for="accountName" class="block text-sm font-medium text-white/90 mb-2">
								Account Name
							</label>
							<input
								id="accountName"
								type="text"
								bind:value={accountName}
								required
								class="input-glass"
								placeholder="e.g., Chase Checking"
								disabled={creating}
							/>
						</div>

						<!-- Account Type -->
						<div>
							<label for="accountType" class="block text-sm font-medium text-white/90 mb-2">
								Account Type
							</label>
							<select
								id="accountType"
								bind:value={accountType}
								class="input-glass"
								disabled={creating}
							>
								{#each accountTypes as type}
									<option value={type.value}>{type.icon} {type.label}</option>
								{/each}
							</select>
						</div>

						<!-- Initial Balance -->
						<div>
							<label for="balance" class="block text-sm font-medium text-white/90 mb-2">
								Initial Balance
							</label>
							<input
								id="balance"
								type="number"
								step="0.01"
								bind:value={balance}
								required
								class="input-glass"
								placeholder="0.00"
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
								{creating ? 'Creating...' : 'Create Account'}
							</button>
							<button
								type="button"
								onclick={() => showCreateModal = false}
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
