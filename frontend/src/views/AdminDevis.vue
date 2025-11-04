<template>
  <div class="min-h-screen bg-gray-50 dark:bg-dark-900 py-12 transition-colors duration-200">
    <div class="container mx-auto px-4 lg:px-8">
      <!-- En-tête -->
      <div class="mb-8">
        <h1 class="text-4xl font-display font-bold gradient-text mb-2">Administration des Devis</h1>
        <p class="text-dark-600 dark:text-dark-300">Gérez tous les devis de la plateforme</p>
      </div>

      <!-- Statistiques -->
      <div v-if="statistics" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <div class="bg-white dark:bg-dark-800 rounded-xl shadow-sm p-6 border border-gray-200 dark:border-dark-700">
          <div class="flex items-center justify-between mb-2">
            <h3 class="text-sm font-medium text-dark-600 dark:text-dark-400">Total</h3>
            <svg class="w-8 h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
            </svg>
          </div>
          <p class="text-3xl font-bold text-dark-800 dark:text-dark-100">{{ statistics.total_quotes }}</p>
        </div>

        <div class="bg-white dark:bg-dark-800 rounded-xl shadow-sm p-6 border border-gray-200 dark:border-dark-700">
          <div class="flex items-center justify-between mb-2">
            <h3 class="text-sm font-medium text-dark-600 dark:text-dark-400">Envoyés</h3>
            <svg class="w-8 h-8 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
            </svg>
          </div>
          <p class="text-3xl font-bold text-dark-800 dark:text-dark-100">{{ countByStatus('sent') }}</p>
        </div>

        <div class="bg-white dark:bg-dark-800 rounded-xl shadow-sm p-6 border border-gray-200 dark:border-dark-700">
          <div class="flex items-center justify-between mb-2">
            <h3 class="text-sm font-medium text-dark-600 dark:text-dark-400">Acceptés</h3>
            <svg class="w-8 h-8 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </div>
          <p class="text-3xl font-bold text-dark-800 dark:text-dark-100">{{ countByStatus('accepted') }}</p>
        </div>

        <div class="bg-white dark:bg-dark-800 rounded-xl shadow-sm p-6 border border-gray-200 dark:border-dark-700">
          <div class="flex items-center justify-between mb-2">
            <h3 class="text-sm font-medium text-dark-600 dark:text-dark-400">Montant total</h3>
            <svg class="w-8 h-8 text-yellow-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </div>
          <p class="text-3xl font-bold text-dark-800 dark:text-dark-100">{{ formatAmount(statistics.total_amount) }} €</p>
        </div>
      </div>

      <!-- Filtres et recherche -->
      <div class="bg-white dark:bg-dark-800 rounded-xl shadow-sm p-6 mb-6 border border-gray-200 dark:border-dark-700">
        <div class="flex flex-col lg:flex-row gap-4">
          <!-- Barre de recherche -->
          <div class="flex-1">
            <div class="relative">
              <svg class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-dark-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
              </svg>
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Rechercher par nom, email, référence..."
                class="w-full pl-10 pr-4 py-2 rounded-lg border border-gray-300 dark:border-dark-600 bg-white dark:bg-dark-700 text-dark-800 dark:text-dark-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              />
            </div>
          </div>

          <!-- Filtre par statut -->
          <select
            v-model="filterStatus"
            class="px-4 py-2 rounded-lg border border-gray-300 dark:border-dark-600 bg-white dark:bg-dark-700 text-dark-800 dark:text-dark-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          >
            <option :value="null">Tous les statuts</option>
            <option value="draft">Brouillons</option>
            <option value="sent">Envoyés</option>
            <option value="viewed">Consultés</option>
            <option value="accepted">Acceptés</option>
            <option value="rejected">Refusés</option>
            <option value="expired">Expirés</option>
          </select>
        </div>
      </div>

      <!-- Chargement -->
      <div v-if="loading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        <p class="mt-4 text-dark-600 dark:text-dark-300">Chargement des devis...</p>
      </div>

      <!-- Table des devis -->
      <div v-else-if="filteredQuotes.length > 0" class="bg-white dark:bg-dark-800 rounded-xl shadow-sm border border-gray-200 dark:border-dark-700 overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-gray-50 dark:bg-dark-700 border-b border-gray-200 dark:border-dark-600">
              <tr>
                <th class="px-6 py-4 text-left text-xs font-semibold text-dark-700 dark:text-dark-300 uppercase tracking-wider">
                  Référence
                </th>
                <th class="px-6 py-4 text-left text-xs font-semibold text-dark-700 dark:text-dark-300 uppercase tracking-wider">
                  Client
                </th>
                <th class="px-6 py-4 text-left text-xs font-semibold text-dark-700 dark:text-dark-300 uppercase tracking-wider">
                  Projet
                </th>
                <th class="px-6 py-4 text-left text-xs font-semibold text-dark-700 dark:text-dark-300 uppercase tracking-wider">
                  Montant
                </th>
                <th class="px-6 py-4 text-left text-xs font-semibold text-dark-700 dark:text-dark-300 uppercase tracking-wider">
                  Date
                </th>
                <th class="px-6 py-4 text-left text-xs font-semibold text-dark-700 dark:text-dark-300 uppercase tracking-wider">
                  Statut
                </th>
                <th class="px-6 py-4 text-right text-xs font-semibold text-dark-700 dark:text-dark-300 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200 dark:divide-dark-600">
              <tr
                v-for="quote in paginatedQuotes"
                :key="quote.id"
                class="hover:bg-gray-50 dark:hover:bg-dark-700/50 transition-colors"
              >
                <td class="px-6 py-4 whitespace-nowrap">
                  <span class="text-sm font-medium text-dark-800 dark:text-dark-100">
                    #{{ quote.quote_number }}
                  </span>
                </td>
                <td class="px-6 py-4">
                  <div class="text-sm">
                    <div class="font-medium text-dark-800 dark:text-dark-100">{{ quote.client_name }}</div>
                    <div class="text-dark-600 dark:text-dark-400">{{ quote.client_email }}</div>
                  </div>
                </td>
                <td class="px-6 py-4">
                  <div class="text-sm text-dark-800 dark:text-dark-100">
                    {{ quote.project_type.name }}
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm">
                    <div class="font-semibold text-dark-800 dark:text-dark-100">
                      {{ quote.total_price }} €
                    </div>
                    <div v-if="quote.discount_amount > 0" class="text-xs text-green-600 dark:text-green-400">
                      Remise: -{{ quote.discount_amount }}€
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span class="text-sm text-dark-600 dark:text-dark-400">
                    {{ formatShortDate(quote.created_at) }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span
                    :class="[
                      'px-3 py-1 rounded-full text-xs font-semibold',
                      getStatusClass(quote.status)
                    ]"
                  >
                    {{ quote.status_display }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-right">
                  <div class="flex items-center justify-end gap-2">
                    <router-link
                      :to="`/devis/${quote.id}`"
                      class="text-primary-600 hover:text-primary-700 dark:text-primary-400 font-medium text-sm"
                    >
                      Voir
                    </router-link>
                    <button
                      @click="openEditModal(quote)"
                      class="text-indigo-600 hover:text-indigo-700 dark:text-indigo-400 font-medium text-sm"
                    >
                      Modifier
                    </button>
                    <button
                      v-if="quote.status === 'draft'"
                      @click="sendQuote(quote.id)"
                      :disabled="sending === quote.id"
                      class="text-green-600 hover:text-green-700 dark:text-green-400 font-medium text-sm disabled:opacity-50"
                    >
                      {{ sending === quote.id ? 'Envoi...' : 'Envoyer' }}
                    </button>
                    <button
                      @click="downloadPDF(quote.id, quote.quote_number)"
                      :disabled="downloading === quote.id"
                      class="text-blue-600 hover:text-blue-700 dark:text-blue-400 font-medium text-sm disabled:opacity-50"
                    >
                      {{ downloading === quote.id ? 'PDF...' : 'PDF' }}
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination -->
        <div v-if="totalPages > 1" class="px-6 py-4 bg-gray-50 dark:bg-dark-700 border-t border-gray-200 dark:border-dark-600">
          <div class="flex items-center justify-between">
            <p class="text-sm text-dark-600 dark:text-dark-400">
              Affichage de {{ startIndex + 1 }} à {{ Math.min(endIndex, filteredQuotes.length) }} sur {{ filteredQuotes.length }} devis
            </p>
            <div class="flex gap-2">
              <button
                @click="currentPage--"
                :disabled="currentPage === 1"
                class="px-3 py-1 rounded bg-white dark:bg-dark-600 border border-gray-300 dark:border-dark-500 text-dark-700 dark:text-dark-300 disabled:opacity-50 hover:bg-gray-50 dark:hover:bg-dark-500 transition-colors"
              >
                Précédent
              </button>
              <span class="px-3 py-1 text-dark-700 dark:text-dark-300">
                Page {{ currentPage }} / {{ totalPages }}
              </span>
              <button
                @click="currentPage++"
                :disabled="currentPage === totalPages"
                class="px-3 py-1 rounded bg-white dark:bg-dark-600 border border-gray-300 dark:border-dark-500 text-dark-700 dark:text-dark-300 disabled:opacity-50 hover:bg-gray-50 dark:hover:bg-dark-500 transition-colors"
              >
                Suivant
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Liste vide -->
      <div v-else class="bg-white dark:bg-dark-800 rounded-xl shadow-sm p-12 text-center border border-gray-200 dark:border-dark-700">
        <svg class="w-16 h-16 mx-auto mb-4 text-gray-400 dark:text-dark-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
        </svg>
        <h3 class="text-xl font-semibold text-dark-700 dark:text-dark-200 mb-2">Aucun devis trouvé</h3>
        <p class="text-dark-600 dark:text-dark-300">Aucun devis ne correspond à vos critères de recherche.</p>
      </div>
    </div>

    <!-- Modale d'édition de devis -->
    <div
      v-if="showEditModal"
      class="fixed inset-0 z-50 overflow-y-auto"
      @click.self="closeEditModal"
    >
      <div class="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
        <!-- Overlay -->
        <div class="fixed inset-0 transition-opacity bg-gray-500 dark:bg-gray-900 bg-opacity-75 dark:bg-opacity-75" @click="closeEditModal"></div>

        <!-- Modal -->
        <div class="inline-block align-bottom bg-white dark:bg-dark-800 rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-2xl sm:w-full">
          <div class="bg-white dark:bg-dark-800 px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <div class="flex items-center justify-between mb-6">
              <h3 class="text-2xl font-bold text-dark-900 dark:text-white">
                Modifier le devis #{{ editingQuote?.quote_number }}
              </h3>
              <button @click="closeEditModal" class="text-gray-400 hover:text-gray-500">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
              </button>
            </div>

            <div v-if="editingQuote" class="space-y-6">
              <!-- Informations client -->
              <div class="space-y-4">
                <h4 class="text-lg font-semibold text-dark-800 dark:text-dark-100">Informations client</h4>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label class="block text-sm font-medium text-dark-700 dark:text-dark-300 mb-2">Nom</label>
                    <input
                      v-model="editForm.client_name"
                      type="text"
                      class="w-full px-3 py-2 border border-gray-300 dark:border-dark-600 rounded-lg bg-white dark:bg-dark-700 text-dark-900 dark:text-white focus:ring-2 focus:ring-primary-500"
                    />
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-dark-700 dark:text-dark-300 mb-2">Email</label>
                    <input
                      v-model="editForm.client_email"
                      type="email"
                      class="w-full px-3 py-2 border border-gray-300 dark:border-dark-600 rounded-lg bg-white dark:bg-dark-700 text-dark-900 dark:text-white focus:ring-2 focus:ring-primary-500"
                    />
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-dark-700 dark:text-dark-300 mb-2">Téléphone</label>
                    <input
                      v-model="editForm.client_phone"
                      type="tel"
                      class="w-full px-3 py-2 border border-gray-300 dark:border-dark-600 rounded-lg bg-white dark:bg-dark-700 text-dark-900 dark:text-white focus:ring-2 focus:ring-primary-500"
                    />
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-dark-700 dark:text-dark-300 mb-2">Entreprise</label>
                    <input
                      v-model="editForm.company_name"
                      type="text"
                      class="w-full px-3 py-2 border border-gray-300 dark:border-dark-600 rounded-lg bg-white dark:bg-dark-700 text-dark-900 dark:text-white focus:ring-2 focus:ring-primary-500"
                    />
                  </div>
                </div>
              </div>

              <!-- Remise (Admin uniquement) -->
              <div class="space-y-4 border-t border-gray-200 dark:border-dark-700 pt-6">
                <h4 class="text-lg font-semibold text-dark-800 dark:text-dark-100">Remise</h4>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div>
                    <label class="block text-sm font-medium text-dark-700 dark:text-dark-300 mb-2">Type de remise</label>
                    <select
                      v-model="editForm.discount_type"
                      class="w-full px-3 py-2 border border-gray-300 dark:border-dark-600 rounded-lg bg-white dark:bg-dark-700 text-dark-900 dark:text-white focus:ring-2 focus:ring-primary-500"
                    >
                      <option value="">Aucune remise</option>
                      <option value="percent">Pourcentage (%)</option>
                      <option value="fixed">Montant fixe (€)</option>
                    </select>
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-dark-700 dark:text-dark-300 mb-2">
                      Valeur {{ editForm.discount_type === 'percent' ? '(%)' : '(€)' }}
                    </label>
                    <input
                      v-model.number="editForm.discount_value"
                      type="number"
                      min="0"
                      :max="editForm.discount_type === 'percent' ? 100 : 999999"
                      step="0.01"
                      :disabled="!editForm.discount_type"
                      class="w-full px-3 py-2 border border-gray-300 dark:border-dark-600 rounded-lg bg-white dark:bg-dark-700 text-dark-900 dark:text-white focus:ring-2 focus:ring-primary-500 disabled:opacity-50"
                    />
                  </div>
                  <div class="md:col-span-3">
                    <label class="block text-sm font-medium text-dark-700 dark:text-dark-300 mb-2">Raison de la remise</label>
                    <input
                      v-model="editForm.discount_reason"
                      type="text"
                      :disabled="!editForm.discount_type"
                      placeholder="Ex: Client fidèle, Promotion, etc."
                      class="w-full px-3 py-2 border border-gray-300 dark:border-dark-600 rounded-lg bg-white dark:bg-dark-700 text-dark-900 dark:text-white focus:ring-2 focus:ring-primary-500 disabled:opacity-50"
                    />
                  </div>
                </div>
                <!-- Aperçu de la remise -->
                <div v-if="editForm.discount_type && editForm.discount_value > 0" class="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-3">
                  <p class="text-sm text-green-800 dark:text-green-200">
                    <strong>Remise appliquée :</strong>
                    <span v-if="editForm.discount_type === 'percent'">{{ editForm.discount_value }}% sur le montant HT</span>
                    <span v-else>{{ editForm.discount_value }}€</span>
                    <span v-if="editForm.discount_reason"> - {{ editForm.discount_reason }}</span>
                  </p>
                </div>
              </div>

              <!-- Description du projet -->
              <div class="space-y-4 border-t border-gray-200 dark:border-dark-700 pt-6">
                <h4 class="text-lg font-semibold text-dark-800 dark:text-dark-100">Description du projet</h4>
                <textarea
                  v-model="editForm.project_description"
                  rows="4"
                  class="w-full px-3 py-2 border border-gray-300 dark:border-dark-600 rounded-lg bg-white dark:bg-dark-700 text-dark-900 dark:text-white focus:ring-2 focus:ring-primary-500"
                ></textarea>
              </div>
            </div>
          </div>

          <!-- Actions -->
          <div class="bg-gray-50 dark:bg-dark-700 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse gap-3">
            <button
              @click="saveQuote"
              :disabled="savingQuote"
              class="w-full inline-flex justify-center rounded-lg border border-transparent shadow-sm px-4 py-2 bg-primary-600 text-base font-medium text-white hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 sm:ml-3 sm:w-auto sm:text-sm disabled:opacity-50"
            >
              {{ savingQuote ? 'Enregistrement...' : 'Enregistrer' }}
            </button>
            <button
              @click="closeEditModal"
              :disabled="savingQuote"
              class="mt-3 w-full inline-flex justify-center rounded-lg border border-gray-300 dark:border-dark-600 shadow-sm px-4 py-2 bg-white dark:bg-dark-800 text-base font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-dark-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 sm:mt-0 sm:w-auto sm:text-sm"
            >
              Annuler
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getAllQuotes, sendQuote as sendQuoteAPI, getStatistics, downloadQuotePDF, patchQuote } from '../api/quotes'
import { useToastStore } from '../stores/toast'

