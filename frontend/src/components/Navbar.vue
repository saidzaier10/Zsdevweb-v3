<template>
  <nav class="bg-white/80 dark:bg-dark-800/80 backdrop-blur-md shadow-md sticky top-0 z-50 border-b border-gray-200 dark:border-dark-700 transition-colors duration-200">
    <div class="container mx-auto px-4 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <!-- Logo -->
        <router-link to="/" class="flex items-center space-x-2 group">
          <div class="w-10 h-10 bg-gradient-to-br from-primary-600 to-secondary-500 rounded-lg flex items-center justify-center transform group-hover:rotate-6 transition-transform duration-300">
            <span class="text-white font-bold text-xl">Zs</span>
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
              class="px-4 py-2 rounded-lg font-medium text-dark-700 dark:text-dark-200 hover:text-primary-600 hover:bg-primary-50 dark:hover:bg-dark-700 transition-all duration-200"
              active-class="text-primary-600 bg-primary-50 dark:bg-dark-700"
            >
              Accueil
            </router-link>
          </li>
          <li>
            <router-link 
              to="/portfolio" 
              class="px-4 py-2 rounded-lg font-medium text-dark-700 dark:text-dark-200 hover:text-primary-600 hover:bg-primary-50 dark:hover:bg-dark-700 transition-all duration-200"
              active-class="text-primary-600 bg-primary-50 dark:bg-dark-700"
            >
              Portfolio
            </router-link>
          </li>
          <li>
            <router-link
              to="/devis"
              class="px-4 py-2 rounded-lg font-medium text-dark-700 dark:text-dark-200 hover:text-primary-600 hover:bg-primary-50 dark:hover:bg-dark-700 transition-all duration-200"
              active-class="text-primary-600 bg-primary-50 dark:bg-dark-700"
            >
              Devis
            </router-link>
          </li>
          <!-- Mes Devis (uniquement si connecté et non admin) -->
          <li v-if="authStore.isAuthenticated && !authStore.user?.is_staff">
            <router-link
              to="/mes-devis"
              class="px-4 py-2 rounded-lg font-medium text-dark-700 dark:text-dark-200 hover:text-primary-600 hover:bg-primary-50 dark:hover:bg-dark-700 transition-all duration-200"
              active-class="text-primary-600 bg-primary-50 dark:bg-dark-700"
            >
              Mes Devis
            </router-link>
          </li>
          <!-- Admin (uniquement si admin) -->
          <li v-if="authStore.user?.is_staff">
            <router-link
              to="/admin/devis"
              class="px-4 py-2 rounded-lg font-medium text-dark-700 dark:text-dark-200 hover:text-primary-600 hover:bg-primary-50 dark:hover:bg-dark-700 transition-all duration-200"
              active-class="text-primary-600 bg-primary-50 dark:bg-dark-700"
            >
              Admin
            </router-link>
          </li>
          <li>
            <router-link
              to="/contact"
              class="px-4 py-2 rounded-lg font-medium text-dark-700 dark:text-dark-200 hover:text-primary-600 hover:bg-primary-50 dark:hover:bg-dark-700 transition-all duration-200"
              active-class="text-primary-600 bg-primary-50 dark:bg-dark-700"
            >
              Contact
            </router-link>
          </li>
        </ul>

        <!-- Auth Buttons + Dark Mode Toggle Desktop -->
        <div class="hidden md:flex items-center space-x-3">
          <!-- Dark Mode Toggle -->
          <button
            @click="themeStore.toggleDarkMode()"
            class="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-dark-700 transition-colors"
            aria-label="Toggle dark mode"
          >
            <!-- Sun Icon (visible in dark mode) -->
            <svg v-if="themeStore.isDark" class="w-5 h-5 text-yellow-500" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" clip-rule="evenodd"></path>
            </svg>
            <!-- Moon Icon (visible in light mode) -->
            <svg v-else class="w-5 h-5 text-dark-600" fill="currentColor" viewBox="0 0 20 20">
              <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z"></path>
            </svg>
          </button>

          <router-link 
            v-if="!authStore.isAuthenticated" 
            to="/login" 
            class="px-5 py-2 rounded-lg font-semibold text-primary-600 hover:bg-primary-50 dark:hover:bg-dark-700 transition-all duration-200"
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
            <div class="flex items-center space-x-2 px-4 py-2 bg-primary-50 dark:bg-dark-700 rounded-lg">
              <div class="w-8 h-8 bg-gradient-to-br from-primary-600 to-secondary-500 rounded-full flex items-center justify-center">
                <span class="text-white font-bold text-sm">{{ authStore.user?.username?.charAt(0).toUpperCase() }}</span>
              </div>
              <span class="font-medium text-dark-700 dark:text-dark-200">{{ authStore.user?.username }}</span>
            </div>
            <button 
              @click="handleLogout" 
              class="px-5 py-2 rounded-lg font-semibold text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20 transition-all duration-200"
            >
              Déconnexion
            </button>
          </div>
        </div>
        
        <!-- Bouton Menu Mobile -->
        <button 
          @click="mobileMenuOpen = !mobileMenuOpen" 
          class="md:hidden p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-dark-700 transition-colors"
          aria-label="Menu"
        >
          <svg v-if="!mobileMenuOpen" class="w-6 h-6 text-dark-700 dark:text-dark-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
          </svg>
          <svg v-else class="w-6 h-6 text-dark-700 dark:text-dark-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
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
      <div v-if="mobileMenuOpen" class="md:hidden border-t border-gray-200 dark:border-dark-700 bg-white dark:bg-dark-800">
        <div class="container mx-auto px-4 py-4 space-y-2">
          <router-link 
            to="/" 
            @click="mobileMenuOpen = false" 
            class="block px-4 py-3 rounded-lg font-medium text-dark-700 dark:text-dark-200 hover:text-primary-600 hover:bg-primary-50 dark:hover:bg-dark-700 transition-all"
            active-class="text-primary-600 bg-primary-50 dark:bg-dark-700"
          >
            Accueil
          </router-link>
          <router-link 
            to="/portfolio" 
            @click="mobileMenuOpen = false" 
            class="block px-4 py-3 rounded-lg font-medium text-dark-700 dark:text-dark-200 hover:text-primary-600 hover:bg-primary-50 dark:hover:bg-dark-700 transition-all"
            active-class="text-primary-600 bg-primary-50 dark:bg-dark-700"
          >
            Portfolio
          </router-link>
          <router-link
            to="/devis"
            @click="mobileMenuOpen = false"
            class="block px-4 py-3 rounded-lg font-medium text-dark-700 dark:text-dark-200 hover:text-primary-600 hover:bg-primary-50 dark:hover:bg-dark-700 transition-all"
            active-class="text-primary-600 bg-primary-50 dark:bg-dark-700"
          >
            Devis
          </router-link>
          <!-- Mes Devis (mobile - uniquement si connecté et non admin) -->
          <router-link
            v-if="authStore.isAuthenticated && !authStore.user?.is_staff"
            to="/mes-devis"
            @click="mobileMenuOpen = false"
            class="block px-4 py-3 rounded-lg font-medium text-dark-700 dark:text-dark-200 hover:text-primary-600 hover:bg-primary-50 dark:hover:bg-dark-700 transition-all"
            active-class="text-primary-600 bg-primary-50 dark:bg-dark-700"
          >
            Mes Devis
          </router-link>
          <!-- Admin (mobile - uniquement si admin) -->
          <router-link
            v-if="authStore.user?.is_staff"
            to="/admin/devis"
            @click="mobileMenuOpen = false"
            class="block px-4 py-3 rounded-lg font-medium text-dark-700 dark:text-dark-200 hover:text-primary-600 hover:bg-primary-50 dark:hover:bg-dark-700 transition-all"
            active-class="text-primary-600 bg-primary-50 dark:bg-dark-700"
          >
            Admin
          </router-link>
          <router-link
            to="/contact"
            @click="mobileMenuOpen = false"
            class="block px-4 py-3 rounded-lg font-medium text-dark-700 dark:text-dark-200 hover:text-primary-600 hover:bg-primary-50 dark:hover:bg-dark-700 transition-all"
            active-class="text-primary-600 bg-primary-50 dark:bg-dark-700"
          >
            Contact
          </router-link>
          
          <!-- Dark Mode Toggle Mobile -->
          <button
            @click="themeStore.toggleDarkMode()"
            class="w-full flex items-center justify-between px-4 py-3 rounded-lg font-medium text-dark-700 dark:text-dark-200 hover:bg-gray-100 dark:hover:bg-dark-700 transition-all"
          >
            <span>{{ themeStore.isDark ? 'Mode clair' : 'Mode sombre' }}</span>
            <svg v-if="themeStore.isDark" class="w-5 h-5 text-yellow-500" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" clip-rule="evenodd"></path>
            </svg>
            <svg v-else class="w-5 h-5 text-dark-600" fill="currentColor" viewBox="0 0 20 20">
              <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z"></path>
            </svg>
          </button>
          
          <div class="pt-4 space-y-2 border-t border-gray-200 dark:border-dark-700">
            <template v-if="!authStore.isAuthenticated">
              <router-link 
                to="/login" 
                @click="mobileMenuOpen = false" 
                class="block px-4 py-3 rounded-lg font-semibold text-center text-primary-600 hover:bg-primary-50 dark:hover:bg-dark-700 transition-all"
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
              <div class="px-4 py-3 bg-primary-50 dark:bg-dark-700 rounded-lg">
                <div class="flex items-center space-x-2">
                  <div class="w-8 h-8 bg-gradient-to-br from-primary-600 to-secondary-500 rounded-full flex items-center justify-center">
                    <span class="text-white font-bold text-sm">{{ authStore.user?.username?.charAt(0).toUpperCase() }}</span>
                  </div>
                  <span class="font-medium text-dark-700 dark:text-dark-200">{{ authStore.user?.username }}</span>
                </div>
              </div>
              <button 
                @click="handleLogout" 
                class="w-full px-4 py-3 rounded-lg font-semibold text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20 transition-all"
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
import { useThemeStore } from '../stores/theme'

const router = useRouter()
const authStore = useAuthStore()
const themeStore = useThemeStore()
const mobileMenuOpen = ref(false)

const handleLogout = async () => {
  await authStore.logout()
  mobileMenuOpen.value = false
  router.push('/')
}
</script>