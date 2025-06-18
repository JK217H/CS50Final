/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  safelist: [
    {
      pattern: /(bg|text|border)-backgroundblue/,
    },
  ],
  theme: {
    extend: {
      colors: {
        backgroundblue: '#cfe9e6',
      },
    },
  },
  plugins: [],
};
