<script lang="ts">
	import { auth } from '$lib/stores/auth';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';

	let mobileMenuOpen = $state(false);

	function handleLogout() {
		auth.logout();
		goto('/login');
	}

	// Navigation items
	const navItems = [
		{ path: '/dashboard', label: 'Dashboard', icon: '📊' },
		{ path: '/accounts', label: 'Accounts', icon: '🏦' },
		{ path: '/transactions', label: 'Transactions', icon: '💸' },
		{ path: '/budgets', label: 'Budgets', icon: '🎯' },
		{ path: '/savings', label: 'Savings Goals', icon: '💰' },
		{ path: '/investments', label: 'Investments', icon: '📈' },
		{ path: '/insights', label: 'AI Insights', icon: '🤖' },
		{ path: '/pricing', label: 'Pricing', icon: '💎' },
	];

	function isActive(path: string): boolean {
		// Handle both exact match and trailing slash
		const currentPath = $page.url.pathname;
		return currentPath === path || currentPath === path + '/';
	}

	function handleNavClick() {
		// Close mobile menu when navigation item is clicked
		mobileMenuOpen = false;
	}
</script>

<!-- Mobile Menu Button (visible only on mobile) -->
<button
	onclick={() => mobileMenuOpen = !mobileMenuOpen}
	class="md:hidden fixed top-4 left-4 z-50 p-3 glass-card rounded-lg text-2xl hover:bg-charcoal/60 transition-all"
	aria-label="Toggle menu"
>
	{mobileMenuOpen ? '✕' : '☰'}
</button>

<!-- Overlay (visible only when mobile menu is open) -->
{#if mobileMenuOpen}
	<div
		onclick={() => mobileMenuOpen = false}
		class="md:hidden fixed inset-0 bg-black/60 backdrop-blur-sm z-40"
	></div>
{/if}

<!-- Sidebar -->
<aside class="w-64 glass-card min-h-screen p-6 flex flex-col fixed md:static z-40 transition-transform duration-300 {mobileMenuOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'}">
	<!-- Logo -->
	<div class="mb-8">
		<h1 class="text-2xl font-bold gradient-text">WealthFlow</h1>
		<p class="text-white/60 text-sm mt-1">Financial Planner</p>
	</div>

	<!-- User Info -->
	{#if $auth.user}
		<div class="mb-8 p-4 glass-card">
			<p class="text-white/90 font-medium truncate">{$auth.user.full_name || $auth.user.email}</p>
			<p class="text-white/60 text-xs truncate">{$auth.user.email}</p>
			<div class="mt-2">
				<span class="text-xs px-2 py-1 rounded bg-emerald/20 text-emerald">
					{$auth.user.subscription_tier || 'Free'}
				</span>
			</div>
		</div>
	{/if}

	<!-- Navigation -->
	<nav class="flex-1 space-y-2">
		{#each navItems as item}
			<a
				href={item.path}
				onclick={handleNavClick}
				class="flex items-center gap-3 px-4 py-3 rounded-lg transition-all {isActive(item.path)
					? 'bg-emerald/20 text-emerald border border-emerald/30'
					: 'text-white/70 hover:bg-white/10 hover:text-white'}"
			>
				<span class="text-xl">{item.icon}</span>
				<span class="font-medium">{item.label}</span>
			</a>
		{/each}
	</nav>

	<!-- Logout Button -->
	<button onclick={handleLogout} class="btn-secondary w-full mt-6">
		Logout
	</button>
</aside>

