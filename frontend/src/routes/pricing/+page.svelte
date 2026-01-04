<script lang="ts">
	import { goto } from '$app/navigation';
	import Sidebar from '$lib/components/layout/Sidebar.svelte';

	interface PricingTier {
		name: string;
		price: string;
		period: string;
		description: string;
		features: string[];
		cta: string;
		popular?: boolean;
		disabled?: boolean;
	}

	const tiers: PricingTier[] = [
		{
			name: 'Free',
			price: '$0',
			period: '/month',
			description: 'Perfect for getting started with personal finance tracking',
			features: [
				'Up to 2 bank accounts',
				'100 transactions per month',
				'Basic expense categorization',
				'Simple budget tracking',
				'Monthly financial reports',
				'Mobile responsive design'
			],
			cta: 'Get Started Free'
		},
		{
			name: 'Pro',
			price: '$9.99',
			period: '/month',
			description: 'Advanced features for serious financial planning',
			features: [
				'Unlimited bank accounts',
				'Unlimited transactions',
				'Advanced categorization & tags',
				'Custom budgets & goals',
				'Investment portfolio tracking',
				'AI-powered insights',
				'Expense forecasting',
				'Export to CSV/PDF',
				'Priority email support'
			],
			cta: 'Start Pro Trial',
			popular: true
		},
		{
			name: 'Elite',
			price: '$19.99',
			period: '/month',
			description: 'Premium suite for wealth management',
			features: [
				'Everything in Pro',
				'Multi-currency support',
				'Tax optimization insights',
				'Advanced AI recommendations',
				'Custom financial reports',
				'API access',
				'Dedicated account manager',
				'White-label options',
				'Priority phone & chat support'
			],
			cta: 'Contact Sales'
		}
	];

	const faqs = [
		{
			question: 'Can I change plans anytime?',
			answer: 'Yes! You can upgrade or downgrade your plan at any time. Changes take effect immediately.'
		},
		{
			question: 'Is my financial data secure?',
			answer: 'Absolutely. We use bank-level 256-bit SSL encryption and never store your bank credentials.'
		},
		{
			question: 'Do you offer refunds?',
			answer: 'We offer a 30-day money-back guarantee on all paid plans, no questions asked.'
		},
		{
			question: 'What payment methods do you accept?',
			answer: 'We accept all major credit cards, debit cards, and PayPal payments.'
		}
	];

	function handleCTA(tier: PricingTier) {
		if (tier.name === 'Free') {
			goto('/register');
		} else if (tier.name === 'Elite') {
			window.location.href = 'mailto:support@wealthflow.fun?subject=Elite Plan Inquiry';
		} else {
			// Redirect to payment/checkout (to be implemented)
			alert('Pro plan checkout coming soon! Please contact support@wealthflow.fun');
		}
	}
</script>

<svelte:head>
	<title>Pricing - WealthFlow</title>
	<meta name="description" content="Choose the perfect WealthFlow plan for your financial journey" />
</svelte:head>

<div class="flex min-h-screen bg-gradient-to-br from-[#1A1A2E] via-[#2C2C34] to-[#1A1A2E]">
	<!-- Sidebar -->
	<Sidebar />

	<!-- Main Content -->
	<main class="flex-1 px-4 pt-20 pb-4 sm:p-6 md:p-8 overflow-y-auto">
		<div class="max-w-7xl mx-auto">
			<!-- Header -->
			<div class="text-center mb-8 md:mb-16">
				<h1 class="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-bold mb-4 md:mb-6 bg-gradient-to-r from-[#00D9A3] via-[#00B4D8] to-[#FFD700] bg-clip-text text-transparent">
					Simple, Transparent Pricing
				</h1>
				<p class="text-base sm:text-lg md:text-xl text-gray-300 max-w-2xl mx-auto">
					Choose the plan that fits your financial goals. No hidden fees, cancel anytime.
				</p>
			</div>

			<!-- Pricing Cards -->
			<div class="grid grid-cols-1 md:grid-cols-3 gap-6 md:gap-8 mb-12 md:mb-20">
				{#each tiers as tier}
					<div class="glass-card relative {tier.popular ? 'border-2 border-[#00D9A3] md:scale-105' : ''} transition-transform duration-300 hover:scale-105">
						{#if tier.popular}
							<div class="absolute -top-4 left-1/2 -translate-x-1/2 bg-gradient-to-r from-[#00D9A3] to-[#00B4D8] px-4 py-1 rounded-full text-sm font-semibold">
								Most Popular
							</div>
						{/if}

						<div class="p-8">
							<!-- Tier Name -->
							<h3 class="text-2xl font-bold mb-2 text-white">{tier.name}</h3>
							<p class="text-gray-400 mb-6">{tier.description}</p>

							<!-- Price -->
							<div class="mb-8">
								<span class="text-5xl font-bold text-white">{tier.price}</span>
								<span class="text-gray-400">{tier.period}</span>
							</div>

							<!-- Features -->
							<ul class="space-y-3 mb-8">
								{#each tier.features as feature}
									<li class="flex items-start">
										<svg class="w-5 h-5 text-[#00D9A3] mr-3 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
											<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
										</svg>
										<span class="text-gray-300">{feature}</span>
									</li>
								{/each}
							</ul>

							<!-- CTA Button -->
							<button
								on:click={() => handleCTA(tier)}
								disabled={tier.disabled}
								class="w-full py-3 rounded-lg font-semibold transition-all duration-300
									{tier.popular
										? 'bg-gradient-to-r from-[#00D9A3] to-[#00B4D8] hover:shadow-lg hover:shadow-[#00D9A3]/50'
										: 'bg-white/10 hover:bg-white/20'
									}
									{tier.disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
								"
							>
								{tier.cta}
							</button>
						</div>
					</div>
				{/each}
			</div>

			<!-- FAQ Section -->
			<div class="max-w-3xl mx-auto">
				<h2 class="text-2xl md:text-3xl font-bold text-center mb-8 md:mb-12 text-white">Frequently Asked Questions</h2>
				<div class="space-y-4 md:space-y-6">
					{#each faqs as faq}
						<div class="glass-card p-4 md:p-6">
							<h3 class="text-lg md:text-xl font-semibold mb-2 md:mb-3 text-[#00D9A3]">{faq.question}</h3>
							<p class="text-sm md:text-base text-gray-300">{faq.answer}</p>
						</div>
					{/each}
				</div>
			</div>

			<!-- Bottom CTA -->
			<div class="text-center mt-16">
				<p class="text-gray-400 mb-4">Still have questions?</p>
				<a href="mailto:support@wealthflow.fun" class="text-[#00D9A3] hover:text-[#00B4D8] font-semibold underline">
					Contact our support team
				</a>
			</div>
		</div>
	</main>
</div>

<style>
	.glass-card {
		background: rgba(44, 44, 52, 0.4);
		backdrop-filter: blur(10px);
		border: 1px solid rgba(255, 255, 255, 0.1);
		border-radius: 16px;
	}
</style>

