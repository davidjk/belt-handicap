import { defineConfig } from 'vite';

export default defineConfig({
  base: '/belt-handicap/',
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: true
  },
  server: {
    port: 3001,
    strictPort: false,
    open: true
  }
});