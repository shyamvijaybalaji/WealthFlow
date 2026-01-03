<script lang="ts">
	import { auth } from '$lib/stores/auth';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';

	let email = $state('');
	let password = $state('');
	let error = $state('');
	let loading = $state(false);

	// Redirect if already logged in
	onMount(() => {
		if ($auth.user) {
			goto('/dashboard');
		}
	});

	async function handleSubmit() {
		error = '';
		loading = true;

		try {
			await auth.login(email, password);
			goto('/dashboard');
		} catch (err: any) {
			error = err.response?.data?.detail || 'Login failed. Please check your credentials.';
		} finally {
			loading = false;
		}
	}
</script>

<div class="min-h-screen flex items-center justify-center px-4">
	<div class="glass-card p-8 w-full max-w-md">
		<!-- Header -->
		<div class="text-center mb-6 md:mb-8">
			<h1 class="text-3xl md:text-4xl font-bold mb-2 gradient-text">Welcome Back</h1>
			<p class="text-sm md:text-base text-white/70">Sign in to your WealthFlow account</p>
		</div>

		<!-- Error Message -->
		{#if error}
			<div class="mb-6 p-4 bg-red-500/20 border border-red-500/50 rounded-lg">
				<p class="text-red-300 text-sm">{error}</p>
			</div>
		{/if}

		<!-- Login Form -->
		<form onsubmit={handleSubmit} class="space-y-6">
			<!-- Email Field -->
			<div>
				<label for="email" class="block text-sm font-medium text-white/90 mb-2">
					Email Address
				</label>
				<input
					id="email"
					type="email"
					bind:value={email}
					required
					class="input-glass"
					placeholder="you@example.com"
					disabled={loading}
				/>
			</div>

			<!-- Password Field -->
			<div>
				<label for="password" class="block text-sm font-medium text-white/90 mb-2">
					Password
				</label>
				<input
					id="password"
					type="password"
					bind:value={password}
					required
					class="input-glass"
					placeholder="••••••••"
					disabled={loading}
				/>
			</div>

			<!-- Submit Button -->
			<button
				type="submit"
				class="btn-primary w-full"
				disabled={loading}
			>
				{loading ? 'Signing in...' : 'Sign In'}
			</button>
		</form>

		<!-- Register Link -->
		<div class="mt-6 text-center">
			<p class="text-white/60 text-sm">
				Don't have an account?
				<a href="/register" class="text-emerald hover:text-cyan transition-colors font-semibold">
					Sign up
				</a>
			</p>
		</div>

		<!-- Back to Home -->
		<div class="mt-4 text-center">
			<a href="/" class="text-white/50 hover:text-white/80 transition-colors text-sm">
				← Back to Home
			</a>
		</div>
	</div>
</div>
