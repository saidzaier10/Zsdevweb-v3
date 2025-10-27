<template>
  <div class="min-h-screen bg-white flex items-center justify-center py-16">
    <div class="container mx-auto px-4 max-w-md">
      <div class="border-2 border-black p-8">
        <h1 class="text-4xl font-bold mb-8 text-center">Connexion</h1>
        
        <form @submit.prevent="handleLogin" class="space-y-4">
          <div>
            <label class="block font-bold mb-2">Nom d'utilisateur *</label>
            <input 
              v-model="form.username" 
              type="text" 
              required 
              class="w-full border-2 border-black p-3"
              placeholder="Votre nom d'utilisateur"
            >
          </div>
          
          <div>
            <label class="block font-bold mb-2">Mot de passe *</label>
            <input 
              v-model="form.password" 
              type="password" 
              required 
              class="w-full border-2 border-black p-3"
              placeholder="Votre mot de passe"
            >
          </div>

          <button 
            type="submit" 
            :disabled="loading"
            class="bg-black text-white px-8 py-3 font-bold hover:bg-gray-800 transition w-full disabled:bg-gray-400"
          >
            {{ loading ? 'Connexion...' : 'Se connecter' }}
          </button>
        </form>

        <p v-if="error" class="mt-4 text-red-600 font-bold text-center">{{ error }}</p>

        <div class="mt-6 text-center">
          <p class="text-gray-600">
            Pas encore de compte ?
            <router-link to="/register" class="font-bold text-black hover:underline">
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