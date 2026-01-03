<script lang="ts">
	import { auth } from '$lib/stores/auth';
	import { goto } from '$app/navigation';

	$: if ($auth.user) {
		goto('/dashboard');
	}
</script>

<div class="min-h-screen flex items-center justify-center px-4">
	<div class="max-w-4xl w-full text-center">
		<!-- Hero Section -->
		<div class="mb-8 md:mb-12">
			<h1 class="text-4xl sm:text-5xl md:text-6xl font-bold mb-3 md:mb-4 gradient-text">
				WealthFlow
			</h1>
			<p class="text-xl sm:text-2xl text-white/80 mb-2">
				Master Your Money
			</p>
			<p class="text-base md:text-lg text-white/60">
				AI-Driven Personal Finance & Budget Planning
			</p>
		</div>

		<!-- CTA Buttons -->
		<div class="flex flex-col sm:flex-row gap-3 sm:gap-4 justify-center max-w-sm sm:max-w-none mx-auto">
			<a href="/register" class="btn-primary">
				Get Started
			</a>
			<a href="/login" class="btn-secondary">
				Login
			</a>
		</div>

		<!-- Features Grid -->
		<div class="mt-20 grid grid-cols-1 md:grid-cols-3 gap-6">
			<div class="glass-card glass-card-hover p-6">
				<div class="text-emerald text-4xl mb-4">📊</div>
				<h3 class="text-xl font-semibold mb-2">Smart Budgeting</h3>
				<p class="text-white/70">Track expenses with AI-powered insights and alerts</p>
			</div>

			<div class="glass-card glass-card-hover p-6">
				<div class="text-cyan text-4xl mb-4">🎯</div>
				<h3 class="text-xl font-semibold mb-2">Savings Goals</h3>
				<p class="text-white/70">Set and achieve your financial milestones</p>
			</div>

			<div class="glass-card glass-card-hover p-6">
				<div class="text-gold text-4xl mb-4">💰</div>
				<h3 class="text-xl font-semibold mb-2">Investment Tracking</h3>
				<p class="text-white/70">Monitor your portfolio with real-time updates</p>
			</div>
		</div>
	</div>
</div>
