/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./store_analysis/templates/**/*.html",
    "./store_analysis/static/**/*.js",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
  corePlugins: {
    preflight: false,
  }
} 