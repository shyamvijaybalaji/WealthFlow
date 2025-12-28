<script lang="ts">
	import { onMount } from 'svelte';
	import { Chart, registerables } from 'chart.js';

	interface Props {
		labels: string[];
		data: number[];
		colors: string[];
	}

	let { labels, data, colors }: Props = $props();
	let canvas: HTMLCanvasElement;
	let chart: Chart | null = null;

	onMount(() => {
		Chart.register(...registerables);

		const ctx = canvas.getContext('2d');
		if (!ctx) return;

		chart = new Chart(ctx, {
			type: 'doughnut',
			data: {
				labels: labels,
				datasets: [{
					data: data,
					backgroundColor: colors,
					borderColor: '#1A1A2E',
					borderWidth: 2
				}]
			},
			options: {
				responsive: true,
				maintainAspectRatio: true,
				plugins: {
					legend: {
						position: 'right',
						labels: {
							color: '#ffffff',
							font: {
								size: 12
							},
							padding: 12,
							usePointStyle: true,
							pointStyle: 'circle'
						}
					},
					tooltip: {
						callbacks: {
							label: function(context) {
								const label = context.label || '';
								const value = context.parsed || 0;
								const total = context.dataset.data.reduce((a: number, b: number) => a + b, 0) as number;
								const percentage = ((value / total) * 100).toFixed(1);
								return `${label}: $${value.toFixed(2)} (${percentage}%)`;
							}
						}
					}
				},
				cutout: '65%'
			}
		});

		return () => {
			chart?.destroy();
		};
	});

	$effect(() => {
		if (chart) {
			chart.data.labels = labels;
			chart.data.datasets[0].data = data;
			chart.data.datasets[0].backgroundColor = colors;
			chart.update();
		}
	});
</script>

<div class="w-full h-full">
	<canvas bind:this={canvas}></canvas>
</div>
