/**
 * Composable pour gérer la sélection multiple de devis
 * Principe S (Single Responsibility): Sélection uniquement
 */

import { ref, computed } from 'vue'

export function useQuoteSelection(paginatedQuotes) {
  const selectedQuotes = ref([])

  /**
   * Vérifie si un devis est sélectionné
   */
  const isQuoteSelected = (quoteId) => {
    return selectedQuotes.value.includes(quoteId)
  }

  /**
   * Toggle la sélection d'un devis
   */
  const toggleQuoteSelection = (quoteId) => {
    const index = selectedQuotes.value.indexOf(quoteId)
    if (index > -1) {
      selectedQuotes.value.splice(index, 1)
    } else {
      selectedQuotes.value.push(quoteId)
    }
  }

  /**
   * Vérifie si tous les devis de la page sont sélectionnés
   */
  const isAllSelected = computed(() => {
    if (!paginatedQuotes?.value?.length) return false
    return paginatedQuotes.value.every(quote => selectedQuotes.value.includes(quote.id))
  })

  /**
   * Toggle la sélection de tous les devis de la page
   */
  const toggleSelectAll = () => {
    if (!paginatedQuotes?.value) return

    if (isAllSelected.value) {
      // Désélectionner tous les devis de la page
      paginatedQuotes.value.forEach(quote => {
        const index = selectedQuotes.value.indexOf(quote.id)
        if (index > -1) {
          selectedQuotes.value.splice(index, 1)
        }
      })
    } else {
      // Sélectionner tous les devis de la page
      paginatedQuotes.value.forEach(quote => {
        if (!selectedQuotes.value.includes(quote.id)) {
          selectedQuotes.value.push(quote.id)
        }
      })
    }
  }

  /**
   * Efface toutes les sélections
   */
  const clearSelection = () => {
    selectedQuotes.value = []
  }

  /**
   * Sélectionne tous les devis (toutes pages confondues)
   */
  const selectAll = (allQuotes) => {
    if (!allQuotes?.value) return
    selectedQuotes.value = allQuotes.value.map(q => q.id)
  }

  /**
   * Nombre de devis sélectionnés
   */
  const selectedCount = computed(() => {
    return selectedQuotes.value.length
  })

  /**
   * Vérifie si au moins un devis est sélectionné
   */
  const hasSelection = computed(() => {
    return selectedQuotes.value.length > 0
  })

  return {
    // State
    selectedQuotes,

    // Computed
    isAllSelected,
    selectedCount,
    hasSelection,

    // Methods
    isQuoteSelected,
    toggleQuoteSelection,
    toggleSelectAll,
    clearSelection,
    selectAll
  }
}
