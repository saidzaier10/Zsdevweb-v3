<template>
  <nav class="bg-white/80 backdrop-blur-md shadow-md sticky top-0 z-50 border-b border-gray-200">
    <div class="container mx-auto px-4 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <!-- Logo -->
        <router-link to="/" class="flex items-center space-x-2 group">
          <div class="w-10 h-10 bg-gradient-to-br from-primary-600 to-secondary-500 rounded-lg flex items-center justify-center transform group-hover:rotate-6 transition-transform duration-300">
            <span class="text-white font-bold text-xl">Z</span>
          </div>
          <span class="text-2xl font-display font-bold gradient-text hidden sm:block">
            Zsdevweb
          </span>
        </router-link>
        
        <!-- Navigation Desktop -->
        <ul class="hidden md:flex items-center space-x-1">
          <li>
            <router-link 
              to="/" 
              class="px-4 py-2 rounded-lg font-medium text-dark-700 hover:text-primary-600 hover:bg-primary-50 transition-all duration-200"
              active-class="text-primary-600 bg-primary-50"
            >
              Accueil
            </router-link>
          </li>
          <li>
            <router-link 
              to="/portfolio" 
              class="px-4 py-2 rounded-lg font-medium text-dark-700 hover:text-primary-600 hover:bg-primary-50 transition-all duration-200"
              active-class="text-primary-600 bg-primary-50"
            >
              Portfolio
            </router-link>
          </li>
          <li>
            <router-link 
              to="/devis" 
              class="px-4 py-2 rounded-lg font-medium text-dark-700 hover:text-primary-600 hover:bg-primary-50 transition-all duration-200"
              active-class="text-primary-600 bg-primary-50"
            >
              Devis
            </router-link>
          </li>
          <li>
            <router-link 
              to="/contact" 
              class="px-4 py-2 rounded-lg font-medium text-dark-700 hover:text-primary-600 hover:bg-primary-50 transition-all duration-200"
              active-class="text-primary-600 bg-primary-50"
            >
              Contact
            </router-link>
          </li>
        </ul>

        <!-- Auth Buttons Desktop -->
        <div class="hidden md:flex items-center space-x-3">
          <router-link 
            v-if="!authStore.isAuthenticated" 
            to="/login" 
            class="px-5 py-2 rounded-lg font-semibold text-primary-600 hover:bg-primary-50 transition-all duration-200"
          >
            Connexion
          </router-link>
          <router-link 
            v-if="!authStore.isAuthenticated" 
            to="/register" 
            class="btn-primary"
          >
            Inscription
          </router-link>
          
          <!-- User Menu (si connecté) -->
          <div v-else class="flex items-center space-x-3">
            <div class="flex items-center space-x-2 px-4 py-2 bg-primary-50 rounded-lg">
              <div class="w-8 h-8 bg-gradient-to-br from-primary-600 to-secondary-500 rounded-full flex items-center justify-center">
                <span class="text-white font-bold text-sm">{{ authStore.user?.username?.charAt(0).toUpperCase() }}</span>
              </div>
              <span class="font-medium text-dark-700">{{ authStore.user?.username }}</span>
            </div>
            <button 
              @click="handleLogout" 
              class="px-5 py-2 rounded-lg font-semibold text-red-600 hover:bg-red-50 transition-all duration-200"
            >
              Déconnexion
            </button>
          </div>
        </div>
        
        <!-- Bouton Menu Mobile -->
        <button 
          @click="mobileMenuOpen = !mobileMenuOpen" 
          class="md:hidden p-2 rounded-lg hover:bg-gray-100 transition-colors"
          aria-label="Menu"
        >
          <svg v-if="!mobileMenuOpen" class="w-6 h-6 text-dark-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
          </svg>
          <svg v-else class="w-6 h-6 text-dark-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </button>
      </div>
    </div>
    
    <!-- Menu Mobile -->
    <transition
      enter-active-class="transition duration-200 ease-out"
      enter-from-class="opacity-0 -translate-y-2"
      enter-to-class="opacity-100 translate-y-0"
      leave-active-class="transition duration-150 ease-in"
      leave-from-class="opacity-100 translate-y-0"
      leave-to-class="opacity-0 -translate-y-2"
    >
      <div v-if="mobileMenuOpen" class="md:hidden border-t border-gray-200 bg-white">
        <div class="container mx-auto px-4 py-4 space-y-2">
          <router-link 
            to="/" 
            @click="mobileMenuOpen = false" 
            class="block px-4 py-3 rounded-lg font-medium text-dark-700 hover:text-primary-600 hover:bg-primary-50 transition-all"
            active-class="text-primary-600 bg-primary-50"
          >
            Accueil
          </router-link>
          <router-link 
            to="/portfolio" 
            @click="mobileMenuOpen = false" 
            class="block px-4 py-3 rounded-lg font-medium text-dark-700 hover:text-primary-600 hover:bg-primary-50 transition-all"
            active-class="text-primary-600 bg-primary-50"
          >
            Portfolio
          </router-link>
          <router-link 
            to="/devis" 
            @click="mobileMenuOpen = false" 
            class="block px-4 py-3 rounded-lg font-medium text-dark-700 hover:text-primary-600 hover:bg-primary-50 transition-all"
            active-class="text-primary-600 bg-primary-50"
          >
            Devis
          </router-link>
          <router-link 
            to="/contact" 
            @click="mobileMenuOpen = false" 
            class="block px-4 py-3 rounded-lg font-medium text-dark-700 hover:text-primary-600 hover:bg-primary-50 transition-all"
            active-class="text-primary-600 bg-primary-50"
          >
            Contact
          </router-link>
          
          <div class="pt-4 space-y-2 border-t border-gray-200">
            <template v-if="!authStore.isAuthenticated">
              <router-link 
                to="/login" 
                @click="mobileMenuOpen = false" 
                class="block px-4 py-3 rounded-lg font-semibold text-center text-primary-600 hover:bg-primary-50 transition-all"
              >
                Connexion
              </router-link>
              <router-link 
                to="/register" 
                @click="mobileMenuOpen = false" 
                class="block btn-primary text-center"
              >
                Inscription
              </router-link>
            </template>
            
            <template v-else>
              <div class="px-4 py-3 bg-primary-50 rounded-lg">
                <div class="flex items-center space-x-2">
                  <div class="w-8 h-8 bg-gradient-to-br from-primary-600 to-secondary-500 rounded-full flex items-center justify-center">
                    <span class="text-white font-bold text-sm">{{ authStore.user?.username?.charAt(0).toUpperCase() }}</span>
                  </div>
                  <span class="font-medium text-dark-700">{{ authStore.user?.username }}</span>
                </div>
              </div>
              <button 
                @click="handleLogout" 
                class="w-full px-4 py-3 rounded-lg font-semibold text-red-600 hover:bg-red-50 transition-all"
              >
                Déconnexion
              </button>
            </template>
          </div>
        </div>
      </div>
    </transition>
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