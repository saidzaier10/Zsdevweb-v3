<template>
  <div class="min-h-screen bg-white flex items-center justify-center py-16">
    <div class="container mx-auto px-4 max-w-md">
      <div class="border-2 border-black p-8">
        <h1 class="text-4xl font-bold mb-8 text-center">Inscription</h1>
        
        <form @submit.prevent="handleRegister" class="space-y-4">
          <div>
            <label class="block font-bold mb-2">Nom d'utilisateur *</label>
            <input 
              v-model="form.username" 
              type="text" 
              required 
              class="w-full border-2 border-black p-3"
              placeholder="Choisissez un nom d'utilisateur"
            >
          </div>
          
          <div>
            <label class="block font-bold mb-2">Email *</label>
            <input 
              v-model="form.email" 
              type="email" 
              required 
              class="w-full border-2 border-black p-3"
              placeholder="votre@email.com"
            >
          </div>

          <div>
            <label class="block font-bold mb-2">Téléphone</label>
            <input 
              v-model="form.phone" 
              type="tel" 
              class="w-full border-2 border-black p-3"
              placeholder="+33 X XX XX XX XX"
            >
          </div>

          <div>
            <label class="block font-bold mb-2">Entreprise</label>
            <input 
              v-model="form.company_name" 
              type="text" 
              class="w-full border-2 border-black p-3"
              placeholder="Nom de votre entreprise"
            >
          </div>
          
          <div>
            <label class="block font-bold mb-2">Mot de passe *</label>
            <input 
              v-model="form.password" 
              type="password" 
              required 
              class="w-full border-2 border-black p-3"
              placeholder="Choisissez un mot de passe"
            >
          </div>

          <div>
            <label class="block font-bold mb-2">Confirmer le mot de passe *</label>
            <input 
              v-model="form.password2" 
              type="password" 
              required 
              class="w-full border-2 border-black p-3"
              placeholder="Confirmez votre mot de passe"
            >
          </div>

          <button 
            type="submit" 
            :disabled="loading"
            class="bg-black text-white px-8 py-3 font-bold hover:bg-gray-800 transition w-full disabled:bg-gray-400"
          >
            {{ loading ? 'Inscription...' : "S'inscrire" }}
          </button>
        </form>

        <p v-if="error" class="mt-4 text-red-600 font-bold text-center">{{ error }}</p>

        <div class="mt-6 text-center">
          <p class="text-gray-600">
            Déjà un compte ?
            <router-link to="/login" class="font-bold text-black hover:underline">
              Se connecter
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
  email: '',
  phone: '',
  company_name: '',
  password: '',
  password2: ''
})

const loading = ref(false)
const error = ref('')

const handleRegister = async () => {
  if (form.value.password !== form.value.password2) {
    error.value = 'Les mots de passe ne correspondent pas.'
    return
  }

  loading.value = true
  error.value = ''
  
  try {
    await authStore.register(form.value)
    router.push('/')
  } catch (err) {
    error.value = err.response?.data?.username?.[0] || 
                  err.response?.data?.email?.[0] || 
                  err.response?.data?.password?.[0] ||
                  "Erreur lors de l'inscription. Vérifiez vos informations."
  } finally {
    loading.value = false
  }
}
</script>