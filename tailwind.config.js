/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [],
  theme: {
    extend: {
      animation: {
        'bounce-right': 'bounce-right 1s infinite', // Custom animation
      },
      keyframes: {
        'bounce-right': {
          '0%, 100%': { transform: 'translateX(0)' }, // Start and end at the original position
          '50%': { transform: 'translateX(25px)' }, // Move 25px to the right
        },
      },
    },
  },
  plugins: [],
}