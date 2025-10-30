<template>
  <div class="min-h-screen bg-gray-50 dark:bg-dark-900 py-12">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Loading -->
      <div v-if="loading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>

      <!-- Devis Detail -->
      <div v-else-if="quote" class="bg-white dark:bg-dark-800 rounded-lg shadow-lg overflow-hidden">
        <!-- Header -->
        <div class="bg-gradient-to-r from-indigo-600 to-indigo-700 px-8 py-6">
          <div class="flex justify-between items-start">
            <div>
              <h1 class="text-3xl font-bold text-white">{{ quote.quote_number }}</h1>
              <p class="text-indigo-100 mt-1">{{ quote.project_type_detail?.name }}</p>
            </div>
            <span
              :class="[
                'px-4 py-2 rounded-full text-sm font-semibold',
                getStatusClass(quote.status)
              ]"
            >
              {{ quote.status_display }}
            </span>
          </div>
        </div>

        <!-- Content -->
        <div class="px-8 py-6">
          <!-- Informations Client -->
          <section class="mb-8">
            <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-4">
              Informations Client
            </h2>
            <div class="grid md:grid-cols-2 gap-4">
              <div>
                <p class="text-sm text-gray-500 dark:text-gray-400">Nom</p>
                <p class="font-medium text-gray-900 dark:text-white">{{ quote.client_name }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-500 dark:text-gray-400">Email</p>
                <p class="font-medium text-gray-900 dark:text-white">{{ quote.client_email }}</p>
              </div>
              <div v-if="quote.client_phone">
                <p class="text-sm text-gray-500 dark:text-gray-400">Téléphone</p>
                <p class="font-medium text-gray-900 dark:text-white">{{ quote.client_phone }}</p>
              </div>
              <div v-if="quote.company_name">
                <p class="text-sm text-gray-500 dark:text-gray-400">Entreprise</p>
                <p class="font-medium text-gray-900 dark:text-white">{{ quote.company_name }}</p>
              </div>
            </div>
          </section>

          <!-- Détails du Projet -->
          <section class="mb-8">
            <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-4">
              Détails du Projet
            </h2>
            <div class="space-y-4">
              <div>
                <p class="text-sm text-gray-500 dark:text-gray-400">Type de projet</p>
                <p class="font-medium text-gray-900 dark:text-white">
                  {{ quote.project_type_detail?.name }}
                </p>
              </div>
              <div>
                <p class="text-sm text-gray-500 dark:text-gray-400">Option de design</p>
                <p class="font-medium text-gray-900 dark:text-white">
                  {{ quote.design_option_detail?.name }}
                </p>
              </div>
              <div>
                <p class="text-sm text-gray-500 dark:text-gray-400">Complexité</p>
                <p class="font-medium text-gray-900 dark:text-white">
                  {{ quote.complexity_level_detail?.name }}
                </p>
              </div>
              <div v-if="quote.project_description">
                <p class="text-sm text-gray-500 dark:text-gray-400">Description</p>
                <p class="font-medium text-gray-900 dark:text-white">
                  {{ quote.project_description }}
                </p>
              </div>
            </div>
          </section>

          <!-- Options Supplémentaires -->
          <section v-if="quote.supplementary_options_detail?.length > 0" class="mb-8">
            <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-4">
              Options Supplémentaires
            </h2>
            <ul class="space-y-2">
              <li
                v-for="option in quote.supplementary_options_detail"
                :key="option.id"
                class="flex justify-between items-center py-2 border-b border-gray-200 dark:border-gray-700"
              >
                <span class="text-gray-900 dark:text-white">{{ option.name }}</span>
                <span class="font-medium text-gray-900 dark:text-white">
                  {{ option.price }} €
                </span>
              </li>
            </ul>
          </section>

          <!-- Détails Financiers -->
          <section class="mb-8">
            <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-4">
              Détails Financiers
            </h2>
            <div class="bg-gray-50 dark:bg-dark-700 rounded-lg p-6 space-y-3">
              <div class="flex justify-between">
                <span class="text-gray-600 dark:text-gray-300">Sous-total HT</span>
                <span class="font-medium text-gray-900 dark:text-white">
                  {{ quote.subtotal_ht }} €
                </span>
              </div>
              <div v-if="quote.discount_amount > 0" class="flex justify-between text-green-600">
                <span>Remise {{ quote.discount_reason ? `(${quote.discount_reason})` : '' }}</span>
                <span>- {{ quote.discount_amount }} €</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600 dark:text-gray-300">TVA ({{ quote.tva_rate }}%)</span>
                <span class="font-medium text-gray-900 dark:text-white">
                  {{ quote.tva_amount }} €
                </span>
              </div>
              <div class="flex justify-between text-lg font-bold border-t border-gray-300 dark:border-gray-600 pt-3">
                <span class="text-gray-900 dark:text-white">Total TTC</span>
                <span class="text-indigo-600 dark:text-indigo-400">
                  {{ quote.total_ttc }} €
                </span>
              </div>
            </div>
          </section>

          <!-- Paiements -->
          <section class="mb-8">
            <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-4">
              Échéancier de Paiement
            </h2>
            <div class="grid md:grid-cols-3 gap-4">
              <div class="bg-indigo-50 dark:bg-indigo-900/20 rounded-lg p-4">
                <p class="text-sm text-indigo-600 dark:text-indigo-400 mb-1">Acompte (30%)</p>
                <p class="text-2xl font-bold text-indigo-700 dark:text-indigo-300">
                  {{ quote.payment_first }} €
                </p>
              </div>
              <div class="bg-indigo-50 dark:bg-indigo-900/20 rounded-lg p-4">
                <p class="text-sm text-indigo-600 dark:text-indigo-400 mb-1">2ème paiement (40%)</p>
                <p class="text-2xl font-bold text-indigo-700 dark:text-indigo-300">
                  {{ quote.payment_second }} €
                </p>
              </div>
              <div class="bg-indigo-50 dark:bg-indigo-900/20 rounded-lg p-4">
                <p class="text-sm text-indigo-600 dark:text-indigo-400 mb-1">Solde (30%)</p>
                <p class="text-2xl font-bold text-indigo-700 dark:text-indigo-300">
                  {{ quote.payment_final }} €
                </p>
              </div>
            </div>
          </section>

          <!-- Signature (si signé) -->
          <section v-if="quote.signed_at" class="mb-8">
            <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-4">
              Signature
            </h2>
            <div class="bg-green-50 dark:bg-green-900/20 rounded-lg p-6">
              <div class="flex items-center mb-4">
                <svg class="w-6 h-6 text-green-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span class="text-green-700 dark:text-green-300 font-medium">
                  Devis signé le {{ formatDate(quote.signed_at) }}
                </span>
              </div>
              <p class="text-gray-700 dark:text-gray-300">
                Signé par: <strong>{{ quote.signer_name }}</strong>
              </p>
              <img
                v-if="quote.signature_image"
                :src="quote.signature_image"
                alt="Signature"
                class="mt-4 border border-gray-300 dark:border-gray-600 rounded p-2 bg-white max-w-xs"
              />
            </div>
          </section>

          <!-- Dates -->
          <section class="mb-8">
            <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-4">
              Dates Importantes
            </h2>
            <div class="grid md:grid-cols-2 gap-4">
              <div>
                <p class="text-sm text-gray-500 dark:text-gray-400">Créé le</p>
                <p class="font-medium text-gray-900 dark:text-white">
                  {{ formatDate(quote.created_at) }}
                </p>
              </div>
              <div>
                <p class="text-sm text-gray-500 dark:text-gray-400">Expire le</p>
                <p class="font-medium text-gray-900 dark:text-white">
                  {{ formatDate(quote.expires_at) }}
                </p>
              </div>
              <div v-if="quote.estimated_start_date">
                <p class="text-sm text-gray-500 dark:text-gray-400">Début estimé</p>
                <p class="font-medium text-gray-900 dark:text-white">
                  {{ formatDate(quote.estimated_start_date) }}
                </p>
              </div>
              <div v-if="quote.estimated_duration_days">
                <p class="text-sm text-gray-500 dark:text-gray-400">Durée estimée</p>
                <p class="font-medium text-gray-900 dark:text-white">
                  {{ quote.estimated_duration_days }} jours
                </p>
              </div>
            </div>
          </section>

          <!-- Actions -->
          <div class="flex flex-wrap gap-4 border-t border-gray-200 dark:border-gray-700 pt-6">
            <button
              @click="downloadPdf"
              class="flex-1 px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors font-medium"
            >
              Télécharger PDF
            </button>
            <button
              v-if="quote.status === 'sent' && !quote.is_expired"
              @click="goToSignature"
              class="flex-1 px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors font-medium"
            >
              Signer le devis
            </button>
            <button
              @click="resendEmail"
              class="px-6 py-3 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors font-medium"
            >
              Renvoyer par email
            </button>
            <button
              @click="$router.push('/mes-devis')"
              class="px-6 py-3 bg-gray-200 dark:bg-dark-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-300 dark:hover:bg-dark-600 transition-colors font-medium"
            >
              Retour
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getQuote, downloadPDF, sendEmail } from '../api/quotes'
import { useToastStore } from '../stores/toast'

