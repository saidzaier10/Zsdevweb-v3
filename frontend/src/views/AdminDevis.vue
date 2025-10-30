<template>
  <div class="min-h-screen bg-gray-50 dark:bg-dark-900 py-12">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Administration des Devis</h1>
        <p class="mt-2 text-gray-600 dark:text-gray-400">
          Gérez tous les devis et consultez les statistiques
        </p>
      </div>

      <!-- Statistiques -->
      <div v-if="statistics" class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div class="bg-white dark:bg-dark-800 rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0 bg-indigo-500 rounded-md p-3">
              <svg class="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500 dark:text-gray-400">Total Devis</p>
              <p class="text-2xl font-semibold text-gray-900 dark:text-white">
                {{ statistics.total_quotes }}
              </p>
            </div>
          </div>
        </div>

        <div class="bg-white dark:bg-dark-800 rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0 bg-green-500 rounded-md p-3">
              <svg class="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500 dark:text-gray-400">Acceptés</p>
              <p class="text-2xl font-semibold text-gray-900 dark:text-white">
                {{ statistics.status_breakdown?.accepted || 0 }}
              </p>
            </div>
          </div>
        </div>

        <div class="bg-white dark:bg-dark-800 rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0 bg-yellow-500 rounded-md p-3">
              <svg class="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500 dark:text-gray-400">Taux de conversion</p>
              <p class="text-2xl font-semibold text-gray-900 dark:text-white">
                {{ statistics.conversion_rate }}%
              </p>
            </div>
          </div>
        </div>

        <div class="bg-white dark:bg-dark-800 rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0 bg-purple-500 rounded-md p-3">
              <svg class="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500 dark:text-gray-400">Revenu total</p>
              <p class="text-2xl font-semibold text-gray-900 dark:text-white">
                {{ formatCurrency(statistics.total_amount) }}
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Filtres et recherche -->
      <div class="bg-white dark:bg-dark-800 rounded-lg shadow p-6 mb-6">
        <div class="flex flex-wrap gap-4">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Rechercher un devis..."
            class="flex-1 min-w-[200px] px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 dark:bg-dark-700 dark:text-white"
          />
          <select
            v-model="filterStatus"
            class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 dark:bg-dark-700 dark:text-white"
          >
            <option :value="null">Tous les statuts</option>
            <option value="draft">Brouillon</option>
            <option value="sent">Envoyé</option>
            <option value="viewed">Consulté</option>
            <option value="accepted">Accepté</option>
            <option value="rejected">Refusé</option>
            <option value="expired">Expiré</option>
          </select>
          <button
            @click="fetchQuotes"
            class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
          >
            Actualiser
          </button>
        </div>
      </div>

      <!-- Table des devis -->
      <div class="bg-white dark:bg-dark-800 rounded-lg shadow overflow-hidden">
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
            <thead class="bg-gray-50 dark:bg-dark-700">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Numéro
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Client
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Projet
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Montant
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Statut
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Date
                </th>
                <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody class="bg-white dark:bg-dark-800 divide-y divide-gray-200 dark:divide-gray-700">
              <tr v-for="quote in filteredQuotes" :key="quote.id" class="hover:bg-gray-50 dark:hover:bg-dark-700">
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                  {{ quote.quote_number }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm font-medium text-gray-900 dark:text-white">{{ quote.client_name }}</div>
                  <div class="text-sm text-gray-500 dark:text-gray-400">{{ quote.client_email }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                  {{ quote.project_type_name }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                  {{ quote.total_ttc }} €
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span
                    :class="[
                      'px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full',
                      getStatusClass(quote.status)
                    ]"
                  >
                    {{ quote.status_display }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                  {{ formatDate(quote.created_at) }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <div class="flex justify-end gap-2">
                    <button
                      @click="viewQuote(quote.id)"
                      class="text-indigo-600 hover:text-indigo-900 dark:text-indigo-400"
                      title="Voir"
                    >
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                      </svg>
                    </button>
                    <button
                      @click="duplicateDevis(quote.id)"
                      class="text-blue-600 hover:text-blue-900 dark:text-blue-400"
                      title="Dupliquer"
                    >
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                      </svg>
                    </button>
                    <button
                      @click="downloadPdf(quote.id)"
                      class="text-green-600 hover:text-green-900 dark:text-green-400"
                      title="Télécharger PDF"
                    >
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                    </button>
                    <button
                      @click="deleteDevis(quote.id)"
                      class="text-red-600 hover:text-red-900 dark:text-red-400"
                      title="Supprimer"
                    >
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Empty State -->
        <div v-if="filteredQuotes.length === 0" class="text-center py-12">
          <p class="text-gray-500 dark:text-gray-400">Aucun devis trouvé</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getQuotes, getQuoteStatistics, duplicateQuote, downloadPDF, deleteQuote } from '../api/quotes'
import { useToastStore } from '../stores/toast'

const router = useRouter()
const toastStore = useToastStore()

const quotes = ref([])
const statistics = ref(null)
const searchQuery = ref('')
const filterStatus = ref(null)

const filteredQuotes = computed(() => {
  let result = quotes.value

  // Filtrer par statut
  if (filterStatus.value) {
    result = result.filter(q => q.status === filterStatus.value)
  }

  // Filtrer par recherche
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(q =>
      q.quote_number.toLowerCase().includes(query) ||
      q.client_name.toLowerCase().includes(query) ||
      q.client_email.toLowerCase().includes(query) ||
      q.project_type_name?.toLowerCase().includes(query)
    )
  }

  return result
})

const fetchQuotes = async () => {
  try {
    const response = await getQuotes(filterStatus.value)
    quotes.value = response.data
  } catch (error) {
    console.error('Erreur chargement devis:', error)
    toastStore.addToast('Erreur lors du chargement des devis', 'error')
  }
}

const fetchStatistics = async () => {
  try {
    const response = await getQuoteStatistics()
    statistics.value = response.data
  } catch (error) {
    console.error('Erreur chargement statistiques:', error)
  }
}

const viewQuote = (id) => {
  router.push(`/devis/${id}`)
}

const duplicateDevis = async (id) => {
  if (!confirm('Voulez-vous dupliquer ce devis ?')) return
  
  try {
    await duplicateQuote(id)
    toastStore.addToast('Devis dupliqué avec succès', 'success')
    fetchQuotes()
  } catch (error) {
    console.error('Erreur duplication:', error)
    toastStore.addToast('Erreur lors de la duplication', 'error')
  }
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

const deleteDevis = async (id) => {
  if (!confirm('Voulez-vous vraiment supprimer ce devis ?')) return
  
  try {
    await deleteQuote(id)
    toastStore.addToast('Devis supprimé avec succès', 'success')
    fetchQuotes()
    fetchStatistics()
  } catch (error) {
    console.error('Erreur suppression:', error)
    toastStore.addToast('Erreur lors de la suppression', 'error')
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

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('fr-FR', {
    style: 'currency',
    currency: 'EUR'
  }).format(amount || 0)
}

onMounted(() => {
  fetchQuotes()
  fetchStatistics()
})
</script>