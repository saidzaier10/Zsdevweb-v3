<template>
  <div
    class="min-h-screen bg-gradient-to-br from-primary-600 via-primary-700 to-secondary-600 dark:from-primary-900 dark:via-primary-800 dark:to-secondary-900 text-white transition-colors duration-200 relative">
    <!-- Global Animated Background -->


    <div class="relative flex flex-col min-h-screen">
      <Navbar />

      <!-- Router view with page transitions -->
      <router-view v-slot="{ Component, route }">
        <transition name="page" mode="out-in">
          <component :is="Component" :key="route.path" />
        </transition>
      </router-view>

      <Footer />
    </div>

    <!-- Toast Container -->
    <div class="fixed top-4 right-4 z-50 space-y-3">
      <Toast v-for="toast in toasts" :key="toast.id" :type="toast.type" :title="toast.title" :message="toast.message"
        @close="removeToast(toast.id)" />
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
  toastStore.removeToast(id)
}

import { isLowEndDevice } from './utils/performance'

onMounted(() => {
  // Initialisation du thème au montage de l'application
  themeStore.initTheme()

  // Disable heavy animations on low-end devices
  if (isLowEndDevice()) {
    document.body.classList.add('reduce-motion')
  }
})
</script>

<style>
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

main {
  flex: 1;
}
</style>
