<script lang="ts">
	import { auth } from '$lib/stores/auth';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';

	let email = $state('');
	let password = $state('');
	let confirmPassword = $state('');
	let fullName = $state('');
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

		// Validate passwords match
		if (password !== confirmPassword) {
			error = 'Passwords do not match';
			return;
		}

		// Validate password length
		if (password.length < 8) {
			error = 'Password must be at least 8 characters';
			return;
		}

		loading = true;

		try {
			await auth.register(email, password, fullName || undefined);
			goto('/dashboard');
		} catch (err: any) {
			error = err.response?.data?.detail || 'Registration failed. Please try again.';
		} finally {
			loading = false;
		}
	}
</script>

<div class="min-h-screen flex items-center justify-center px-4 py-12">
	<div class="glass-card p-8 w-full max-w-md">
		<!-- Header -->
		<div class="text-center mb-6 md:mb-8">
			<h1 class="text-3xl md:text-4xl font-bold mb-2 gradient-text">Get Started</h1>
			<p class="text-sm md:text-base text-white/70">Create your WealthFlow account</p>
		</div>

		<!-- Error Message -->
		{#if error}
			<div class="mb-6 p-4 bg-red-500/20 border border-red-500/50 rounded-lg">
				<p class="text-red-300 text-sm">{error}</p>
			</div>
		{/if}

		<!-- Register Form -->
		<form onsubmit={handleSubmit} class="space-y-6">
			<!-- Full Name Field -->
			<div>
				<label for="fullName" class="block text-sm font-medium text-white/90 mb-2">
					Full Name (Optional)
				</label>
				<input
					id="fullName"
					type="text"
					bind:value={fullName}
					class="input-glass"
					placeholder="John Doe"
					disabled={loading}
				/>
			</div>

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
				<p class="text-white/50 text-xs mt-1">Minimum 8 characters</p>
			</div>

			<!-- Confirm Password Field -->
			<div>
				<label for="confirmPassword" class="block text-sm font-medium text-white/90 mb-2">
					Confirm Password
				</label>
				<input
					id="confirmPassword"
					type="password"
					bind:value={confirmPassword}
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
				{loading ? 'Creating Account...' : 'Create Account'}
			</button>
		</form>

		<!-- Login Link -->
		<div class="mt-6 text-center">
			<p class="text-white/60 text-sm">
				Already have an account?
				<a href="/login" class="text-emerald hover:text-cyan transition-colors font-semibold">
					Sign in
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
