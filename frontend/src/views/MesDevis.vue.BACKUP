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
            @click="filterStatus = null"
            :class="[
              'px-3 sm:px-4 py-2 rounded-lg font-medium transition-all text-sm sm:text-base',
              filterStatus === null
                ? 'bg-primary-600 text-white shadow-lg'
                : 'bg-gray-100 dark:bg-dark-700 text-dark-700 dark:text-dark-200 hover:bg-gray-200 dark:hover:bg-dark-600'
            ]"
          >
            Tous <span class="hidden sm:inline">({{ quotes.length }})</span>
          </button>
          <button
            @click="filterStatus = 'draft'"
            :class="[
              'px-3 sm:px-4 py-2 rounded-lg font-medium transition-all text-sm sm:text-base',
              filterStatus === 'draft'
                ? 'bg-primary-600 text-white shadow-lg'
                : 'bg-gray-100 dark:bg-dark-700 text-dark-700 dark:text-dark-200 hover:bg-gray-200 dark:hover:bg-dark-600'
            ]"
          >
            Brouillons <span class="hidden sm:inline">({{ countByStatus('draft') }})</span>
          </button>
          <button
            @click="filterStatus = 'sent'"
            :class="[
              'px-3 sm:px-4 py-2 rounded-lg font-medium transition-all text-sm sm:text-base',
              filterStatus === 'sent'
                ? 'bg-primary-600 text-white shadow-lg'
                : 'bg-gray-100 dark:bg-dark-700 text-dark-700 dark:text-dark-200 hover:bg-gray-200 dark:hover:bg-dark-600'
            ]"
          >
            Envoyés <span class="hidden sm:inline">({{ countByStatus('sent') }})</span>
          </button>
          <button
            @click="filterStatus = 'accepted'"
            :class="[
              'px-3 sm:px-4 py-2 rounded-lg font-medium transition-all text-sm sm:text-base',
              filterStatus === 'accepted'
                ? 'bg-primary-600 text-white shadow-lg'
                : 'bg-gray-100 dark:bg-dark-700 text-dark-700 dark:text-dark-200 hover:bg-gray-200 dark:hover:bg-dark-600'
            ]"
          >
            Acceptés <span class="hidden sm:inline">({{ countByStatus('accepted') }})</span>
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
              <span
                :class="[
                  'px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wide',
                  getStatusClass(quote.status)
                ]"
              >
                {{ getStatusLabel(quote.status) }}
              </span>
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
                {{ formatShortDate(quote.created_at) }}
              </div>
              <div class="flex items-center gap-2 text-sm font-semibold" :class="quote.discount_amount > 0 ? 'text-green-600 dark:text-green-400' : 'text-dark-800 dark:text-dark-100'">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                {{ quote.total_price }} €
              </div>
            </div>

            <!-- Tags -->
            <div class="flex flex-wrap gap-2 mb-4">
              <span class="px-2 py-1 bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300 text-xs font-medium rounded">
                {{ quote.design_option?.name || 'N/A' }}
              </span>
              <span class="px-2 py-1 bg-purple-50 dark:bg-purple-900/20 text-purple-700 dark:text-purple-300 text-xs font-medium rounded">
                {{ quote.complexity_level?.name || 'N/A' }}
              </span>
              <span v-if="quote.supplementary_options.length > 0" class="px-2 py-1 bg-amber-50 dark:bg-amber-900/20 text-amber-700 dark:text-amber-300 text-xs font-medium rounded">
                +{{ quote.supplementary_options.length }} option{{ quote.supplementary_options.length > 1 ? 's' : '' }}
              </span>
            </div>

            <!-- Actions rapides -->
            <div class="flex flex-wrap gap-2">
              <button
                v-if="quote.status === 'draft'"
                @click.stop="sendQuote(quote.id)"
                :disabled="sending === quote.id"
                class="flex-1 flex items-center justify-center gap-2 px-4 py-2 bg-gradient-to-r from-green-600 to-green-500 hover:from-green-700 hover:to-green-600 text-white rounded-lg font-medium transition-all disabled:opacity-50 text-sm"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                </svg>
                {{ sending === quote.id ? 'Envoi...' : 'Envoyer' }}
              </button>
              <button
                v-if="quote.status === 'sent' && quote.signature_token"
                @click.stop="goToSignature(quote)"
                class="flex-1 flex items-center justify-center gap-2 px-4 py-2 bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-700 hover:to-blue-600 text-white rounded-lg font-medium transition-all text-sm"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"></path>
                </svg>
                Signer
              </button>
              <button
                v-if="quote.pdf_file"
                @click.stop="downloadPDF(quote.id, quote.quote_number)"
                :disabled="downloading === quote.id"
                class="flex items-center justify-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg font-medium transition-all disabled:opacity-50 text-sm"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
                PDF
              </button>
              <button
                @click.stop="openQuoteDetails(quote)"
                class="flex items-center justify-center gap-2 px-4 py-2 bg-gray-100 dark:bg-dark-700 hover:bg-gray-200 dark:hover:bg-dark-600 text-dark-700 dark:text-dark-200 rounded-lg font-medium transition-all text-sm"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                Détails
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Modal de détails -->
      <div
        v-if="selectedQuote"
        class="fixed inset-0 z-50 overflow-y-auto"
        aria-labelledby="modal-title"
        role="dialog"
        aria-modal="true"
      >
        <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
          <div
            class="fixed inset-0 bg-gray-900/75 dark:bg-black/80 transition-opacity"
            aria-hidden="true"
            @click="closeQuoteDetails"
          ></div>

          <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>

          <div class="relative inline-block align-bottom bg-white dark:bg-dark-800 rounded-2xl text-left overflow-hidden shadow-2xl transform transition-all sm:my-8 sm:align-middle sm:max-w-4xl sm:w-full">
            <!-- En-tête du modal -->
            <div class="bg-gradient-to-r from-primary-600 to-secondary-600 px-6 py-6">
              <div class="flex items-start justify-between">
                <div class="flex-1 text-white">
                  <h3 class="text-2xl font-bold mb-1">{{ selectedQuote.project_type?.name || 'N/A' }}</h3>
                  <p class="text-white/80 font-mono text-sm">#{{ selectedQuote.quote_number }}</p>
                </div>
                <button
                  @click="closeQuoteDetails"
                  class="text-white/80 hover:text-white transition-colors"
                >
                  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                  </svg>
                </button>
              </div>
            </div>

            <!-- Contenu du modal -->
            <div class="px-6 py-6 max-h-[70vh] overflow-y-auto">
              <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <!-- Colonne gauche: Informations -->
                <div class="space-y-6">
                  <!-- Informations générales -->
                  <div>
                    <h4 class="text-lg font-semibold text-dark-800 dark:text-dark-100 mb-3">Informations générales</h4>
                    <div class="space-y-3 bg-gray-50 dark:bg-dark-700 rounded-lg p-4">
                      <div class="flex justify-between">
                        <span class="text-dark-600 dark:text-dark-300">Type de projet:</span>
                        <span class="font-semibold text-dark-800 dark:text-dark-100">{{ selectedQuote.project_type?.name || 'N/A' }}</span>
                      </div>
                      <div class="flex justify-between">
                        <span class="text-dark-600 dark:text-dark-300">Design:</span>
                        <span class="font-semibold text-dark-800 dark:text-dark-100">{{ selectedQuote.design_option?.name || 'N/A' }}</span>
                      </div>
                      <div class="flex justify-between">
                        <span class="text-dark-600 dark:text-dark-300">Complexité:</span>
                        <span class="font-semibold text-dark-800 dark:text-dark-100">{{ selectedQuote.complexity_level?.name || 'N/A' }}</span>
                      </div>
                      <div class="flex justify-between border-t border-gray-200 dark:border-dark-600 pt-3">
                        <span class="text-dark-600 dark:text-dark-300">Prix total:</span>
                        <span class="text-xl font-bold text-primary-600 dark:text-primary-400">{{ selectedQuote.total_price }} €</span>
                      </div>
                      <div v-if="selectedQuote.discount_amount > 0" class="flex justify-between text-green-600 dark:text-green-400">
                        <span>Remise appliquée:</span>
                        <span class="font-semibold">-{{ selectedQuote.discount_amount }}€</span>
                      </div>
                    </div>
                  </div>

                  <!-- Options supplémentaires -->
                  <div v-if="selectedQuote.supplementary_options.length > 0">
                    <h4 class="text-lg font-semibold text-dark-800 dark:text-dark-100 mb-3">Options supplémentaires</h4>
                    <div class="space-y-2">
                      <div
                        v-for="option in selectedQuote.supplementary_options"
                        :key="option.id"
                        class="flex items-center gap-2 bg-primary-50 dark:bg-primary-900/20 rounded-lg p-3"
                      >
                        <svg class="w-5 h-5 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                        </svg>
                        <span class="text-dark-800 dark:text-dark-100 font-medium">{{ option.name }}</span>
                        <span class="ml-auto text-primary-600 dark:text-primary-400 font-semibold">+{{ option.price }}€</span>
                      </div>
                    </div>
                  </div>

                  <!-- Description du projet -->
                  <div v-if="selectedQuote.project_description">
                    <h4 class="text-lg font-semibold text-dark-800 dark:text-dark-100 mb-3">Description du projet</h4>
                    <p class="text-dark-600 dark:text-dark-300 bg-gray-50 dark:bg-dark-700 rounded-lg p-4 leading-relaxed">
                      {{ selectedQuote.project_description }}
                    </p>
                  </div>
                </div>

                <!-- Colonne droite: Timeline -->
                <div>
                  <h4 class="text-lg font-semibold text-dark-800 dark:text-dark-100 mb-3">Historique</h4>
                  <QuoteTimeline :quote="selectedQuote" />
                </div>
              </div>
            </div>

            <!-- Pied de page du modal -->
            <div class="bg-gray-50 dark:bg-dark-700 px-6 py-4 flex justify-end gap-3">
              <button
                v-if="selectedQuote.pdf_file"
                @click="downloadPDF(selectedQuote.id, selectedQuote.quote_number)"
                :disabled="downloading === selectedQuote.id"
                class="flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg font-medium transition-all disabled:opacity-50"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
                {{ downloading === selectedQuote.id ? 'Téléchargement...' : 'Télécharger PDF' }}
              </button>
              <button
                @click="closeQuoteDetails"
                class="px-4 py-2 bg-gray-200 dark:bg-dark-600 hover:bg-gray-300 dark:hover:bg-dark-500 text-dark-700 dark:text-dark-200 rounded-lg font-medium transition-all"
              >
                Fermer
              </button>
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
import { getMyQuotes, sendQuote as sendQuoteAPI, downloadQuotePDF } from '../api/quotes'
import { useToastStore } from '../stores/toast'
import ClientQuoteStats from '../components/ClientQuoteStats.vue'
import QuoteTimeline from '../components/QuoteTimeline.vue'

