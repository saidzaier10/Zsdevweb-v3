/**
 * Composable pour gérer l'export des devis (Excel & PDF)
 * Principe S (Single Responsibility): Export uniquement
 */

import { useQuoteExport as useQuoteExportOriginal } from '@/composables/useQuoteExport'
import { useErrorHandler } from '@/composables/useErrorHandler'

export function useQuoteExport() {
  const { exportToExcel, exportToPDF } = useQuoteExportOriginal()
  const { handleSuccess, handleWarning } = useErrorHandler()

  /**
   * Exporte les devis en Excel
   */
  const handleExportExcel = (quotes, filename = 'devis_admin') => {
    if (!quotes || quotes.length === 0) {
      handleWarning('Aucun devis à exporter')
      return false
    }

    try {
      const success = exportToExcel(quotes, filename)
      if (success) {
        handleSuccess(`${quotes.length} devis exportés en Excel`)
      }
      return success
    } catch (error) {
      console.error('Erreur lors de l\'export Excel:', error)
      return false
    }
  }

  /**
   * Exporte les devis en PDF avec statistiques
   */
  const handleExportPDF = (quotes, filename = 'rapport_devis_admin') => {
    if (!quotes || quotes.length === 0) {
      handleWarning('Aucun devis à exporter')
      return false
    }

    try {
      // Calcul des statistiques pour le PDF
      const stats = {
        total: quotes.length,
        draft: quotes.filter(q => q.status === 'draft').length,
        sent: quotes.filter(q => q.status === 'sent').length,
        viewed: quotes.filter(q => q.status === 'viewed').length,
        accepted: quotes.filter(q => q.status === 'accepted').length,
        rejected: quotes.filter(q => q.status === 'rejected').length,
        expired: quotes.filter(q => q.status === 'expired').length,
        accepted_revenue: quotes
          .filter(q => q.status === 'accepted')
          .reduce((sum, q) => sum + parseFloat(q.total_price || 0), 0),
        pending_revenue: quotes
          .filter(q => ['sent', 'viewed'].includes(q.status))
          .reduce((sum, q) => sum + parseFloat(q.total_price || 0), 0)
      }

      const success = exportToPDF(quotes, stats, filename)
      if (success) {
        handleSuccess(`Rapport PDF généré pour ${quotes.length} devis`)
      }
      return success
    } catch (error) {
      console.error('Erreur lors de l\'export PDF:', error)
      return false
    }
  }

  return {
    handleExportExcel,
    handleExportPDF
  }
}
