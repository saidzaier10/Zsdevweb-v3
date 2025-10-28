<template>
  <div class="min-h-screen bg-white dark:bg-dark-900 transition-colors duration-200">
    <Navbar />
    <router-view />
    <Footer />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import Navbar from './components/Navbar.vue'
import Footer from './components/Footer.vue'
import { useThemeStore } from './stores/theme'

const themeStore = useThemeStore()

onMounted(() => {
  console.log('App mounted, initializing theme...')
  themeStore.initTheme()
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