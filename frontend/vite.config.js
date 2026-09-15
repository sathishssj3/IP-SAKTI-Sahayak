import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// src/App.jsx calls a relative /api, so whatever serves the app has to forward
// it to the FastAPI backend (backend/main.py on :8000). Both dev and preview
// need this — without it the page loads fine and every API call 404s on Vite.
const apiProxy = {
  '/api': {
    target: 'http://127.0.0.1:8000',
    changeOrigin: true,
  },
};

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    strictPort: false,
    proxy: apiProxy,
  },
  preview: {
    proxy: apiProxy,
  },
  build: {
    outDir: 'dist',
    sourcemap: false,
  },
});