const toastStore = useToastStore()

const quotes = ref([])
const statistics = ref(null)
const loading = ref(true)
const searchQuery = ref('')
const filterStatus = ref(null)
const currentPage = ref(1)
const itemsPerPage = 20
const sending = ref(null)
const downloading = ref(null)

// Variables pour la modale d'édition
const showEditModal = ref(false)
const editingQuote = ref(null)
const savingQuote = ref(false)
const editForm = ref({
  client_name: '',
  client_email: '',
  client_phone: '',
  company_name: '',
  project_description: '',
  discount_type: '',
  discount_value: 0,
  discount_reason: ''
})

const filteredQuotes = computed(() => {
  let result = quotes.value

  // Filtre par recherche
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(q =>
      q.quote_number.toLowerCase().includes(query) ||
      q.client_name.toLowerCase().includes(query) ||
      q.client_email.toLowerCase().includes(query) ||
      q.project_type.name.toLowerCase().includes(query)
    )
  }

  // Filtre par statut
  if (filterStatus.value) {
    result = result.filter(q => q.status === filterStatus.value)
  }

  return result
})

const totalPages = computed(() => {
  return Math.ceil(filteredQuotes.value.length / itemsPerPage)
})

const startIndex = computed(() => {
  return (currentPage.value - 1) * itemsPerPage
})

