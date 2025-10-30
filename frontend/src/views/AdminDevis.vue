<template>
  <div class="admin-devis-container">
    <div class="container mx-auto px-4 py-8">
      <div class="max-w-7xl mx-auto">
        <!-- En-tête -->
        <div class="mb-8">
          <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-2">Administration des devis</h1>
          <p class="text-gray-600 dark:text-gray-400">Gérez tous les devis de votre entreprise</p>
        </div>

        <!-- Statistiques -->
        <div v-if="statistics" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm text-gray-600 dark:text-gray-400">Total devis</p>
                <p class="text-2xl font-bold text-gray-900 dark:text-white mt-1">{{ statistics.total_quotes }}</p>
              </div>
              <div class="p-3 bg-indigo-100 dark:bg-indigo-900 rounded-full">
                <svg class="w-6 h-6 text-indigo-600 dark:text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
            </div>
          </div>

          <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm text-gray-600 dark:text-gray-400">Devis acceptés</p>
                <p class="text-2xl font-bold text-green-600 dark:text-green-400 mt-1">{{ statistics.accepted_quotes }}</p>
              </div>
              <div class="p-3 bg-green-100 dark:bg-green-900 rounded-full">
                <svg class="w-6 h-6 text-green-600 dark:text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>
            <p class="text-xs text-gray-500 dark:text-gray-400 mt-2">
              Taux: {{ statistics.total_quotes > 0 ? ((statistics.accepted_quotes / statistics.total_quotes) * 100).toFixed(1) : 0 }}%
            </p>
          </div>

          <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm text-gray-600 dark:text-gray-400">En attente</p>
                <p class="text-2xl font-bold text-blue-600 dark:text-blue-400 mt-1">{{ statistics.pending_quotes }}</p>
              </div>
              <div class="p-3 bg-blue-100 dark:bg-blue-900 rounded-full">
                <svg class="w-6 h-6 text-blue-600 dark:text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>
          </div>

          <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm text-gray-600 dark:text-gray-400">Revenu total</p>
                <p class="text-2xl font-bold text-indigo-600 dark:text-indigo-400 mt-1">{{ formatPrice(statistics.total_revenue) }} €</p>
              </div>
              <div class="p-3 bg-indigo-100 dark:bg-indigo-900 rounded-full">
                <svg class="w-6 h-6 text-indigo-600 dark:text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>
          </div>
        </div>

        <!-- Filtres et recherche -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-6">
          <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Recherche</label>
              <input
                v-model="filters.search"
                type="text"
                placeholder="Numéro, client..."
                class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Statut</label>
              <select
                v-model="filters.status"
                class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              >
                <option value="">Tous</option>
                <option value="draft">Brouillon</option>
                <option value="sent">Envoyé</option>
                <option value="viewed">Consulté</option>
                <option value="accepted">Accepté</option>
                <option value="rejected">Refusé</option>
                <option value="expired">Expiré</option>
              </select>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Trier par</label>
              <select
                v-model="filters.sortBy"
                class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              >
                <option value="-created_at">Plus récent</option>
                <option value="created_at">Plus ancien</option>
                <option value="-total_ttc">Montant (décroissant)</option>
                <option value="total_ttc">Montant (croissant)</option>
                <option value="client_name">Client (A-Z)</option>
              </select>
            </div>

            <div class="flex items-end">
              <button
                @click="applyFilters"
                class="w-full px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
              >
                Appliquer
              </button>
            </div>
          </div>
        </div>

        <!-- Tableau des devis -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden">
          <!-- Loader -->
          <div v-if="loading" class="flex justify-center items-center py-12">
            <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-600"></div>
          </div>

          <!-- Liste vide -->
          <div v-else-if="quotes.length === 0" class="text-center py-12">
            <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <h3 class="mt-2 text-sm font-medium text-gray-900 dark:text-white">Aucun devis</h3>
            <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">Aucun devis ne correspond à vos critères.</p>
          </div>

          <!-- Tableau -->
          <div v-else class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
              <thead class="bg-gray-50 dark:bg-gray-900">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Numéro
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Client
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Date
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Montant
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Statut
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                <tr v-for="quote in quotes" :key="quote.id" class="hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="text-sm font-medium text-gray-900 dark:text-white">{{ quote.quote_number }}</div>
                  </td>
                  <td class="px-6 py-4">
                    <div class="text-sm text-gray-900 dark:text-white">{{ quote.client_name }}</div>
                    <div class="text-sm text-gray-500 dark:text-gray-400">{{ quote.client_email }}</div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="text-sm text-gray-900 dark:text-white">{{ formatDate(quote.created_at) }}</div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="text-sm font-semibold text-gray-900 dark:text-white">{{ formatPrice(quote.total_ttc) }} €</div>
                    <div v-if="quote.monthly_subscription_total > 0" class="text-xs text-indigo-600 dark:text-indigo-400">
                      + {{ formatPrice(quote.monthly_subscription_total) }} €/mois
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span :class="getStatusBadgeClass(quote.status)" class="px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full">
                      {{ getStatusLabel(quote.status) }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm">
                    <div class="flex gap-2">
                      <button
                        @click="viewQuote(quote.id)"
                        class="text-indigo-600 dark:text-indigo-400 hover:text-indigo-900 dark:hover:text-indigo-300"
                        title="Voir"
                      >
                        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                        </svg>
                      </button>
                      <button
                        @click="duplicateQuote(quote.id)"
                        class="text-blue-600 dark:text-blue-400 hover:text-blue-900 dark:hover:text-blue-300"
                        title="Dupliquer"
                      >
                        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                        </svg>
                      </button>
                      <button
                        @click="downloadPDF(quote.id)"
                        class="text-green-600 dark:text-green-400 hover:text-green-900 dark:hover:text-green-300"
                        title="Télécharger PDF"
                      >
                        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                      </button>
                      <button
                        v-if="quote.status === 'draft'"
                        @click="deleteQuote(quote.id)"
                        class="text-red-600 dark:text-red-400 hover:text-red-900 dark:hover:text-red-300"
                        title="Supprimer"
                      >
                        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Pagination -->
          <div v-if="pagination.total > 0" class="bg-white dark:bg-gray-800 px-4 py-3 border-t border-gray-200 dark:border-gray-700 sm:px-6">
            <div class="flex items-center justify-between">
              <div class="text-sm text-gray-700 dark:text-gray-300">
                Affichage de <span class="font-medium">{{ (pagination.current - 1) * pagination.pageSize + 1 }}</span>
                à <span class="font-medium">{{ Math.min(pagination.current * pagination.pageSize, pagination.total) }}</span>
                sur <span class="font-medium">{{ pagination.total }}</span> résultats
              </div>
              <div class="flex gap-2">
                <button
                  @click="goToPage(pagination.current - 1)"
                  :disabled="pagination.current === 1"
                  class="px-3 py-1 border border-gray-300 dark:border-gray-600 rounded-lg text-sm disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300"
                >
                  Précédent
                </button>
                <button
                  @click="goToPage(pagination.current + 1)"
                  :disabled="pagination.current * pagination.pageSize >= pagination.total"
                  class="px-3 py-1 border border-gray-300 dark:border-gray-600 rounded-lg text-sm disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300"
                >
                  Suivant
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
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getAllQuotes, getQuoteStatistics, duplicateQuote as duplicateQuoteAPI, downloadQuotePDF, deleteQuote as deleteQuoteAPI } from '@/api/quotes'
import { useToastStore } from '@/stores/toast'

