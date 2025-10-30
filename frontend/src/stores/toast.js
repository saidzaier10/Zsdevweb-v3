import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useToastStore = defineStore('toast', () => {
  const toasts = ref([])
  let nextId = 1

  /**
   * Affiche une notification toast
   * @param {string} type - Type de notification (success, error, warning, info)
   * @param {string} title - Titre de la notification
   * @param {string} message - Message optionnel
   * @param {number} duration - Durée d'affichage en ms (0 = permanent)
   * @returns {number} ID du toast créé
   */
  const show = (type, title, message = '', duration = 5000) => {
    const id = nextId++
    
    toasts.value.push({
      id,
      type,
      title,
      message,
      duration
    })

    return id
  }

  /**
   * Affiche une notification de succès
   * @param {string} title - Titre de la notification
   * @param {string} message - Message optionnel
   * @param {number} duration - Durée d'affichage en ms
   * @returns {number} ID du toast créé
   */
  const success = (title, message = '', duration = 5000) => {
    return show('success', title, message, duration)
  }

  /**
   * Affiche une notification d'erreur
   * @param {string} title - Titre de la notification
   * @param {string} message - Message optionnel
   * @param {number} duration - Durée d'affichage en ms
   * @returns {number} ID du toast créé
   */
  const error = (title, message = '', duration = 7000) => {
    return show('error', title, message, duration)
  }

  /**
   * Affiche une notification d'avertissement
   * @param {string} title - Titre de la notification
   * @param {string} message - Message optionnel
   * @param {number} duration - Durée d'affichage en ms
   * @returns {number} ID du toast créé
   */
  const warning = (title, message = '', duration = 6000) => {
    return show('warning', title, message, duration)
  }

  /**
   * Affiche une notification d'information
   * @param {string} title - Titre de la notification
   * @param {string} message - Message optionnel
   * @param {number} duration - Durée d'affichage en ms
   * @returns {number} ID du toast créé
   */
  const info = (title, message = '', duration = 5000) => {
    return show('info', title, message, duration)
  }

  /**
   * Supprime une notification toast
   * @param {number} id - ID du toast à supprimer
   */
  const remove = (id) => {
    const index = toasts.value.findIndex(t => t.id === id)
    if (index !== -1) {
      toasts.value.splice(index, 1)
    }
  }

  /**
   * Supprime toutes les notifications
   */
  const clear = () => {
    toasts.value = []
  }

  return {
    toasts,
    show,
    success,
    error,
    warning,
    info,
    remove,
    clear
  }
})