const router = useRouter()
const toastStore = useToastStore()

const quotes = ref([])
const loading = ref(true)
const filterStatus = ref(null)
const sending = ref(null)
const downloading = ref(null)
const selectedQuote = ref(null)

const filteredQuotes = computed(() => {
  if (!Array.isArray(quotes.value)) return []
  if (filterStatus.value === null) return quotes.value
  return quotes.value.filter(q => q.status === filterStatus.value)
})

const countByStatus = (status) => {
  if (!Array.isArray(quotes.value)) return 0
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
    draft: 'bg-gray-100 text-gray-700 dark:bg-gray-900/30 dark:text-gray-300',
    sent: 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300',
    viewed: 'bg-indigo-100 text-indigo-700 dark:bg-indigo-900/30 dark:text-indigo-300',
    accepted: 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300',
    rejected: 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-300',
    expired: 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-300'
  }
  return classes[status] || 'bg-gray-100 text-gray-700'
}

const getProgressPercentage = (quote) => {
  const statusProgress = {
    draft: 20,
    sent: 40,
    viewed: 60,
    accepted: 100,
    rejected: 100,
    expired: 100
  }
  return statusProgress[quote.status] || 0
}

const formatShortDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('fr-FR', {
    day: '2-digit',
    month: 'short'
  })
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

