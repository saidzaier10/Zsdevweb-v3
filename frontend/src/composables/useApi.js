/**
 * Composable pour standardiser les appels API
 * Combine useLoader et useErrorHandler pour une gestion uniforme
 */

import { useLoader } from './useLoader'
import { useErrorHandler } from './useErrorHandler'
import { SUCCESS_MESSAGES } from '@/utils/constants'

/**
 * Hook pour standardiser les appels API avec gestion automatique du loading et des erreurs
 * @param {Object} options - Options par défaut
 * @returns {Object} Fonctions et états pour les appels API
 */
export function useApi(options = {}) {
  const { initialLoading = false } = options

  const { loading, isLoading, error, withLoading, reset } = useLoader(initialLoading)
  const {
    handleError,
    handleSuccess,
    handleWarning,
    handleInfo,
    handleValidationErrors
  } = useErrorHandler()

  /**
   * Effectue un appel API avec gestion automatique du loading et des erreurs
   * @param {Function} apiFunction - Fonction API à appeler
   * @param {Object} callOptions - Options pour cet appel spécifique
   * @returns {Promise} Résultat de l'appel API
   */
  const callApi = async (apiFunction, callOptions = {}) => {
    const {
      successMessage = null,
      errorMessage = null,
      showSuccessToast = !!successMessage,
      showErrorToast = true,
      onSuccess = null,
      onError = null,
      transformResponse = null,
      useCounter = false
    } = callOptions

    try {
      // Exécuter l'appel API avec gestion du loading
      const response = await withLoading(apiFunction, { useCounter })

      // Transformer la réponse si nécessaire
      const result = transformResponse ? transformResponse(response) : response

      // Afficher le message de succès si demandé
      if (showSuccessToast && successMessage) {
        handleSuccess(successMessage)
      }

      // Callback de succès
      if (onSuccess) {
        await onSuccess(result)
      }

      return result
    } catch (err) {
      // Afficher le message d'erreur si demandé
      if (showErrorToast) {
        handleError(err, errorMessage)
      }

      // Callback d'erreur
      if (onError) {
        await onError(err)
      }

      throw err
    }
  }

  /**
   * Effectue un appel API GET
   * @param {Function} apiFunction - Fonction API GET
   * @param {Object} callOptions - Options
   * @returns {Promise} Données récupérées
   */
  const get = async (apiFunction, callOptions = {}) => {
    return callApi(apiFunction, {
      transformResponse: (response) => response.data,
      ...callOptions
    })
  }

  /**
   * Effectue un appel API POST
   * @param {Function} apiFunction - Fonction API POST
   * @param {Object} callOptions - Options
   * @returns {Promise} Données créées
   */
  const post = async (apiFunction, callOptions = {}) => {
    return callApi(apiFunction, {
      successMessage: callOptions.successMessage || SUCCESS_MESSAGES.CREATED,
      transformResponse: (response) => response.data,
      ...callOptions
    })
  }

  /**
   * Effectue un appel API PUT/PATCH
   * @param {Function} apiFunction - Fonction API PUT/PATCH
   * @param {Object} callOptions - Options
   * @returns {Promise} Données mises à jour
   */
  const update = async (apiFunction, callOptions = {}) => {
    return callApi(apiFunction, {
      successMessage: callOptions.successMessage || SUCCESS_MESSAGES.UPDATED,
      transformResponse: (response) => response.data,
      ...callOptions
    })
  }

  /**
   * Effectue un appel API DELETE
   * @param {Function} apiFunction - Fonction API DELETE
   * @param {Object} callOptions - Options
   * @returns {Promise} Résultat de la suppression
   */
  const remove = async (apiFunction, callOptions = {}) => {
    return callApi(apiFunction, {
      successMessage: callOptions.successMessage || SUCCESS_MESSAGES.DELETED,
      ...callOptions
    })
  }

  /**
   * Effectue plusieurs appels API en parallèle
   * @param {Array<Object>} calls - Tableau d'objets { fn, options }
   * @returns {Promise<Array>} Résultats des appels
   */
  const parallel = async (calls) => {
    try {
      loading.value = true

      const promises = calls.map(({ fn, options = {} }) =>
        callApi(fn, { ...options, useCounter: false })
      )

      const results = await Promise.all(promises)
      loading.value = false

      return results
    } catch (err) {
      loading.value = false
      throw err
    }
  }

  /**
   * Effectue plusieurs appels API en séquence
   * @param {Array<Object>} calls - Tableau d'objets { fn, options }
   * @returns {Promise<Array>} Résultats des appels
   */
  const sequential = async (calls) => {
    const results = []

    try {
      loading.value = true

      for (const { fn, options = {} } of calls) {
        const result = await callApi(fn, { ...options, useCounter: false })
        results.push(result)
      }

      loading.value = false
      return results
    } catch (err) {
      loading.value = false
      throw err
    }
  }

  /**
   * Effectue un appel API avec retry automatique
   * @param {Function} apiFunction - Fonction API à appeler
   * @param {Object} callOptions - Options
   * @returns {Promise} Résultat de l'appel
   */
  const withRetry = async (apiFunction, callOptions = {}) => {
    const {
      maxRetries = 3,
      retryDelay = 1000,
      retryOn = [500, 502, 503, 504],
      ...otherOptions
    } = callOptions

    let lastError = null

    for (let attempt = 0; attempt < maxRetries; attempt++) {
      try {
        return await callApi(apiFunction, {
          ...otherOptions,
          showErrorToast: attempt === maxRetries - 1 // Afficher l'erreur seulement au dernier essai
        })
      } catch (err) {
        lastError = err

        // Vérifier si on doit réessayer
        const shouldRetry =
          attempt < maxRetries - 1 &&
          err.response &&
          retryOn.includes(err.response.status)

        if (shouldRetry) {
          // Attendre avant de réessayer
          await new Promise((resolve) => setTimeout(resolve, retryDelay * (attempt + 1)))
        } else {
          throw err
        }
      }
    }

    throw lastError
  }

  return {
    // États
    loading,
    isLoading,
    error,

    // Méthodes principales
    callApi,
    get,
    post,
    update,
    remove,

    // Méthodes avancées
    parallel,
    sequential,
    withRetry,

    // Méthodes utilitaires
    reset,

    // Gestionnaires de messages
    handleError,
    handleSuccess,
    handleWarning,
    handleInfo,
    handleValidationErrors
  }
}
