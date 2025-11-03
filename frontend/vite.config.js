import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'node:path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src')
    }
  },
  server: {
    host: '0.0.0.0',  // Écoute sur toutes les interfaces
    port: 5173,
    strictPort: true,
    watch: {
      usePolling: true  // Nécessaire pour Docker
    }
  },
  build: {
    // Optimisations de build
    rollupOptions: {
      output: {
        // Séparation manuelle des chunks pour meilleur caching
        manualChunks: {
          'vendor': ['vue', 'vue-router', 'pinia', 'axios'],
        }
      }
    },
    // Limite de taille pour les warnings
    chunkSizeWarningLimit: 1000,
    // Minification optimale
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true, // Supprime les console.log en production
        drop_debugger: true
      }
    },
    // Source maps pour debug en prod (optionnel)
    sourcemap: false,
  }
})
