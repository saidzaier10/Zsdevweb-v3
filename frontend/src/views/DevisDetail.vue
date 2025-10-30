<template>
  <div class="devis-detail-container">
    <div class="container mx-auto px-4 py-8">
      <!-- Loader -->
      <div v-if="loading" class="flex justify-center items-center min-h-screen">
        <div class="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-indigo-600"></div>
      </div>

      <!-- Erreur -->
      <div v-else-if="error" class="max-w-2xl mx-auto">
        <div class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-6 text-center">
          <svg class="mx-auto h-12 w-12 text-red-500 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
          <h3 class="text-lg font-medium text-red-800 dark:text-red-200 mb-2">Erreur</h3>
          <p class="text-red-600 dark:text-red-300">{{ error }}</p>
          <router-link to="/mes-devis" class="mt-4 inline-block px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700">
            Retour à mes devis
          </router-link>
        </div>
      </div>

      <!-- Détail du devis -->
      <div v-else-if="quote" class="max-w-5xl mx-auto">
        <!-- En-tête -->
        <div class="flex justify-between items-start mb-8">
          <div>
            <router-link to="/mes-devis" class="text-indigo-600 dark:text-indigo-400 hover:underline mb-2 inline-block">
              ← Retour à mes devis
            </router-link>
            <h1 class="text-3xl font-bold text-gray-900 dark:text-white">{{ quote.quote_number }}</h1>
            <p class="text-gray-600 dark:text-gray-400 mt-1">
              Créé le {{ formatDate(quote.created_at) }}
            </p>
          </div>
          <div class="flex gap-3">
            <span :class="getStatusBadgeClass(quote.status)" class="px-4 py-2 rounded-full text-sm font-medium">
              {{ getStatusLabel(quote.status) }}
            </span>
          </div>
        </div>

        <!-- Actions -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-6">
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Actions</h2>
          <div class="flex flex-wrap gap-3">
            <button
              @click="downloadPDF"
              :disabled="downloadingPDF"
              class="flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
            >
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              {{ downloadingPDF ? 'Téléchargement...' : 'Télécharger PDF' }}
            </button>

            <button
              v-if="canSign"
              @click="goToSignature"
              class="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
            >
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
              </svg>
              Signer le devis
            </button>

            <button
              v-if="quote.status === 'draft'"
              @click="resendEmail"
              :disabled="sendingEmail"
              class="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
            >
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
              {{ sendingEmail ? 'Envoi...' : 'Envoyer par email' }}
            </button>
          </div>
        </div>

        <!-- Informations client -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-6">
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Informations client</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <p class="text-sm text-gray-600 dark:text-gray-400">Nom du client</p>
              <p class="text-gray-900 dark:text-white font-medium">{{ quote.client_name }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-600 dark:text-gray-400">Email</p>
              <p class="text-gray-900 dark:text-white font-medium">{{ quote.client_email }}</p>
            </div>
            <div v-if="quote.client_phone">
              <p class="text-sm text-gray-600 dark:text-gray-400">Téléphone</p>
              <p class="text-gray-900 dark:text-white font-medium">{{ quote.client_phone }}</p>
            </div>
            <div v-if="quote.client_company">
              <p class="text-sm text-gray-600 dark:text-gray-400">Entreprise</p>
              <p class="text-gray-900 dark:text-white font-medium">{{ quote.client_company }}</p>
            </div>
          </div>
        </div>

        <!-- Détails du projet -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-6">
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Détails du projet</h2>
          <div class="space-y-4">
            <div v-if="quote.company_details">
              <p class="text-sm text-gray-600 dark:text-gray-400">Type d'entreprise</p>
              <p class="text-gray-900 dark:text-white font-medium">{{ quote.company_details.name }}</p>
            </div>
            <div v-if="quote.project_type_details">
              <p class="text-sm text-gray-600 dark:text-gray-400">Type de projet</p>
              <p class="text-gray-900 dark:text-white font-medium">{{ quote.project_type_details.name }}</p>
            </div>
            <div v-if="quote.description">
              <p class="text-sm text-gray-600 dark:text-gray-400">Description</p>
              <p class="text-gray-900 dark:text-white">{{ quote.description }}</p>
            </div>
          </div>
        </div>

        <!-- Options de design -->
        <div v-if="quote.design_options && quote.design_options.length > 0" class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-6">
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Options de design</h2>
          <div class="space-y-3">
            <div v-for="option in quote.design_options" :key="option.id" class="flex justify-between items-center p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
              <div>
                <p class="font-medium text-gray-900 dark:text-white">{{ option.name }}</p>
                <p v-if="option.description" class="text-sm text-gray-600 dark:text-gray-400">{{ option.description }}</p>
              </div>
              <span class="text-indigo-600 dark:text-indigo-400 font-semibold">{{ formatPrice(option.price) }} €</span>
            </div>
          </div>
        </div>

        <!-- Fonctionnalités -->
        <div v-if="quote.features && quote.features.length > 0" class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-6">
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Fonctionnalités</h2>
          <div class="space-y-3">
            <div v-for="feature in quote.features" :key="feature.id" class="flex justify-between items-center p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
              <div>
                <p class="font-medium text-gray-900 dark:text-white">{{ feature.name }}</p>
                <p v-if="feature.description" class="text-sm text-gray-600 dark:text-gray-400">{{ feature.description }}</p>
              </div>
              <span class="text-indigo-600 dark:text-indigo-400 font-semibold">{{ formatPrice(feature.price) }} €</span>
            </div>
          </div>
        </div>

        <!-- Options supplémentaires -->
        <div v-if="quote.supplementary_options && quote.supplementary_options.length > 0" class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-6">
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Options supplémentaires</h2>
          <div class="space-y-3">
            <div v-for="option in quote.supplementary_options" :key="option.id" class="flex justify-between items-center p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
              <div>
                <p class="font-medium text-gray-900 dark:text-white">{{ option.name }}</p>
                <p v-if="option.description" class="text-sm text-gray-600 dark:text-gray-400">{{ option.description }}</p>
                <span class="text-xs text-gray-500 dark:text-gray-400">
                  {{ option.billing_type === 'one_time' ? 'Paiement unique' : 'Paiement mensuel' }}
                </span>
              </div>
              <span class="text-indigo-600 dark:text-indigo-400 font-semibold">
                {{ formatPrice(option.price) }} €{{ option.billing_type === 'monthly' ? '/mois' : '' }}
              </span>
            </div>
          </div>
        </div>

        <!-- Tarification -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-6">
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Tarification</h2>
          <div class="space-y-3">
            <div class="flex justify-between text-gray-700 dark:text-gray-300">
              <span>Sous-total HT</span>
              <span>{{ formatPrice(quote.subtotal_ht) }} €</span>
            </div>
            <div v-if="quote.discount_percentage > 0" class="flex justify-between text-green-600 dark:text-green-400">
              <span>Remise ({{ quote.discount_percentage }}%)</span>
              <span>- {{ formatPrice(quote.discount_amount) }} €</span>
            </div>
            <div class="flex justify-between text-gray-700 dark:text-gray-300">
              <span>Total HT</span>
              <span>{{ formatPrice(quote.total_ht) }} €</span>
            </div>
            <div class="flex justify-between text-gray-700 dark:text-gray-300">
              <span>TVA ({{ quote.tax_percentage }}%)</span>
              <span>{{ formatPrice(quote.tax_amount) }} €</span>
            </div>
            <div class="flex justify-between text-xl font-bold text-gray-900 dark:text-white pt-3 border-t border-gray-200 dark:border-gray-700">
              <span>Total TTC</span>
              <span>{{ formatPrice(quote.total_ttc) }} €</span>
            </div>
            <div v-if="quote.monthly_subscription_total > 0" class="flex justify-between text-indigo-600 dark:text-indigo-400 pt-2 border-t border-gray-200 dark:border-gray-700">
              <span>Abonnement mensuel</span>
              <span>{{ formatPrice(quote.monthly_subscription_total) }} € /mois</span>
            </div>
          </div>
        </div>

        <!-- Dates importantes -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-6">
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Dates importantes</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <p class="text-sm text-gray-600 dark:text-gray-400">Date de validité</p>
              <p class="text-gray-900 dark:text-white font-medium">{{ formatDate(quote.valid_until) }}</p>
              <p v-if="isExpired" class="text-red-600 text-sm mt-1">Expiré</p>
              <p v-else-if="expiresInDays <= 7" class="text-orange-600 text-sm mt-1">Expire dans {{ expiresInDays }} jour(s)</p>
            </div>
            <div v-if="quote.signed_at">
              <p class="text-sm text-gray-600 dark:text-gray-400">Signé le</p>
              <p class="text-gray-900 dark:text-white font-medium">{{ formatDate(quote.signed_at) }}</p>
            </div>
          </div>
        </div>

        <!-- Signature (si signé) -->
        <div v-if="quote.signed_at && quote.signature_image" class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Signature</h2>
          <div class="border border-gray-300 dark:border-gray-600 rounded-lg p-4 bg-white dark:bg-gray-900">
            <img :src="quote.signature_image" alt="Signature" class="max-w-md mx-auto" />
            <p class="text-center text-sm text-gray-600 dark:text-gray-400 mt-2">
              Signé par {{ quote.signature_name }} le {{ formatDate(quote.signed_at) }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getQuoteById, downloadQuotePDF, sendQuoteEmail } from '@/api/quotes'
import { useToastStore } from '@/stores/toast'

const route = useRoute()
const router = useRouter()
const toast = useToastStore()

const quote = ref(null)
const loading = ref(true)
const error = ref(null)
const downloadingPDF = ref(false)
const sendingEmail = ref(false)

// Computed
const canSign = computed(() => {
  return quote.value && ['sent', 'viewed'].includes(quote.value.status) && !isExpired.value
})

const isExpired = computed(() => {
  if (!quote.value) return false
  return new Date(quote.value.valid_until) < new Date()
})

const expiresInDays = computed(() => {
  if (!quote.value) return 0
  const validUntil = new Date(quote.value.valid_until)
  const today = new Date()
  const diffTime = validUntil - today
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  return diffDays
})

// Methods
const fetchQuote = async () => {
  try {
    loading.value = true
    error.value = null
    const response = await getQuoteById(route.params.id)
    quote.value = response.data
  } catch (err) {
    console.error('Erreur lors de la récupération du devis:', err)
    error.value = err.response?.data?.detail || 'Impossible de charger le devis'
    toast.error('Erreur', error.value)
  } finally {
    loading.value = false
  }
}

const downloadPDF = async () => {
  try {
    downloadingPDF.value = true
    const response = await downloadQuotePDF(quote.value.id)
    
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `${quote.value.quote_number}.pdf`)
    document.body.appendChild(link)
    link.click()
    link.remove()
    window.URL.revokeObjectURL(url)
    
    toast.success('Téléchargement réussi', 'Le PDF a été téléchargé')
  } catch (err) {
    console.error('Erreur lors du téléchargement:', err)
    toast.error('Erreur', 'Impossible de télécharger le PDF')
  } finally {
    downloadingPDF.value = false
  }
}

const goToSignature = () => {
  router.push(`/signature/${quote.value.public_token}`)
}

const resendEmail = async () => {
  try {
    sendingEmail.value = true
    await sendQuoteEmail(quote.value.id)
    toast.success('Email envoyé', 'Le devis a été envoyé par email')
  } catch (err) {
    console.error('Erreur lors de l\'envoi:', err)
    toast.error('Erreur', 'Impossible d\'envoyer l\'email')
  } finally {
    sendingEmail.value = false
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
  fetchQuote()
})
</script>

<style scoped>
.devis-detail-container {
  min-height: calc(100vh - 64px);
  background-color: #f9fafb;
}

.dark .devis-detail-container {
  background-color: #111827;
}
</style>