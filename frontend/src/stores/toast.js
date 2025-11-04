import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useToastStore = defineStore('toast', () => {
  const toasts = ref([])
  let nextId = 1

  const addToast = ({ type = 'info', title = '', message = '', duration = 5000 }) => {
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
   * Alias compatible avec l'ancien usage (type, title, message, duration)
   */
  const show = (type, title, message = '', duration = 5000) => {
    return addToast({ type, title, message, duration })
  }

  /**
   * Nouvelle API : toastStore.showToast(message, type?, options?)
   */
  const showToast = (message, type = 'info', options = {}) => {
    const opts = typeof options === 'object' && options !== null ? options : {}
    const duration = opts.duration ?? opts.timeout ?? 5000
    const title = opts.title ?? message
    const description = opts.description ?? opts.message ?? (opts.title ? message : '')

    return addToast({
      type,
      title,
      message: description,
      duration
    })
  }

  const success = (title, message = '', duration = 5000) => addToast({ type: 'success', title, message, duration })
  const error = (title, message = '', duration = 7000) => addToast({ type: 'error', title, message, duration })
  const warning = (title, message = '', duration = 6000) => addToast({ type: 'warning', title, message, duration })
  const info = (title, message = '', duration = 5000) => addToast({ type: 'info', title, message, duration })

  const remove = (id) => {
    const index = toasts.value.findIndex((t) => t.id === id)
    if (index !== -1) {
      toasts.value.splice(index, 1)
    }
  }

  const clear = () => {
    toasts.value = []
  }

  const removeToast = remove

  return {
    toasts,
    show,
    showToast,
    success,
    error,
    warning,
    info,
    remove,
    removeToast,
    clear
  }
})
