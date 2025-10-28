<template>
  <div class="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50 dark:from-dark-900 dark:to-dark-800 flex items-center justify-center py-16 transition-colors duration-200">
    <div class="container mx-auto px-4 max-w-md">
      <div class="bg-white dark:bg-dark-800 rounded-2xl shadow-2xl p-8 border border-gray-100 dark:border-dark-700">
        <div class="text-center mb-8">
          <div class="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-primary-600 to-secondary-500 rounded-2xl mb-4">
            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1"></path>
            </svg>
          </div>
          <h1 class="text-3xl font-bold text-dark-900 dark:text-white mb-2">Connexion</h1>
          <p class="text-dark-600 dark:text-dark-300">Bienvenue ! Connectez-vous à votre compte</p>
        </div>
        
        <form @submit.prevent="handleLogin" class="space-y-5">
          <div>
            <label class="block text-sm font-semibold text-dark-700 dark:text-dark-200 mb-2">
              Nom d'utilisateur <span class="text-red-500">*</span>
            </label>
            <input 
              v-model="form.username" 
              type="text" 
              required 
              class="w-full px-4 py-3 border-2 border-gray-200 dark:border-dark-600 dark:bg-dark-700 dark:text-white rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
              placeholder="Votre nom d'utilisateur"
            >
          </div>
          
          <div>
            <label class="block text-sm font-semibold text-dark-700 dark:text-dark-200 mb-2">
              Mot de passe <span class="text-red-500">*</span>
            </label>
            <input 
              v-model="form.password" 
              type="password" 
              required 
              class="w-full px-4 py-3 border-2 border-gray-200 dark:border-dark-600 dark:bg-dark-700 dark:text-white rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
              placeholder="Votre mot de passe"
            >
          </div>

          <button 
            type="submit" 
            :disabled="loading"
            class="w-full bg-gradient-to-r from-primary-600 to-secondary-500 text-white px-8 py-3 rounded-lg font-bold hover:from-primary-700 hover:to-secondary-600 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-xl"
          >
            {{ loading ? 'Connexion...' : 'Se connecter' }}
          </button>
        </form>

        <p v-if="error" class="mt-4 text-red-600 dark:text-red-400 font-semibold text-center text-sm bg-red-50 dark:bg-red-900/20 p-3 rounded-lg">
          {{ error }}
        </p>

        <div class="mt-6 text-center">
          <p class="text-dark-600 dark:text-dark-300">
            Pas encore de compte ?
            <router-link to="/register" class="font-bold text-primary-600 dark:text-primary-400 hover:underline">
              S'inscrire
            </router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = ref({
  username: '',
  password: ''
})

const loading = ref(false)
const error = ref('')

const handleLogin = async () => {
  loading.value = true
  error.value = ''
  
  try {
    await authStore.login(form.value)
    router.push('/')
  } catch (err) {
    error.value = err.response?.data?.detail || 'Erreur de connexion. Vérifiez vos identifiants.'
  } finally {
    loading.value = false
  }
}
</script>