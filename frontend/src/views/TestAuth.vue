<!--
  ⚠️ PAGE DE TEST - DÉVELOPPEMENT UNIQUEMENT
  Cette page est utilisée uniquement pour tester et déboguer l'authentification.
  Elle ne doit PAS être accessible en production.
  Pour la désactiver, la supprimer de router/index.js
-->
<template>
  <div class="min-h-screen bg-gray-50 dark:bg-dark-900 py-12">
    <div class="container mx-auto px-4 max-w-4xl">
      <h1 class="text-3xl font-bold mb-8">🔍 Test d'Authentification (DEV ONLY)</h1>

      <!-- Info localStorage -->
      <div class="bg-white dark:bg-dark-800 rounded-lg shadow p-6 mb-6">
        <h2 class="text-xl font-semibold mb-4">📦 LocalStorage</h2>
        <div class="space-y-2">
          <div>
            <strong>accessToken:</strong>
            <code class="ml-2 text-sm bg-gray-100 dark:bg-dark-700 px-2 py-1 rounded">
              {{ accessToken ? accessToken.substring(0, 50) + '...' : 'ABSENT' }}
            </code>
          </div>
          <div>
            <strong>refreshToken:</strong>
            <code class="ml-2 text-sm bg-gray-100 dark:bg-dark-700 px-2 py-1 rounded">
              {{ refreshToken ? refreshToken.substring(0, 50) + '...' : 'ABSENT' }}
            </code>
          </div>
          <div v-if="tokenPayload">
            <strong>User ID:</strong> {{ tokenPayload.user_id }}
          </div>
          <div v-if="tokenPayload">
            <strong>Expire:</strong> {{ new Date(tokenPayload.exp * 1000).toLocaleString() }}
          </div>
          <div v-if="tokenPayload">
            <strong>Expiré?</strong>
            <span :class="isExpired ? 'text-red-600' : 'text-green-600'">
              {{ isExpired ? 'OUI ⚠️' : 'NON ✅' }}
            </span>
          </div>
        </div>
      </div>

      <!-- Info Store Auth -->
      <div class="bg-white dark:bg-dark-800 rounded-lg shadow p-6 mb-6">
        <h2 class="text-xl font-semibold mb-4">👤 Auth Store (Pinia)</h2>
        <div class="space-y-2">
          <div><strong>isAuthenticated:</strong> {{ authStore.isAuthenticated ? 'OUI ✅' : 'NON ❌' }}</div>
          <div><strong>Username:</strong> {{ authStore.user?.username || 'Non défini' }}</div>
          <div><strong>Email:</strong> {{ authStore.user?.email || 'Non défini' }}</div>
          <div><strong>is_staff:</strong> {{ authStore.user?.is_staff ? 'OUI (Admin)' : 'NON' }}</div>
        </div>
      </div>

      <!-- Test API -->
      <div class="bg-white dark:bg-dark-800 rounded-lg shadow p-6 mb-6">
        <h2 class="text-xl font-semibold mb-4">🔌 Test API</h2>
        <button
          @click="testAPI"
          :disabled="loading"
          class="px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg font-medium transition-colors disabled:opacity-50"
        >
          {{ loading ? 'Chargement...' : 'Tester /api/quotes/quotes/my-quotes/' }}
        </button>

        <div v-if="apiResponse" class="mt-4">
          <div v-if="apiSuccess" class="p-4 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded">
            <p class="text-green-800 dark:text-green-200">
              ✅ SUCCESS! {{ apiResponse.length }} devis récupérés
            </p>
          </div>
          <div v-else class="p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded">
            <p class="text-red-800 dark:text-red-200">
              ❌ ERREUR: {{ apiError }}
            </p>
          </div>
        </div>
      </div>

      <!-- Actions -->
      <div class="bg-white dark:bg-dark-800 rounded-lg shadow p-6">
        <h2 class="text-xl font-semibold mb-4">⚙️ Actions</h2>
        <div class="flex gap-4">
          <button
            @click="refreshData"
            class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors"
          >
            🔄 Rafraîchir
          </button>
          <button
            @click="clearLocalStorage"
            class="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg font-medium transition-colors"
          >
            🗑️ Vider localStorage
          </button>
          <router-link
            to="/login"
            class="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg font-medium transition-colors inline-block"
          >
            🔑 Aller au Login
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { getMyQuotes } from '../api/quotes'

const authStore = useAuthStore()
const accessToken = ref(null)
const refreshToken = ref(null)
const tokenPayload = ref(null)
const loading = ref(false)
const apiResponse = ref(null)
const apiSuccess = ref(false)
const apiError = ref(null)

const isExpired = computed(() => {
  if (!tokenPayload.value) return false
  return tokenPayload.value.exp * 1000 < Date.now()
})

const loadData = () => {
  accessToken.value = localStorage.getItem('accessToken')
  refreshToken.value = localStorage.getItem('refreshToken')

  if (accessToken.value) {
    try {
      const parts = accessToken.value.split('.')
      if (parts.length === 3) {
        tokenPayload.value = JSON.parse(atob(parts[1]))
      }
    } catch (e) {
      console.error('Erreur décodage token:', e)
    }
  }
}

const testAPI = async () => {
  loading.value = true
  apiResponse.value = null
  apiSuccess.value = false
  apiError.value = null

  try {
    const response = await getMyQuotes()

    if (Array.isArray(response.data)) {
      apiResponse.value = response.data
      apiSuccess.value = true
    } else if (response.data?.results) {
      apiResponse.value = response.data.results
      apiSuccess.value = true
    }
  } catch (error) {
    apiSuccess.value = false
    apiError.value = error.response?.data?.detail || error.message
  } finally {
    loading.value = false
  }
}

const refreshData = () => {
  loadData()
}

const clearLocalStorage = () => {
  if (confirm('Êtes-vous sûr de vouloir vider le localStorage ?')) {
    localStorage.clear()
    authStore.clearAuth()
    loadData()
  }
}

onMounted(() => {
  loadData()
})
</script>
