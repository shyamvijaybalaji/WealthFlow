/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    extend: {
      colors: {
        'midnight-blue': '#1A1A2E',
        'charcoal': '#2C2C34',
        'emerald': '#00D9A3',
        'cyan': '#00B4D8',
        'gold': '#FFD700',
      },
      backdropBlur: {
        'glass': '10px',
      }
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}
