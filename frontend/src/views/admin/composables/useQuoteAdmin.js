/**
 * Composable pour gérer la logique métier des devis admin
 * Principe S (Single Responsibility): Gestion des opérations sur les devis uniquement
 */

import { ref } from 'vue'
import { getAllQuotes, sendQuote as sendQuoteAPI, getStatistics, downloadQuotePDF, patchQuote } from '@/api/quotes'
import { useApi } from '@/composables/useApi'
import { SUCCESS_MESSAGES } from '@/utils/constants'

export function useQuoteAdmin() {
  const { loading, get, callApi, handleSuccess, handleError } = useApi()

  const quotes = ref([])
  const statistics = ref(null)
  const sending = ref(null)
  const downloading = ref(null)
  const savingQuote = ref(false)

  /**
   * Charge tous les devis
   */
  const loadQuotes = async () => {
    try {
      const data = await get(
        () => getAllQuotes(),
        { errorMessage: 'Erreur lors du chargement des devis' }
      )

      quotes.value = Array.isArray(data) ? data : (data.results || [])
    } catch (error) {
      quotes.value = []
    }
  }

  /**
   * Charge les statistiques
   */
  const loadStatistics = async () => {
    try {
      const data = await get(
        () => getStatistics(),
        { showErrorToast: false }
      )
      statistics.value = data
    } catch (error) {
      console.error('Erreur lors du chargement des statistiques:', error)
      statistics.value = null
    }
  }

  /**
   * Charge les données (quotes + stats)
   */
  const loadData = async () => {
    await Promise.all([loadQuotes(), loadStatistics()])
  }

  /**
   * Envoie un devis
   */
  const sendQuote = async (quoteId) => {
    try {
      sending.value = quoteId

      await callApi(
        () => sendQuoteAPI(quoteId),
        {
          successMessage: 'Devis envoyé avec succès',
          errorMessage: 'Erreur lors de l\'envoi du devis'
        }
      )

      await loadData()
    } finally {
      sending.value = null
    }
  }

  /**
   * Télécharge le PDF d'un devis
   */
  const downloadPDF = async (quoteId, quoteNumber) => {
    try {
      downloading.value = quoteId

      const response = await callApi(
        () => downloadQuotePDF(quoteId),
        {
          successMessage: 'PDF téléchargé avec succès',
          errorMessage: 'Erreur lors du téléchargement du PDF'
        }
      )

      // Création et téléchargement du blob
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

  /**
   * Sauvegarde les modifications d'un devis
   */
  const saveQuote = async (quoteId, updateData) => {
    try {
      savingQuote.value = true

      await callApi(
        () => patchQuote(quoteId, updateData),
        {
          successMessage: updateData.status === 'draft'
            ? 'Devis mis à jour et repassé en brouillon. Vous devez le renvoyer au client pour signature.'
            : 'Devis mis à jour avec succès',
          errorMessage: 'Erreur lors de la mise à jour du devis'
        }
      )

      await loadData()
      return true
    } catch (error) {
      return false
    } finally {
      savingQuote.value = false
    }
  }

  /**
   * Envoie plusieurs devis en masse
   */
  const bulkSendQuotes = async (quoteIds) => {
    let successCount = 0
    let errorCount = 0

    for (const quoteId of quoteIds) {
      try {
        await sendQuoteAPI(quoteId)
        successCount++
      } catch (error) {
        errorCount++
        console.error(`Erreur lors de l'envoi du devis ${quoteId}:`, error)
      }
    }

    if (successCount > 0) {
      handleSuccess(`${successCount} devis envoyés avec succès`)
    }
    if (errorCount > 0) {
      handleError(new Error(`${errorCount} devis n'ont pas pu être envoyés`))
    }

    await loadData()
    return { successCount, errorCount }
  }

  return {
    // States
    quotes,
    statistics,
    loading,
    sending,
    downloading,
    savingQuote,

    // Methods
    loadQuotes,
    loadStatistics,
    loadData,
    sendQuote,
    downloadPDF,
    saveQuote,
    bulkSendQuotes
  }
}
