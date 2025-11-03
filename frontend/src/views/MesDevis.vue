<template>
  <div class="min-h-screen bg-gray-50 dark:bg-dark-900 py-12 transition-colors duration-200">
    <div class="container mx-auto px-4 lg:px-8">
      <!-- En-tête -->
      <div class="mb-8">
        <h1 class="text-4xl font-display font-bold gradient-text mb-2">Mes Devis</h1>
        <p class="text-dark-600 dark:text-dark-300">Consultez et gérez vos demandes de devis</p>
      </div>

      <!-- Filtres -->
      <div class="bg-white dark:bg-dark-800 rounded-xl shadow-sm p-6 mb-6 border border-gray-200 dark:border-dark-700">
        <div class="flex flex-wrap gap-3">
          <button
            @click="filterStatus = null"
            :class="[
              'px-4 py-2 rounded-lg font-medium transition-all',
              filterStatus === null
                ? 'bg-primary-600 text-white'
                : 'bg-gray-100 dark:bg-dark-700 text-dark-700 dark:text-dark-200 hover:bg-gray-200 dark:hover:bg-dark-600'
            ]"
          >
            Tous ({{ quotes.length }})
          </button>
          <button
            @click="filterStatus = 'draft'"
            :class="[
              'px-4 py-2 rounded-lg font-medium transition-all',
              filterStatus === 'draft'
                ? 'bg-primary-600 text-white'
                : 'bg-gray-100 dark:bg-dark-700 text-dark-700 dark:text-dark-200 hover:bg-gray-200 dark:hover:bg-dark-600'
            ]"
          >
            Brouillons ({{ countByStatus('draft') }})
          </button>
          <button
            @click="filterStatus = 'sent'"
            :class="[
              'px-4 py-2 rounded-lg font-medium transition-all',
              filterStatus === 'sent'
                ? 'bg-primary-600 text-white'
                : 'bg-gray-100 dark:bg-dark-700 text-dark-700 dark:text-dark-200 hover:bg-gray-200 dark:hover:bg-dark-600'
            ]"
          >
            Envoyés ({{ countByStatus('sent') }})
          </button>
          <button
            @click="filterStatus = 'accepted'"
            :class="[
              'px-4 py-2 rounded-lg font-medium transition-all',
              filterStatus === 'accepted'
                ? 'bg-primary-600 text-white'
                : 'bg-gray-100 dark:bg-dark-700 text-dark-700 dark:text-dark-200 hover:bg-gray-200 dark:hover:bg-dark-600'
            ]"
          >
            Acceptés ({{ countByStatus('accepted') }})
          </button>
          <button
            @click="filterStatus = 'rejected'"
            :class="[
              'px-4 py-2 rounded-lg font-medium transition-all',
              filterStatus === 'rejected'
                ? 'bg-primary-600 text-white'
                : 'bg-gray-100 dark:bg-dark-700 text-dark-700 dark:text-dark-200 hover:bg-gray-200 dark:hover:bg-dark-600'
            ]"
          >
            Refusés ({{ countByStatus('rejected') }})
          </button>
        </div>
      </div>

      <!-- Chargement -->
      <div v-if="loading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        <p class="mt-4 text-dark-600 dark:text-dark-300">Chargement de vos devis...</p>
      </div>

      <!-- Liste vide -->
      <div v-else-if="filteredQuotes.length === 0" class="bg-white dark:bg-dark-800 rounded-xl shadow-sm p-12 text-center border border-gray-200 dark:border-dark-700">
        <svg class="w-16 h-16 mx-auto mb-4 text-gray-400 dark:text-dark-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
        </svg>
        <h3 class="text-xl font-semibold text-dark-700 dark:text-dark-200 mb-2">Aucun devis</h3>
        <p class="text-dark-600 dark:text-dark-300 mb-6">Vous n'avez pas encore de devis{{ filterStatus ? ' avec ce statut' : '' }}.</p>
        <router-link to="/devis" class="btn-primary inline-block">
          Créer un devis
        </router-link>
      </div>

      <!-- Liste des devis -->
      <div v-else class="space-y-4">
        <div
          v-for="quote in filteredQuotes"
          :key="quote.id"
          class="bg-white dark:bg-dark-800 rounded-xl shadow-sm hover:shadow-md transition-all duration-200 border border-gray-200 dark:border-dark-700 overflow-hidden"
        >
          <div class="p-6">
            <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
              <!-- Informations principales -->
              <div class="flex-1">
                <div class="flex items-start justify-between mb-3">
                  <div>
                    <h3 class="text-xl font-semibold text-dark-800 dark:text-dark-100 mb-1">
                      {{ quote.project_type.name }}
                    </h3>
                    <p class="text-sm text-dark-600 dark:text-dark-400">
                      Référence: #{{ quote.quote_number }}
                    </p>
                  </div>
                  <span
                    :class="[
                      'px-3 py-1 rounded-full text-sm font-semibold',
                      getStatusClass(quote.status)
                    ]"
                  >
                    {{ getStatusLabel(quote.status) }}
                  </span>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">
                  <div class="flex items-center text-dark-600 dark:text-dark-300">
                    <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                    </svg>
                    Créé le {{ formatDate(quote.created_at) }}
                  </div>
                  <div class="flex items-center text-dark-600 dark:text-dark-300">
                    <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                    {{ quote.total_price }} €
                  </div>
                  <div class="flex items-center text-dark-600 dark:text-dark-300">
                    <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01"></path>
                    </svg>
                    {{ quote.design_option.name }}
                  </div>
                  <div class="flex items-center text-dark-600 dark:text-dark-300">
                    <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                    </svg>
                    {{ quote.complexity_level.name }}
                  </div>
                </div>

                <!-- Options supplémentaires -->
                <div v-if="quote.supplementary_options.length > 0" class="mt-3 flex flex-wrap gap-2">
                  <span
                    v-for="option in quote.supplementary_options"
                    :key="option.id"
                    class="px-2 py-1 bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-300 rounded text-xs font-medium"
                  >
                    {{ option.name }}
                  </span>
                </div>
              </div>

              <!-- Actions -->
              <div class="flex flex-col gap-2 lg:ml-4">
                <router-link
                  :to="`/devis/${quote.id}`"
                  class="px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg font-medium transition-colors text-center"
                >
                  Voir détails
                </router-link>
                <button
                  v-if="quote.status === 'sent' && quote.signature_token"
                  @click="goToSignature(quote)"
                  class="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg font-medium transition-colors"
                >
                  Signer
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getMyQuotes } from '../api/quotes'
import { useToastStore } from '../stores/toast'

