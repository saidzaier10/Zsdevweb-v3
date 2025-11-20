/**
 * Composable pour gérer les erreurs de manière centralisée
 * Principe: Uniformiser la gestion des erreurs dans toute l'application
 */

import { useToastStore } from '@/stores/toast'
import { ERROR_MESSAGES } from '@/utils/constants'

/**
 * Hook pour gérer les erreurs et les notifications de succès
 * @returns {Object} Fonctions de gestion d'erreurs et de succès
 */
export function useErrorHandler() {
  const toastStore = useToastStore()

  /**
   * Gère une erreur et affiche un toast
   * @param {Error|Object} error - Erreur à gérer
   * @param {string|null} customMessage - Message personnalisé (optionnel)
   * @param {Object} options - Options supplémentaires
   */
  const handleError = (error, customMessage = null, options = {}) => {
    const { logToConsole = true, duration = 7000 } = options

    // Logger l'erreur dans la console pour le debug
    if (logToConsole) {
      console.error('Error caught by useErrorHandler:', error)
    }

    // Déterminer le message d'erreur approprié
    let message = customMessage || ERROR_MESSAGES.GENERIC_ERROR

    // Extraire le message d'erreur de la réponse API
    if (error?.response?.data) {
      const data = error.response.data

      // Différents formats possibles de réponse d'erreur
      if (data.error) {
        message = data.error
      } else if (data.detail) {
        message = data.detail
      } else if (data.message) {
        message = data.message
      } else if (typeof data === 'string') {
        message = data
      } else if (data.non_field_errors) {
        message = Array.isArray(data.non_field_errors)
          ? data.non_field_errors.join(', ')
          : data.non_field_errors
      }
      // Gérer les erreurs de validation de champs
      else if (typeof data === 'object') {
        const firstErrorField = Object.keys(data)[0]
        if (firstErrorField && data[firstErrorField]) {
          const errorValue = data[firstErrorField]
          message = Array.isArray(errorValue) ? errorValue[0] : errorValue
        }
      }
    }
    // Erreur réseau ou autre
    else if (error?.message) {
      message = error.message
    }
    // Gérer les erreurs HTTP spécifiques
    else if (error?.response?.status) {
      const status = error.response.status
      switch (status) {
        case 401:
          message = customMessage || ERROR_MESSAGES.UNAUTHORIZED
          break
        case 404:
          message = customMessage || ERROR_MESSAGES.NOT_FOUND
          break
        case 500:
        case 502:
        case 503:
          message = customMessage || ERROR_MESSAGES.SERVER_ERROR
          break
        default:
          message = customMessage || ERROR_MESSAGES.GENERIC_ERROR
      }
    }

    // Afficher le toast d'erreur
    toastStore.showToast(message, 'error', { duration })

    return message
  }

  /**
   * Affiche un message de succès
   * @param {string} message - Message de succès
   * @param {Object} options - Options supplémentaires
   */
  const handleSuccess = (message, options = {}) => {
    const { duration = 5000 } = options

    toastStore.showToast(message, 'success', { duration })
  }

  /**
   * Affiche un message d'avertissement
   * @param {string} message - Message d'avertissement
   * @param {Object} options - Options supplémentaires
   */
  const handleWarning = (message, options = {}) => {
    const { duration = 6000 } = options

    toastStore.showToast(message, 'warning', { duration })
  }

  /**
   * Affiche un message d'information
   * @param {string} message - Message d'information
   * @param {Object} options - Options supplémentaires
   */
  const handleInfo = (message, options = {}) => {
    const { duration = 5000 } = options

    toastStore.showToast(message, 'info', { duration })
  }

  /**
   * Gère les erreurs de validation de formulaire
   * @param {Object} errors - Objet d'erreurs { field: error }
   * @returns {string} Premier message d'erreur trouvé
   */
  const handleValidationErrors = (errors) => {
    if (!errors || typeof errors !== 'object') return null

    const firstErrorField = Object.keys(errors)[0]
    if (firstErrorField && errors[firstErrorField]) {
      const message = errors[firstErrorField]
      toastStore.showToast(message, 'error', { duration: 7000 })
      return message
    }

    return null
  }

  /**
   * Wrapper pour exécuter une fonction avec gestion d'erreur automatique
   * @param {Function} fn - Fonction async à exécuter
   * @param {Object} options - Options
   * @returns {Promise} Résultat de la fonction ou undefined en cas d'erreur
   */
  const withErrorHandling = async (fn, options = {}) => {
    const { errorMessage = null, showError = true, rethrow = false } = options

    try {
      return await fn()
    } catch (error) {
      if (showError) {
        handleError(error, errorMessage)
      }

      if (rethrow) {
        throw error
      }

      return undefined
    }
  }

  return {
    handleError,
    handleSuccess,
    handleWarning,
    handleInfo,
    handleValidationErrors,
    withErrorHandling
  }
}
