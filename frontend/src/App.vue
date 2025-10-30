<template>
  <div class="min-h-screen bg-white dark:bg-dark-900 transition-colors duration-200">
    <Navbar />
    <router-view />
    <Footer />
    
    <!-- Système de notifications toast -->
    <div class="fixed top-4 right-4 z-50 space-y-3">
      <Toast 
        v-for="toast in toasts" 
        :key="toast.id" 
        :type="toast.type"
        :title="toast.title"
        :message="toast.message"
        :duration="toast.duration"
        @close="removeToast(toast.id)"
      />
    </div>
  </div>
</template>

<script setup>
import { onMounted, computed } from 'vue'
import Navbar from './components/Navbar.vue'
import Footer from './components/Footer.vue'
import Toast from './components/Toast.vue'
import { useThemeStore } from './stores/theme'
import { useToastStore } from './stores/toast'

const themeStore = useThemeStore()
const toastStore = useToastStore()

const toasts = computed(() => toastStore.toasts)

const removeToast = (id) => {
  toastStore.remove(id)
}

onMounted(() => {
  console.log('App mounted, initializing theme...')
  themeStore.initTheme()
})
</script>

<style>
#app {
  min-h-screen: 100vh;
  display: flex;
  flex-direction: column;
}

main {
  flex: 1;
}
</style>