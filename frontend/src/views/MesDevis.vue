<template>
  <div class="min-h-screen bg-gray-50 dark:bg-dark-900 py-12">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Mes Devis</h1>
        <p class="mt-2 text-gray-600 dark:text-gray-400">
          Consultez et gérez tous vos devis
        </p>
      </div>

      <!-- Filtres -->
      <div class="mb-6 flex flex-wrap gap-3">
        <button
          @click="filterStatus = null"
          :class="[
            'px-4 py-2 rounded-lg font-medium transition-colors',
            filterStatus === null
              ? 'bg-indigo-600 text-white'
              : 'bg-white dark:bg-dark-800 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-dark-700'
          ]"
        >
          Tous
        </button>
        <button
          @click="filterStatus = 'draft'"
          :class="[
            'px-4 py-2 rounded-lg font-medium transition-colors',
            filterStatus === 'draft'
              ? 'bg-indigo-600 text-white'
              : 'bg-white dark:bg-dark-800 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-dark-700'
          ]"
        >
          Brouillons
        </button>
        <button
          @click="filterStatus = 'sent'"
          :class="[
            'px-4 py-2 rounded-lg font-medium transition-colors',
            filterStatus === 'sent'
              ? 'bg-indigo-600 text-white'
              : 'bg-white dark:bg-dark-800 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-dark-700'
          ]"
        >
          Envoyés
        </button>
        <button
          @click="filterStatus = 'accepted'"
          :class="[
            'px-4 py-2 rounded-lg font-medium transition-colors',
            filterStatus === 'accepted'
              ? 'bg-indigo-600 text-white'
              : 'bg-white dark:bg-dark-800 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-dark-700'
          ]"
        >
          Acceptés
        </button>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>

      <!-- Liste des devis -->
      <div v-else-if="filteredQuotes.length > 0" class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        <div
          v-for="quote in filteredQuotes"
          :key="quote.id"
          class="bg-white dark:bg-dark-800 rounded-lg shadow-md hover:shadow-lg transition-shadow p-6"
        >
          <!-- Status Badge -->
          <div class="flex justify-between items-start mb-4">
            <span
              :class="[
                'px-3 py-1 rounded-full text-xs font-semibold',
                getStatusClass(quote.status)
              ]"
            >
              {{ quote.status_display }}
            </span>
            <span v-if="quote.is_expired" class="text-red-600 text-xs font-medium">
              Expiré
            </span>
          </div>

          <!-- Infos -->
          <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-2">
            {{ quote.quote_number }}
          </h3>
          <p class="text-gray-600 dark:text-gray-400 text-sm mb-1">
            {{ quote.client_name }}
          </p>
          <p class="text-gray-600 dark:text-gray-400 text-sm mb-4">
            {{ quote.project_type_name }}
          </p>

          <!-- Prix -->
          <div class="text-2xl font-bold text-indigo-600 dark:text-indigo-400 mb-4">
            {{ quote.total_ttc }} € TTC
          </div>

          <!-- Date -->
          <p class="text-gray-500 dark:text-gray-500 text-xs mb-4">
            Créé le {{ formatDate(quote.created_at) }}
          </p>

          <!-- Actions -->
          <div class="flex flex-wrap gap-2">
            <button
              @click="viewDetail(quote.id)"
              class="flex-1 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors text-sm font-medium"
            >
              Voir
            </button>
            <button
              v-if="quote.status === 'sent' && !quote.is_expired"
              @click="goToSignature(quote)"
              class="flex-1 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors text-sm font-medium"
            >
              Signer
            </button>
            <button
              @click="downloadPdf(quote.id)"
              class="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors text-sm font-medium"
            >
              PDF
            </button>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="text-center py-12">
        <div class="text-gray-400 mb-4">
          <svg class="mx-auto h-24 w-24" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        </div>
        <h3 class="text-xl font-medium text-gray-900 dark:text-white mb-2">
          Aucun devis trouvé
        </h3>
        <p class="text-gray-500 dark:text-gray-400 mb-6">
          Commencez par créer votre premier devis
        </p>
        <router-link
          to="/devis"
          class="inline-block px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors font-medium"
        >
          Créer un devis
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getQuotes, downloadPDF } from '../api/quotes'
import { useToastStore } from '../stores/toast'

const router = useRouter()
const toastStore = useToastStore()

const quotes = ref([])
const loading = ref(false)
const filterStatus = ref(null)

const filteredQuotes = computed(() => {
  if (!filterStatus.value) return quotes.value
  return quotes.value.filter(q => q.status === filterStatus.value)
})

const fetchQuotes = async () => {
  loading.value = true
  try {
    const response = await getQuotes()
    quotes.value = response.data
  } catch (error) {
    console.error('Erreur chargement devis:', error)
    toastStore.addToast('Erreur lors du chargement des devis', 'error')
  } finally {
    loading.value = false
  }
}

const viewDetail = (id) => {
  router.push(`/devis/${id}`)
}

const goToSignature = (quote) => {
  // Extraire le token depuis signature_url ou utiliser signature_token
  const token = quote.signature_token
  router.push(`/signature/${token}`)
}

const downloadPdf = async (id) => {
  try {
    const response = await downloadPDF(id)
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `devis_${id}.pdf`)
    document.body.appendChild(link)
    link.click()
    link.remove()
    toastStore.addToast('PDF téléchargé avec succès', 'success')
  } catch (error) {
    console.error('Erreur téléchargement PDF:', error)
    toastStore.addToast('Erreur lors du téléchargement du PDF', 'error')
  }
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
    year: 'numeric'
  })
}

onMounted(() => {
  fetchQuotes()
})
</script>