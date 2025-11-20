/**
 * Composable pour gérer le filtrage et la pagination des devis
 * Principe S (Single Responsibility): Filtrage et pagination uniquement
 */

import { ref, computed } from 'vue'
import { PAGINATION } from '@/utils/constants'

export function useQuoteFilters(quotes) {
  const searchQuery = ref('')
  const filterStatus = ref(null)
  const currentPage = ref(1)
  const itemsPerPage = PAGINATION.DEFAULT_PAGE_SIZE

  /**
   * Devis filtrés par recherche et statut
   */
  const filteredQuotes = computed(() => {
    if (!Array.isArray(quotes.value)) return []

    let result = quotes.value

    // Filtre par recherche
    if (searchQuery.value) {
      const query = searchQuery.value.toLowerCase()
      result = result.filter(q =>
        q.quote_number?.toLowerCase().includes(query) ||
        q.client_name?.toLowerCase().includes(query) ||
        q.client_email?.toLowerCase().includes(query) ||
        q.project_type?.name?.toLowerCase().includes(query)
      )
    }

    // Filtre par statut
    if (filterStatus.value) {
      result = result.filter(q => q.status === filterStatus.value)
    }

    return result
  })

  /**
   * Nombre total de pages
   */
  const totalPages = computed(() => {
    return Math.ceil(filteredQuotes.value.length / itemsPerPage)
  })

  /**
   * Index de début de la page courante
   */
  const startIndex = computed(() => {
    return (currentPage.value - 1) * itemsPerPage
  })

  /**
   * Index de fin de la page courante
   */
  const endIndex = computed(() => {
    return startIndex.value + itemsPerPage
  })

  /**
   * Devis paginés
   */
  const paginatedQuotes = computed(() => {
    return filteredQuotes.value.slice(startIndex.value, endIndex.value)
  })

  /**
   * Réinitialise la page à 1 quand les filtres changent
   */
  const resetPage = () => {
    currentPage.value = 1
  }

  /**
   * Va à la page suivante
   */
  const nextPage = () => {
    if (currentPage.value < totalPages.value) {
      currentPage.value++
    }
  }

  /**
   * Va à la page précédente
   */
  const previousPage = () => {
    if (currentPage.value > 1) {
      currentPage.value--
    }
  }

  /**
   * Va à une page spécifique
   */
  const goToPage = (page) => {
    if (page >= 1 && page <= totalPages.value) {
      currentPage.value = page
    }
  }

  return {
    // States
    searchQuery,
    filterStatus,
    currentPage,
    itemsPerPage,

    // Computed
    filteredQuotes,
    paginatedQuotes,
    totalPages,
    startIndex,
    endIndex,

    // Methods
    resetPage,
    nextPage,
    previousPage,
    goToPage
  }
}