const endIndex = computed(() => {
  return startIndex.value + itemsPerPage
})

const paginatedQuotes = computed(() => {
  return filteredQuotes.value.slice(startIndex.value, endIndex.value)
})

const countByStatus = (status) => {
  return quotes.value.filter(q => q.status === status).length
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

const formatShortDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('fr-FR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  })
}

const formatAmount = (amount) => {
  return parseFloat(amount).toFixed(2)
}

const sendQuote = async (quoteId) => {
  try {
    sending.value = quoteId
    await sendQuoteAPI(quoteId)
    toastStore.showToast('Devis envoyé avec succès', 'success')
    await loadQuotes()
    await loadStatistics()
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
    const response = await getAllQuotes()
    quotes.value = response.data
  } catch (error) {
    console.error('Erreur lors du chargement des devis:', error)
    toastStore.showToast('Erreur lors du chargement des devis', 'error')
  }
}

const loadStatistics = async () => {
  try {
    const response = await getStatistics()
    statistics.value = response.data
  } catch (error) {
    console.error('Erreur lors du chargement des statistiques:', error)
  }
}

const loadData = async () => {
  try {
    loading.value = true
    await Promise.all([loadQuotes(), loadStatistics()])
  } finally {
    loading.value = false
  }
}

// Fonctions de gestion de la modale d'édition
const openEditModal = (quote) => {
  editingQuote.value = quote
  editForm.value = {
    client_name: quote.client_name || '',
    client_email: quote.client_email || '',
    client_phone: quote.client_phone || '',
    company_name: quote.company_name || '',
    project_description: quote.project_description || '',
    discount_type: quote.discount_type || '',
    discount_value: quote.discount_value || 0,
    discount_reason: quote.discount_reason || ''
  }
  showEditModal.value = true
}

const closeEditModal = () => {
  showEditModal.value = false
  editingQuote.value = null
  savingQuote.value = false
}

const saveQuote = async () => {
  if (!editingQuote.value) return

  try {
    savingQuote.value = true

    // Préparer les données à envoyer
    const updateData = {
      client_name: editForm.value.client_name,
      client_email: editForm.value.client_email,
      client_phone: editForm.value.client_phone,
      company_name: editForm.value.company_name,
      project_description: editForm.value.project_description,
      discount_type: editForm.value.discount_type || '',
      discount_value: editForm.value.discount_value || 0,
      discount_reason: editForm.value.discount_reason || ''
    }

    // Si pas de remise, on met les valeurs à zéro
    if (!updateData.discount_type) {
      updateData.discount_value = 0
      updateData.discount_reason = ''
    }

    await patchQuote(editingQuote.value.id, updateData)

    toastStore.showToast('Devis mis à jour avec succès', 'success')
    closeEditModal()

    // Recharger les données
    await loadQuotes()
    await loadStatistics()
  } catch (error) {
    console.error('Erreur lors de la mise à jour du devis:', error)
    toastStore.showToast(
      error.response?.data?.error || 'Erreur lors de la mise à jour du devis',
      'error'
    )
  } finally {
    savingQuote.value = false
  }
}

onMounted(() => {
  loadData()
})
</script>
