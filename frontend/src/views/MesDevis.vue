<template>
  <div class="mes-devis-container">
    <div class="container mx-auto px-4 py-8">
      <div class="max-w-6xl mx-auto">
        <!-- En-tête -->
        <div class="mb-8">
          <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-2">Mes devis</h1>
          <p class="text-gray-600 dark:text-gray-400">Consultez et gérez tous vos devis</p>
        </div>

        <!-- Filtres -->
        <div class="mb-6">
          <div class="flex flex-wrap gap-2">
            <button
              v-for="filter in filters"
              :key="filter.value"
              @click="selectedFilter = filter.value"
              :class="[
                'px-4 py-2 rounded-lg font-medium transition-colors',
                selectedFilter === filter.value
                  ? 'bg-indigo-600 text-white'
                  : 'bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 border border-gray-300 dark:border-gray-600 hover:bg-gray-50 dark:hover:bg-gray-700'
              ]"
            >
              {{ filter.label }}
              <span v-if="filter.count !== undefined" class="ml-2 opacity-75">({{ filter.count }})</span>
            </button>
          </div>
        </div>

        <!-- Loader -->
        <div v-if="loading" class="flex justify-center items-center py-12">
          <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-600"></div>
        </div>

        <!-- Liste vide -->
        <div v-else-if="filteredQuotes.length === 0" class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-12 text-center">
          <svg class="mx-auto h-16 w-16 text-gray-400 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">Aucun devis trouvé</h3>
          <p class="text-gray-500 dark:text-gray-400 mb-6">
            {{ selectedFilter === '' ? 'Vous n\'avez aucun devis pour le moment.' : 'Aucun devis ne correspond à ce filtre.' }}
          </p>
          <router-link
            to="/devis"
            class="inline-block px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors font-medium"
          >
            Demander un devis
          </router-link>
        </div>

        <!-- Liste des devis -->
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div
            v-for="quote in filteredQuotes"
            :key="quote.id"
            class="bg-white dark:bg-gray-800 rounded-lg shadow-md hover:shadow-lg transition-shadow overflow-hidden"
          >
            <!-- En-tête de la carte -->
            <div class="p-6 border-b border-gray-200 dark:border-gray-700">
              <div class="flex items-start justify-between mb-2">
                <h3 class="text-lg font-semibold text-gray-900 dark:text-white">{{ quote.quote_number }}</h3>
                <span :class="getStatusBadgeClass(quote.status)" class="px-2 py-1 text-xs font-medium rounded-full">
                  {{ getStatusLabel(quote.status) }}
                </span>
              </div>
              <p class="text-sm text-gray-600 dark:text-gray-400">
                Créé le {{ formatDate(quote.created_at) }}
              </p>
            </div>

            <!-- Corps de la carte -->
            <div class="p-6">
              <div class="space-y-3 mb-4">
                <div v-if="quote.project_type_details">
                  <p class="text-xs text-gray-500 dark:text-gray-400">Type de projet</p>
                  <p class="text-sm text-gray-900 dark:text-white font-medium">{{ quote.project_type_details.name }}</p>
                </div>
                <div>
                  <p class="text-xs text-gray-500 dark:text-gray-400">Montant total TTC</p>
                  <p class="text-2xl font-bold text-indigo-600 dark:text-indigo-400">{{ formatPrice(quote.total_ttc) }} €</p>
                  <p v-if="quote.monthly_subscription_total > 0" class="text-xs text-gray-600 dark:text-gray-400 mt-1">
                    + {{ formatPrice(quote.monthly_subscription_total) }} €/mois
                  </p>
                </div>
                <div v-if="quote.valid_until">
                  <p class="text-xs text-gray-500 dark:text-gray-400">Valide jusqu'au</p>
                  <p class="text-sm text-gray-900 dark:text-white">{{ formatDate(quote.valid_until) }}</p>
                  <p v-if="isExpiringSoon(quote.valid_until)" class="text-xs text-orange-600 dark:text-orange-400 mt-1">
                    ⚠️ Expire bientôt
                  </p>
                </div>
              </div>

              <!-- Actions -->
              <div class="flex flex-col gap-2">
                <button
                  @click="viewQuote(quote.id)"
                  class="w-full px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors text-sm font-medium"
                >
                  Voir le détail
                </button>
                <div class="flex gap-2">
                  <button
                    v-if="canSign(quote)"
                    @click="goToSignature(quote)"
                    class="flex-1 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors text-sm font-medium"
                  >
                    Signer
                  </button>
                  <button
                    @click="downloadPDF(quote.id)"
                    class="flex-1 px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors text-sm font-medium"
                  >
                    PDF
                  </button>
                </div>
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
import { getMyQuotes, downloadQuotePDF } from '@/api/quotes'
import { useToastStore } from '@/stores/toast'

const router = useRouter()
const toast = useToastStore()

const quotes = ref([])
const loading = ref(true)
const selectedFilter = ref('')

const filters = computed(() => [
  { label: 'Tous', value: '', count: quotes.value.length },
  { label: 'Brouillon', value: 'draft', count: quotes.value.filter(q => q.status === 'draft').length },
  { label: 'Envoyé', value: 'sent', count: quotes.value.filter(q => q.status === 'sent').length },
  { label: 'Consulté', value: 'viewed', count: quotes.value.filter(q => q.status === 'viewed').length },
  { label: 'Accepté', value: 'accepted', count: quotes.value.filter(q => q.status === 'accepted').length },
  { label: 'Refusé', value: 'rejected', count: quotes.value.filter(q => q.status === 'rejected').length },
  { label: 'Expiré', value: 'expired', count: quotes.value.filter(q => q.status === 'expired').length },
])

const filteredQuotes = computed(() => {
  if (selectedFilter.value === '') {
    return quotes.value
  }
  return quotes.value.filter(quote => quote.status === selectedFilter.value)
})

// Methods
const fetchQuotes = async () => {
  try {
    loading.value = true
    const response = await getMyQuotes()
    quotes.value = response.data.results || response.data
  } catch (err) {
    console.error('Erreur lors du chargement des devis:', err)
    toast.error('Erreur', 'Impossible de charger vos devis')
  } finally {
    loading.value = false
  }
}

const viewQuote = (id) => {
  router.push(`/devis/${id}`)
}

const canSign = (quote) => {
  return ['sent', 'viewed'].includes(quote.status) && !isExpired(quote.valid_until)
}

const goToSignature = (quote) => {
  router.push(`/signature/${quote.public_token}`)
}

const isExpired = (validUntil) => {
  return new Date(validUntil) < new Date()
}

const isExpiringSoon = (validUntil) => {
  const validDate = new Date(validUntil)
  const today = new Date()
  const diffTime = validDate - today
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  return diffDays <= 7 && diffDays > 0
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

const formatDate = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('fr-FR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
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
})
</script>

<style scoped>
.mes-devis-container {
  min-height: calc(100vh - 64px);
  background-color: #f9fafb;
}

.dark .mes-devis-container {
  background-color: #111827;
}
</style>