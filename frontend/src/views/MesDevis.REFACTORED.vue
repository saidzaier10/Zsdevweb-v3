<template>
  <div class="min-h-screen bg-gray-50 dark:bg-dark-900 py-12 transition-colors duration-200">
    <div class="container mx-auto px-4 lg:px-8">
      <!-- En-tête -->
      <div class="mb-8">
        <h1 class="text-4xl font-display font-bold gradient-text mb-2">Mes Devis</h1>
        <p class="text-dark-600 dark:text-dark-300">Suivez l'évolution de vos demandes de devis en temps réel</p>
      </div>

      <!-- Statistiques -->
      <ClientQuoteStats v-if="!loading && quotes.length > 0" :quotes="quotes" />

      <!-- Filtres -->
      <div class="bg-white dark:bg-dark-800 rounded-xl shadow-sm p-4 sm:p-6 mb-6 border border-gray-200 dark:border-dark-700">
        <div class="flex flex-wrap gap-2 sm:gap-3">
          <button
            v-for="filter in filters"
            :key="filter.status"
            @click="filterStatus = filter.status"
            :class="[
              'px-3 sm:px-4 py-2 rounded-lg font-medium transition-all text-sm sm:text-base',
              filterStatus === filter.status
                ? 'bg-primary-600 text-white shadow-lg'
                : 'bg-gray-100 dark:bg-dark-700 text-dark-700 dark:text-dark-200 hover:bg-gray-200 dark:hover:bg-dark-600'
            ]"
          >
            {{ filter.label }} <span class="hidden sm:inline">({{ filter.count }})</span>
          </button>
        </div>
      </div>

      <!-- Chargement -->
      <div v-if="loading" class="text-center py-16">
        <div class="inline-block animate-spin rounded-full h-16 w-16 border-4 border-primary-600 border-t-transparent"></div>
        <p class="mt-4 text-dark-600 dark:text-dark-300 font-medium">Chargement de vos devis...</p>
      </div>

      <!-- Liste vide -->
      <div v-else-if="filteredQuotes.length === 0" class="bg-white dark:bg-dark-800 rounded-xl shadow-sm p-12 text-center border border-gray-200 dark:border-dark-700">
        <div class="max-w-md mx-auto">
          <div class="mb-4 inline-flex items-center justify-center w-20 h-20 bg-primary-100 dark:bg-primary-900/30 rounded-full">
            <svg class="w-10 h-10 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
            </svg>
          </div>
          <h3 class="text-2xl font-bold text-dark-800 dark:text-dark-100 mb-2">Aucun devis trouvé</h3>
          <p class="text-dark-600 dark:text-dark-300 mb-6">
            {{ filterStatus ? 'Aucun devis avec ce statut pour le moment.' : 'Commencez par créer votre premier devis!' }}
          </p>
          <router-link to="/devis" class="inline-flex items-center gap-2 bg-gradient-to-r from-primary-600 to-secondary-500 text-white px-6 py-3 rounded-lg font-semibold hover:from-primary-700 hover:to-secondary-600 transition-all shadow-lg">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
            </svg>
            Créer un devis
          </router-link>
        </div>
      </div>

      <!-- Grille de cartes de devis -->
      <div v-else class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div
          v-for="quote in filteredQuotes"
          :key="quote.id"
          class="bg-white dark:bg-dark-800 rounded-xl shadow-sm hover:shadow-xl transition-all duration-300 border border-gray-200 dark:border-dark-700 overflow-hidden group cursor-pointer"
          @click="openQuoteDetails(quote)"
        >
          <!-- En-tête de la carte -->
          <div class="p-6 border-b border-gray-100 dark:border-dark-700">
            <div class="flex items-start justify-between mb-3">
              <div class="flex-1">
                <div class="flex items-center gap-2 mb-2">
                  <h3 class="text-xl font-bold text-dark-800 dark:text-dark-100 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors">
                    {{ quote.project_type?.name || 'N/A' }}
                  </h3>
                  <span v-if="quote.discount_amount && quote.discount_amount > 0" class="px-2 py-0.5 bg-green-100 dark:bg-green-900/20 text-green-700 dark:text-green-400 text-xs font-bold rounded-full">
                    -{{ Math.round((quote.discount_amount / quote.total_price) * 100) }}%
                  </span>
                </div>
                <p class="text-sm text-dark-500 dark:text-dark-400 font-mono">
                  #{{ quote.quote_number }}
                </p>
              </div>
              <StatusBadge :status="quote.status" />
            </div>

            <!-- Barre de progression -->
            <div class="mt-4">
              <div class="flex items-center justify-between text-xs text-dark-500 dark:text-dark-400 mb-1">
                <span>Progression</span>
                <span class="font-semibold">{{ getProgressPercentage(quote) }}%</span>
              </div>
              <div class="w-full bg-gray-200 dark:bg-dark-700 rounded-full h-2 overflow-hidden">
                <div
                  :class="[
                    'h-full rounded-full transition-all duration-500',
                    quote.status === 'accepted' ? 'bg-gradient-to-r from-green-500 to-green-600' :
                    quote.status === 'viewed' ? 'bg-gradient-to-r from-indigo-500 to-purple-600' :
                    quote.status === 'sent' ? 'bg-gradient-to-r from-blue-500 to-blue-600' :
                    'bg-gradient-to-r from-gray-400 to-gray-500'
                  ]"
                  :style="{ width: `${getProgressPercentage(quote)}%` }"
                ></div>
              </div>
            </div>
          </div>

          <!-- Corps de la carte -->
          <div class="p-6">
            <!-- Informations clés -->
            <div class="grid grid-cols-2 gap-4 mb-4">
              <div class="flex items-center gap-2 text-sm text-dark-600 dark:text-dark-300">
                <svg class="w-4 h-4 text-dark-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                </svg>
                <span>{{ formatShortDate(quote.created_at) }}</span>
              </div>
              <div class="flex items-center gap-2 text-sm text-dark-600 dark:text-dark-300">
                <svg class="w-4 h-4 text-dark-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                <span class="font-semibold">{{ formatAmount(quote.total_price) }}</span>
              </div>
            </div>

            <!-- Boutons d'action -->
            <div class="flex gap-2">
              <button
                v-if="quote.status === 'draft'"
                @click.stop="handleSendQuote(quote.id)"
                :disabled="sending === quote.id"
                class="flex-1 flex items-center justify-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-all disabled:opacity-50"
              >
                <svg v-if="sending !== quote.id" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                </svg>
                <span>{{ sending === quote.id ? 'Envoi...' : 'Envoyer' }}</span>
              </button>

              <button
                @click.stop="openQuoteDetails(quote)"
                class="flex-1 flex items-center justify-center gap-2 px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg font-medium transition-all"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                </svg>
                Voir
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Modal de détails (simplifié) -->
      <!-- TODO: Extraire dans un composant séparé -->
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getMyQuotes, sendQuote as sendQuoteAPI, downloadQuotePDF } from '../api/quotes'
import ClientQuoteStats from '../components/ClientQuoteStats.vue'
import QuoteTimeline from '../components/QuoteTimeline.vue'
// NOUVEAUX IMPORTS - Utilitaires centralisés
import { formatShortDate, formatAmount } from '@/utils/formatters'
import { QUOTE_STATUS_LABELS, QUOTE_STATUSES } from '@/utils/constants'
import { useApi } from '@/composables/useApi'
import StatusBadge from '@/components/ui/StatusBadge.vue' // À créer

