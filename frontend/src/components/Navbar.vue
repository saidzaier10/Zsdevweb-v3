<template>
  <nav class="bg-black text-white sticky top-0 z-50 shadow-md">
    <div class="container mx-auto px-4 py-4 flex justify-between items-center">
      <router-link to="/" class="text-2xl font-bold">
        Zsdevweb
      </router-link>
      
      <ul class="hidden md:flex space-x-8 items-center">
        <li>
          <router-link to="/" class="hover:text-gray-300 transition">Accueil</router-link>
        </li>
        <li>
          <router-link to="/portfolio" class="hover:text-gray-300 transition">Portfolio</router-link>
        </li>
        <li>
          <router-link to="/devis" class="hover:text-gray-300 transition">Devis</router-link>
        </li>
        <li>
          <router-link to="/contact" class="hover:text-gray-300 transition">Contact</router-link>
        </li>
        
        <!-- Boutons Auth -->
        <li v-if="!authStore.isAuthenticated">
          <router-link to="/login" class="bg-white text-black px-4 py-2 rounded font-bold hover:bg-gray-200 transition">
            Connexion
          </router-link>
        </li>
        <li v-else class="flex items-center space-x-4">
          <span class="text-gray-300">{{ authStore.user?.username }}</span>
          <button @click="handleLogout" class="bg-white text-black px-4 py-2 rounded font-bold hover:bg-gray-200 transition">
            Déconnexion
          </button>
        </li>
      </ul>
      
      <!-- Bouton menu mobile -->
      <button @click="mobileMenuOpen = !mobileMenuOpen" class="md:hidden">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
        </svg>
      </button>
    </div>
    
    <!-- Menu mobile -->
    <div v-if="mobileMenuOpen" class="md:hidden bg-black border-t border-gray-800">
      <ul class="px-4 py-4 space-y-4">
        <li>
          <router-link to="/" @click="mobileMenuOpen = false" class="block hover:text-gray-300 transition">Accueil</router-link>
        </li>
        <li>
          <router-link to="/portfolio" @click="mobileMenuOpen = false" class="block hover:text-gray-300 transition">Portfolio</router-link>
        </li>
        <li>
          <router-link to="/devis" @click="mobileMenuOpen = false" class="block hover:text-gray-300 transition">Devis</router-link>
        </li>
        <li>
          <router-link to="/contact" @click="mobileMenuOpen = false" class="block hover:text-gray-300 transition">Contact</router-link>
        </li>
        
        <li v-if="!authStore.isAuthenticated" class="pt-4 border-t border-gray-800">
          <router-link to="/login" @click="mobileMenuOpen = false" class="block bg-white text-black px-4 py-2 rounded font-bold text-center hover:bg-gray-200 transition">
            Connexion
          </router-link>
        </li>
        <li v-else class="pt-4 border-t border-gray-800 space-y-2">
          <p class="text-gray-300">{{ authStore.user?.username }}</p>
          <button @click="handleLogout" class="w-full bg-white text-black px-4 py-2 rounded font-bold hover:bg-gray-200 transition">
            Déconnexion
          </button>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const mobileMenuOpen = ref(false)

const handleLogout = async () => {
  await authStore.logout()
  mobileMenuOpen.value = false
  router.push('/')
}
</script>