const router = useRouter()
const toastStore = useToastStore()

const quotes = ref([])
const loading = ref(true)
const filterStatus = ref(null)

const filteredQuotes = computed(() => {
  if (filterStatus.value === null) {
    return quotes.value
  }
  return quotes.value.filter(q => q.status === filterStatus.value)
})

const countByStatus = (status) => {
  return quotes.value.filter(q => q.status === status).length
}

const getStatusLabel = (status) => {
  const labels = {
    draft: 'Brouillon',
    sent: 'Envoyé',
    viewed: 'Consulté',
    accepted: 'Accepté',
    rejected: 'Refusé',
    expired: 'Expiré'
  }
  return labels[status] || status
}

const getStatusClass = (status) => {
  const classes = {
    draft: 'bg-gray-100 text-gray-800 dark:bg-gray-900/20 dark:text-gray-400',
    sent: 'bg-blue-100 text-blue-800 dark:bg-blue-900/20 dark:text-blue-400',
    viewed: 'bg-indigo-100 text-indigo-800 dark:bg-indigo-900/20 dark:text-indigo-400',
    accepted: 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400',
    rejected: 'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-400',
    expired: 'bg-gray-100 text-gray-800 dark:bg-gray-900/20 dark:text-gray-400'
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('fr-FR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const goToSignature = (quote) => {
  router.push(`/signature/${quote.signature_token}`)
}

const loadQuotes = async () => {
  try {
    loading.value = true
    const response = await getMyQuotes()
    quotes.value = response.data
  } catch (error) {
    console.error('Erreur lors du chargement des devis:', error)
    toastStore.showToast('Erreur lors du chargement des devis', 'error')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadQuotes()
})
</script>