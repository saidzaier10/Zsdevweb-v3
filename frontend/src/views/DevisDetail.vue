<template>
  <div class="min-h-screen bg-gray-50 dark:bg-dark-900 py-12 transition-colors duration-200">
    <div class="container mx-auto px-4 lg:px-8 max-w-4xl">
      <!-- Bouton retour -->
      <button
        @click="$router.back()"
        class="mb-6 flex items-center text-primary-600 hover:text-primary-700 dark:text-primary-400 font-medium transition-colors"
      >
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
        </svg>
        Retour
      </button>

      <!-- Chargement -->
      <LoadingSpinner
        v-if="loading"
        message="Chargement du devis..."
      />

      <!-- Erreur -->
      <div v-else-if="error" class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-xl p-6 text-center">
        <svg class="w-12 h-12 mx-auto mb-4 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
        <h3 class="text-xl font-semibold text-red-800 dark:text-red-200 mb-2">Erreur</h3>
        <p class="text-red-700 dark:text-red-300">{{ error }}</p>
      </div>

      <!-- Détail du devis -->
      <div v-else-if="quote" class="space-y-6">
        <!-- En-tête -->
        <div class="bg-white dark:bg-dark-800 rounded-xl shadow-sm p-6 border border-gray-200 dark:border-dark-700">
          <div class="flex flex-col md:flex-row md:items-start md:justify-between gap-4 mb-6">
            <div>
              <h1 class="text-3xl font-display font-bold gradient-text mb-2">
                {{ quote.project_type_detail.name }}
              </h1>
              <p class="text-dark-600 dark:text-dark-400">
                Référence: #{{ quote.quote_number }}
              </p>
            </div>
            <div class="flex flex-col items-start md:items-end gap-2">
              <StatusBadge :status="quote.status" />
              <p class="text-sm text-dark-600 dark:text-dark-400">
                Créé le {{ formatDate(quote.created_at) }}
              </p>
            </div>
          </div>

          <!-- Informations client -->
          <div class="border-t border-gray-200 dark:border-dark-700 pt-6">
            <h2 class="text-lg font-semibold text-dark-800 dark:text-dark-100 mb-4">Informations client</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
              <div>
                <p class="text-dark-600 dark:text-dark-400 mb-1">Nom</p>
                <p class="font-medium text-dark-800 dark:text-dark-100">{{ quote.client_name }}</p>
              </div>
              <div>
                <p class="text-dark-600 dark:text-dark-400 mb-1">Email</p>
                <p class="font-medium text-dark-800 dark:text-dark-100">{{ quote.client_email }}</p>
              </div>
              <div v-if="quote.client_phone">
                <p class="text-dark-600 dark:text-dark-400 mb-1">Téléphone</p>
                <p class="font-medium text-dark-800 dark:text-dark-100">{{ quote.client_phone }}</p>
              </div>
              <div v-if="quote.company_name">
                <p class="text-dark-600 dark:text-dark-400 mb-1">Entreprise</p>
                <p class="font-medium text-dark-800 dark:text-dark-100">{{ quote.company_name }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Détails du projet -->
        <div class="bg-white dark:bg-dark-800 rounded-xl shadow-sm p-6 border border-gray-200 dark:border-dark-700">
          <h2 class="text-lg font-semibold text-dark-800 dark:text-dark-100 mb-4">Détails du projet</h2>

          <div class="space-y-4">
            <div class="flex justify-between items-center py-3 border-b border-gray-200 dark:border-dark-700">
              <span class="text-dark-700 dark:text-dark-300">Type de projet</span>
              <span class="font-semibold text-dark-800 dark:text-dark-100">{{ quote.project_type_detail.name }}</span>
            </div>

            <div class="flex justify-between items-center py-3 border-b border-gray-200 dark:border-dark-700">
              <span class="text-dark-700 dark:text-dark-300">Option de design</span>
              <span class="font-semibold text-dark-800 dark:text-dark-100">{{ quote.design_option_detail.name }}</span>
            </div>

            <div class="flex justify-between items-center py-3 border-b border-gray-200 dark:border-dark-700">
              <span class="text-dark-700 dark:text-dark-300">Niveau de complexité</span>
              <span class="font-semibold text-dark-800 dark:text-dark-100">{{ quote.complexity_level_detail.name }}</span>
            </div>

            <div v-if="quote.supplementary_options_detail.length > 0" class="py-3 border-b border-gray-200 dark:border-dark-700">
              <span class="text-dark-700 dark:text-dark-300 block mb-2">Options supplémentaires</span>
              <div class="flex flex-wrap gap-2">
                <span
                  v-for="option in quote.supplementary_options_detail"
                  :key="option.id"
                  class="px-3 py-1 bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-300 rounded-full text-sm font-medium"
                >
                  {{ option.name }}
                </span>
              </div>
            </div>

            <div v-if="quote.project_description" class="py-3 border-b border-gray-200 dark:border-dark-700">
              <span class="text-dark-700 dark:text-dark-300 block mb-2">Description du projet</span>
              <p class="text-dark-800 dark:text-dark-100 whitespace-pre-wrap">{{ quote.project_description }}</p>
            </div>

            <div v-if="quote.deadline" class="flex justify-between items-center py-3">
              <span class="text-dark-700 dark:text-dark-300">Date limite souhaitée</span>
              <span class="font-semibold text-dark-800 dark:text-dark-100">{{ formatDate(quote.deadline) }}</span>
            </div>

            <div v-if="quote.estimated_duration_days" class="flex justify-between items-center py-3 border-t border-gray-200 dark:border-dark-700">
              <span class="text-dark-700 dark:text-dark-300">Durée estimée</span>
              <span class="font-semibold text-dark-800 dark:text-dark-100">{{ quote.estimated_duration_days }} jours</span>
            </div>
          </div>
        </div>

        <!-- Tarification -->
        <div class="bg-white dark:bg-dark-800 rounded-xl shadow-sm p-6 border border-gray-200 dark:border-dark-700">
          <h2 class="text-lg font-semibold text-dark-800 dark:text-dark-100 mb-4">Tarification</h2>

          <div class="space-y-3">
            <div class="flex justify-between items-center py-2">
              <span class="text-dark-700 dark:text-dark-300">Sous-total HT</span>
              <span class="font-medium text-dark-800 dark:text-dark-100">{{ quote.subtotal_ht }} €</span>
            </div>

            <div v-if="quote.discount_amount > 0" class="flex justify-between items-center py-2 text-green-600 dark:text-green-400">
              <span>Remise ({{ quote.discount_reason || 'Remise appliquée' }})</span>
              <span class="font-medium">-{{ quote.discount_amount }} €</span>
            </div>

            <div class="flex justify-between items-center py-2">
              <span class="text-dark-700 dark:text-dark-300">TVA ({{ quote.tva_rate }}%)</span>
              <span class="font-medium text-dark-800 dark:text-dark-100">{{ quote.tva_amount }} €</span>
            </div>

            <div class="flex justify-between items-center py-4 border-t-2 border-gray-300 dark:border-dark-600">
              <span class="text-xl font-bold text-dark-800 dark:text-dark-100">Total TTC</span>
              <span class="text-2xl font-bold gradient-text">{{ quote.total_ttc }} €</span>
            </div>

            <!-- Échéancier de paiement -->
            <div class="mt-6 pt-4 border-t border-gray-200 dark:border-dark-700">
              <h3 class="text-sm font-semibold text-dark-700 dark:text-dark-300 mb-3">Échéancier de paiement</h3>
              <div class="space-y-2 text-sm">
                <div class="flex justify-between">
                  <span class="text-dark-600 dark:text-dark-400">Acompte (30%)</span>
                  <span class="font-medium text-dark-800 dark:text-dark-100">{{ quote.payment_first }} €</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-dark-600 dark:text-dark-400">Intermédiaire (40%)</span>
                  <span class="font-medium text-dark-800 dark:text-dark-100">{{ quote.payment_second }} €</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-dark-600 dark:text-dark-400">Solde (30%)</span>
                  <span class="font-medium text-dark-800 dark:text-dark-100">{{ quote.payment_final }} €</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Signature -->
        <div v-if="quote.signed_at" class="bg-green-50 dark:bg-green-900/20 rounded-xl shadow-sm p-6 border border-green-200 dark:border-green-800">
          <h2 class="text-lg font-semibold text-green-800 dark:text-green-200 mb-4 flex items-center">
            <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            Devis signé
          </h2>
          <div class="space-y-2 text-sm">
            <p class="text-green-700 dark:text-green-300">
              <span class="font-medium">Date de signature:</span> {{ formatDate(quote.signed_at) }}
            </p>
            <p v-if="quote.client_ip" class="text-green-700 dark:text-green-300">
              <span class="font-medium">IP:</span> {{ quote.client_ip }}
            </p>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex flex-col sm:flex-row gap-3">
          <button
            v-if="quote.status === 'sent' && quote.signature_token"
            @click="goToSignature"
            class="flex-1 px-6 py-3 bg-green-600 hover:bg-green-700 text-white rounded-lg font-semibold transition-colors flex items-center justify-center"
          >
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"></path>
            </svg>
            Signer le devis
          </button>

          <button
            @click="downloadPDF"
            :disabled="downloading"
            class="flex-1 px-6 py-3 bg-primary-600 hover:bg-primary-700 disabled:bg-gray-400 text-white rounded-lg font-semibold transition-colors flex items-center justify-center"
          >
            <svg v-if="!downloading" class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
            </svg>
            <div v-else class="inline-block animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
            {{ downloading ? 'Téléchargement...' : 'Télécharger PDF' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getQuote, downloadQuotePDF } from '../api/quotes'
import { LoadingSpinner, StatusBadge } from '@/components/ui'
import { formatDate } from '@/utils/formatters'
import { useApi } from '@/composables/useApi'

const route = useRoute()
const router = useRouter()
const { loading, error, callApi } = useApi() || {}

const quote = ref(null)
const downloading = ref(false)

const goToSignature = () => {
  router.push(`/signature/${quote.value.signature_token}`)
}

const downloadPDF = async () => {
  downloading.value = true

  const response = await callApi(
    () => downloadQuotePDF(quote.value.id),
    {
      successMessage: 'PDF téléchargé avec succès',
      errorMessage: 'Erreur lors du téléchargement du PDF'
    }
  )

  if (response) {
    const blob = new Blob([response.data], { type: 'application/pdf' })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `devis-${quote.value.quote_number}.pdf`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
  }

  downloading.value = false
}

const loadQuote = async () => {
  const response = await callApi(
    () => getQuote(route.params.id),
    {
      errorMessage: 'Impossible de charger les détails du devis'
    }
  )

  if (response) {
    quote.value = response.data
  }
}

onMounted(() => {
  loadQuote()
})
</script>
