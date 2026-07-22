/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./app/**/*.{js,ts,jsx,tsx}', './components/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        brand:  { 50:'#eef7ff',100:'#d9edff',200:'#bce0ff',300:'#8ecdff',400:'#59b0ff',
                  500:'#3392ff',600:'#1c72f5',700:'#155ce1',800:'#184bb6',900:'#19428f' },
        mint:   { 400:'#34d399', 500:'#10b981', 600:'#059669' },
        sun:    { 400:'#fbbf24', 500:'#f59e0b' },
        coral:  { 400:'#fb7185', 500:'#f43f5e' },
      },
      fontFamily: { display: ['Nunito', 'system-ui', 'sans-serif'] },
      animation: {
        'pop': 'pop 0.3s cubic-bezier(0.34,1.56,0.64,1)',
        'shake': 'shake 0.4s',
        'float': 'float 3s ease-in-out infinite',
        'slide-up': 'slideUp 0.3s ease-out',
      },
      keyframes: {
        pop: { '0%':{transform:'scale(0.8)',opacity:'0'}, '100%':{transform:'scale(1)',opacity:'1'} },
        shake: { '0%,100%':{transform:'translateX(0)'}, '25%':{transform:'translateX(-6px)'}, '75%':{transform:'translateX(6px)'} },
        float: { '0%,100%':{transform:'translateY(0)'}, '50%':{transform:'translateY(-8px)'} },
        slideUp: { '0%':{transform:'translateY(20px)',opacity:'0'}, '100%':{transform:'translateY(0)',opacity:'1'} },
      },
    },
  },
  plugins: [],
};