const sendQuote = async (quoteId) => {
  try {
    sending.value = quoteId
    await sendQuoteAPI(quoteId)
    toastStore.showToast('Devis envoyé avec succès par email', 'success')
    await loadQuotes()
  } catch (error) {
    console.error('Erreur lors de l\'envoi du devis:', error)
    toastStore.showToast('Erreur lors de l\'envoi du devis', 'error')
  } finally {
    sending.value = null
  }
}

const downloadPDF = async (quoteId, quoteNumber) => {
  try {
    downloading.value = quoteId
    const response = await downloadQuotePDF(quoteId)

    const blob = new Blob([response.data], { type: 'application/pdf' })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `devis-${quoteNumber}.pdf`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)

    toastStore.showToast('PDF téléchargé avec succès', 'success')
  } catch (error) {
    console.error('Erreur lors du téléchargement du PDF:', error)
    toastStore.showToast('Erreur lors du téléchargement du PDF', 'error')
  } finally {
    downloading.value = null
  }
}

const loadQuotes = async () => {
  try {
    const response = await getMyQuotes()
    quotes.value = Array.isArray(response.data) ? response.data :
                   (response.data.results ? response.data.results : [])
  } catch (error) {
    console.error('Erreur lors du chargement des devis:', error)
    toastStore.showToast('Erreur lors du chargement des devis', 'error')
    quotes.value = []
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadQuotes()
})
</script>
