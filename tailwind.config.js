/** @type {import('tailwindcss').Config} */
module.exports = {
	content: ['./app/templates/**/*.html'],
	theme: {
		extend: {
			animation: {
				'fade-in': 'fade-in 0.3s ease-in-out',
			},
		},
	},
	plugins: [],
}
