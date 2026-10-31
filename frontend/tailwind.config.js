/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        aqi: {
          good: "#22c55e",       // 0-50 Green
          moderate: "#eab308",   // 51-100 Yellow
          poor: "#f97316",       // 101-200 Orange
          verypoor: "#ef4444",   // 201-300 Red
          severe: "#a855f7",     // 301-400 Purple
          hazardous: "#881337",  // 401+ Maroon
        },
      },
    },
  },
  plugins: [],
}