const route = useRoute()
const router = useRouter()
const toastStore = useToastStore()

const quote = ref(null)
const loading = ref(false)

const fetchQuote = async () => {
  loading.value = true
  try {
    const response = await getQuote(route.params.id)
    quote.value = response.data
  } catch (error) {
    console.error('Erreur chargement devis:', error)
    toastStore.addToast('Erreur lors du chargement du devis', 'error')
    router.push('/mes-devis')
  } finally {
    loading.value = false
  }
}

const downloadPdf = async () => {
  try {
    const response = await downloadPDF(route.params.id)
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `${quote.value.quote_number}.pdf`)
    document.body.appendChild(link)
    link.click()
    link.remove()
    toastStore.addToast('PDF téléchargé avec succès', 'success')
  } catch (error) {
    console.error('Erreur téléchargement PDF:', error)
    toastStore.addToast('Erreur lors du téléchargement du PDF', 'error')
  }
}

const resendEmail = async () => {
  try {
    await sendEmail(route.params.id)
    toastStore.addToast('Email envoyé avec succès', 'success')
  } catch (error) {
    console.error('Erreur envoi email:', error)
    toastStore.addToast('Erreur lors de l\'envoi de l\'email', 'error')
  }
}

const goToSignature = () => {
  router.push(`/signature/${quote.value.signature_token}`)
}

const getStatusClass = (status) => {
  const classes = {
    draft: 'bg-gray-100 text-gray-800',
    sent: 'bg-blue-100 text-blue-800',
    viewed: 'bg-purple-100 text-purple-800',
    accepted: 'bg-green-100 text-green-800',
    rejected: 'bg-red-100 text-red-800',
    expired: 'bg-orange-100 text-orange-800'
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('fr-FR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(() => {
  fetchQuote()
})
</script>