const router = useRouter()

// ✅ AMÉLIORATION 1: Utiliser useApi au lieu de gérer loading/errors manuellement
const { loading, get, callApi, handleSuccess, handleError } = useApi()

const quotes = ref([])
const filterStatus = ref(null)
const sending = ref(null)
const downloading = ref(null)
const selectedQuote = ref(null)

// ✅ AMÉLIORATION 2: Computed pour les filtres (évite duplication)
const filters = computed(() => [
  {
    status: null,
    label: 'Tous',
    count: quotes.value.length
  },
  {
    status: QUOTE_STATUSES.DRAFT,
    label: QUOTE_STATUS_LABELS[QUOTE_STATUSES.DRAFT],
    count: countByStatus(QUOTE_STATUSES.DRAFT)
  },
  {
    status: QUOTE_STATUSES.SENT,
    label: QUOTE_STATUS_LABELS[QUOTE_STATUSES.SENT],
    count: countByStatus(QUOTE_STATUSES.SENT)
  },
  {
    status: QUOTE_STATUSES.ACCEPTED,
    label: QUOTE_STATUS_LABELS[QUOTE_STATUSES.ACCEPTED],
    count: countByStatus(QUOTE_STATUSES.ACCEPTED)
  }
])

const filteredQuotes = computed(() => {
  if (!Array.isArray(quotes.value)) return []
  if (filterStatus.value === null) return quotes.value
  return quotes.value.filter(q => q.status === filterStatus.value)
})

const countByStatus = (status) => {
  if (!Array.isArray(quotes.value)) return 0
  return quotes.value.filter(q => q.status === status).length
}

// ✅ AMÉLIORATION 3: Plus besoin de getStatusLabel et getStatusClass
// Ils sont dans constants.js et utilisés par StatusBadge

const getProgressPercentage = (quote) => {
  const statusProgress = {
    [QUOTE_STATUSES.DRAFT]: 20,
    [QUOTE_STATUSES.SENT]: 40,
    [QUOTE_STATUSES.VIEWED]: 60,
    [QUOTE_STATUSES.ACCEPTED]: 100,
    [QUOTE_STATUSES.REJECTED]: 100,
    [QUOTE_STATUSES.EXPIRED]: 100
  }
  return statusProgress[quote.status] || 0
}

const openQuoteDetails = (quote) => {
  selectedQuote.value = quote
}

const closeQuoteDetails = () => {
  selectedQuote.value = null
}

const goToSignature = (quote) => {
  router.push(`/signature/${quote.signature_token}`)
}

// ✅ AMÉLIORATION 4: Gestion d'erreur simplifiée avec useApi
const handleSendQuote = async (quoteId) => {
  try {
    sending.value = quoteId
    await callApi(
      () => sendQuoteAPI(quoteId),
      {
        successMessage: 'Devis envoyé avec succès par email',
        errorMessage: 'Erreur lors de l\'envoi du devis'
      }
    )
    await loadQuotes()
  } finally {
    sending.value = null
  }
}

// ✅ AMÉLIORATION 5: Download PDF simplifié
const handleDownloadPDF = async (quoteId, quoteNumber) => {
  try {
    downloading.value = quoteId
    const response = await callApi(
      () => downloadQuotePDF(quoteId),
      {
        successMessage: 'PDF téléchargé avec succès',
        errorMessage: 'Erreur lors du téléchargement du PDF'
      }
    )

    // Logique de téléchargement
    const blob = new Blob([response.data], { type: 'application/pdf' })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `devis-${quoteNumber}.pdf`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
  } finally {
    downloading.value = null
  }
}

// ✅ AMÉLIORATION 6: Load quotes avec useApi.get
const loadQuotes = async () => {
  try {
    const data = await get(
      () => getMyQuotes(),
      {
        errorMessage: 'Erreur lors du chargement des devis'
      }
    )
    quotes.value = Array.isArray(data) ? data : (data.results || [])
  } catch (error) {
    quotes.value = []
  }
}

onMounted(() => {
  loadQuotes()
})
</script>