const router = useRouter()
const toast = useToastStore()

const quotes = ref([])
const statistics = ref(null)
const loading = ref(true)

const filters = ref({
  search: '',
  status: '',
  sortBy: '-created_at'
})

const pagination = ref({
  current: 1,
  pageSize: 10,
  total: 0
})

// Methods
const fetchQuotes = async () => {
  try {
    loading.value = true
    const params = {
      page: pagination.value.current,
      page_size: pagination.value.pageSize,
      ordering: filters.value.sortBy
    }

    if (filters.value.search) {
      params.search = filters.value.search
    }

    if (filters.value.status) {
      params.status = filters.value.status
    }

    const response = await getAllQuotes(params)
    quotes.value = response.data.results || response.data
    pagination.value.total = response.data.count || quotes.value.length
  } catch (err) {
    console.error('Erreur lors du chargement des devis:', err)
    toast.error('Erreur', 'Impossible de charger les devis')
  } finally {
    loading.value = false
  }
}

const fetchStatistics = async () => {
  try {
    const response = await getQuoteStatistics()
    statistics.value = response.data
  } catch (err) {
    console.error('Erreur lors du chargement des statistiques:', err)
  }
}

const applyFilters = () => {
  pagination.value.current = 1
  fetchQuotes()
}

const goToPage = (page) => {
  pagination.value.current = page
  fetchQuotes()
}

const viewQuote = (id) => {
  router.push(`/devis/${id}`)
}

const duplicateQuote = async (id) => {
  try {
    const response = await duplicateQuoteAPI(id)
    toast.success('Devis dupliqué', 'Le devis a été dupliqué avec succès')
    router.push(`/devis/${response.data.id}`)
  } catch (err) {
    console.error('Erreur lors de la duplication:', err)
    toast.error('Erreur', 'Impossible de dupliquer le devis')
  }
}

const downloadPDF = async (id) => {
  try {
    const quote = quotes.value.find(q => q.id === id)
    const response = await downloadQuotePDF(id)
    
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `${quote.quote_number}.pdf`)
    document.body.appendChild(link)
    link.click()
    link.remove()
    window.URL.revokeObjectURL(url)
    
    toast.success('Téléchargement réussi', 'Le PDF a été téléchargé')
  } catch (err) {
    console.error('Erreur lors du téléchargement:', err)
    toast.error('Erreur', 'Impossible de télécharger le PDF')
  }
}

const deleteQuote = async (id) => {
  if (!confirm('Êtes-vous sûr de vouloir supprimer ce devis ?')) {
    return
  }

  try {
    await deleteQuoteAPI(id)
    toast.success('Devis supprimé', 'Le devis a été supprimé avec succès')
    fetchQuotes()
    fetchStatistics()
  } catch (err) {
    console.error('Erreur lors de la suppression:', err)
    toast.error('Erreur', 'Impossible de supprimer le devis')
  }
}

const formatDate = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('fr-FR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  }).format(date)
}

const formatPrice = (price) => {
  if (!price) return '0.00'
  return parseFloat(price).toFixed(2)
}

const getStatusLabel = (status) => {
  const labels = {
    'draft': 'Brouillon',
    'sent': 'Envoyé',
    'viewed': 'Consulté',
    'accepted': 'Accepté',
    'rejected': 'Refusé',
    'expired': 'Expiré'
  }
  return labels[status] || status
}

const getStatusBadgeClass = (status) => {
  const classes = {
    'draft': 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300',
    'sent': 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300',
    'viewed': 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300',
    'accepted': 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300',
    'rejected': 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300',
    'expired': 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-300'
  }
  return classes[status] || classes.draft
}

onMounted(() => {
  fetchQuotes()
  fetchStatistics()
})
</script>

<style scoped>
.admin-devis-container {
  min-height: calc(100vh - 64px);
  background-color: #f9fafb;
}

.dark .admin-devis-container {
  background-color: #111827;
}
</style>