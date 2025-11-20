/**
 * Composable pour gérer les états de chargement
 * Principe: Uniformiser la gestion du loading dans toute l'application
 */

import { ref, computed } from 'vue'

/**
 * Hook pour gérer les états de chargement et d'erreur
 * @param {boolean} initialState - État initial du loading
 * @returns {Object} État et fonctions de gestion du loading
 */
export function useLoader(initialState = false) {
  const loading = ref(initialState)
  const error = ref(null)
  const loadingCount = ref(0) // Pour gérer plusieurs opérations simultanées

  /**
   * État de chargement (computed pour réactivité)
   */
  const isLoading = computed(() => loading.value || loadingCount.value > 0)

  /**
   * Démarre le chargement
   */
  const startLoading = () => {
    loading.value = true
    error.value = null
  }

  /**
   * Arrête le chargement
   */
  const stopLoading = () => {
    loading.value = false
  }

  /**
   * Définit une erreur et arrête le chargement
   * @param {Error|string} err - Erreur à définir
   */
  const setError = (err) => {
    error.value = err
    loading.value = false
  }

  /**
   * Réinitialise l'état
   */
  const reset = () => {
    loading.value = initialState
    error.value = null
    loadingCount.value = 0
  }

  /**
   * Incrémente le compteur de chargement
   * Utile pour gérer plusieurs opérations simultanées
   */
  const incrementLoading = () => {
    loadingCount.value++
    error.value = null
  }

  /**
   * Décrémente le compteur de chargement
   */
  const decrementLoading = () => {
    if (loadingCount.value > 0) {
      loadingCount.value--
    }
  }

  /**
   * Wrapper pour exécuter une fonction async avec gestion automatique du loading
   * @param {Function} fn - Fonction async à exécuter
   * @param {Object} options - Options
   * @returns {Promise} Résultat de la fonction
   */
  const withLoading = async (fn, options = {}) => {
    const { useCounter = false, onError = null } = options

    try {
      if (useCounter) {
        incrementLoading()
      } else {
        startLoading()
      }

      const result = await fn()

      if (useCounter) {
        decrementLoading()
      } else {
        stopLoading()
      }

      return result
    } catch (err) {
      setError(err)

      if (useCounter) {
        decrementLoading()
      }

      // Appeler le callback d'erreur si fourni
      if (onError) {
        onError(err)
      }

      throw err
    }
  }

  /**
   * Exécute plusieurs fonctions async en parallèle avec un seul état de loading
   * @param {Array<Function>} fns - Tableau de fonctions async
   * @returns {Promise<Array>} Résultats des fonctions
   */
  const withLoadingParallel = async (fns) => {
    try {
      startLoading()
      const results = await Promise.all(fns.map((fn) => fn()))
      stopLoading()
      return results
    } catch (err) {
      setError(err)
      throw err
    }
  }

  /**
   * Exécute plusieurs fonctions async en séquence avec un seul état de loading
   * @param {Array<Function>} fns - Tableau de fonctions async
   * @returns {Promise<Array>} Résultats des fonctions
   */
  const withLoadingSequential = async (fns) => {
    try {
      startLoading()
      const results = []

      for (const fn of fns) {
        const result = await fn()
        results.push(result)
      }

      stopLoading()
      return results
    } catch (err) {
      setError(err)
      throw err
    }
  }

  return {
    loading,
    isLoading,
    error,
    loadingCount,
    startLoading,
    stopLoading,
    setError,
    reset,
    incrementLoading,
    decrementLoading,
    withLoading,
    withLoadingParallel,
    withLoadingSequential
  }
}

/**
 * Hook simplifié pour un loader basique
 * @param {boolean} initialState - État initial
 * @returns {Object} État et fonction toggle
 */
export function useSimpleLoader(initialState = false) {
  const loading = ref(initialState)

  const toggle = () => {
    loading.value = !loading.value
  }

  const set = (value) => {
    loading.value = value
  }

  return {
    loading,
    toggle,
    set
  }
}
