/**
 * Utilitaires de formatage centralisés
 * Élimine la duplication de code pour le formatage des dates, prix, etc.
 */

/**
 * Formate une date au format français court (JJ/MM/AAAA)
 * @param {string|Date} dateString - Date à formater
 * @param {Object} options - Options de formatage supplémentaires
 * @returns {string} Date formatée
 */
export const formatDate = (dateString, options = {}) => {
  if (!dateString) return 'N/A'
  try {
    const date = new Date(dateString)
    if (isNaN(date.getTime())) return 'N/A'

    return date.toLocaleDateString('fr-FR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      ...options
    })
  } catch (error) {
    console.error('Erreur de formatage de date:', error)
    return 'N/A'
  }
}

/**
 * Alias pour formatDate - format court
 * @param {string|Date} dateString - Date à formater
 * @returns {string} Date formatée
 */
export const formatShortDate = (dateString) => formatDate(dateString)

/**
 * Formate une date au format long (Ex: "lundi 14 novembre 2025")
 * @param {string|Date} dateString - Date à formater
 * @returns {string} Date formatée en format long
 */
export const formatLongDate = (dateString) => {
  return formatDate(dateString, {
    weekday: 'long',
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  })
}

/**
 * Formate une date avec l'heure (Ex: "14/11/2025 à 15:30")
 * @param {string|Date} dateString - Date à formater
 * @returns {string} Date et heure formatées
 */
export const formatDateTime = (dateString) => {
  if (!dateString) return 'N/A'
  try {
    const date = new Date(dateString)
    if (isNaN(date.getTime())) return 'N/A'

    return date.toLocaleString('fr-FR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch (error) {
    console.error('Erreur de formatage de date/heure:', error)
    return 'N/A'
  }
}

/**
 * Formate un montant en euros
 * @param {number|string} amount - Montant à formater
 * @param {string} currency - Symbole de la devise (défaut: €)
 * @param {number} decimals - Nombre de décimales (défaut: 2)
 * @returns {string} Montant formaté
 */
export const formatAmount = (amount, currency = '€', decimals = 2) => {
  if (amount === null || amount === undefined || amount === '') return `0.00 ${currency}`

  try {
    const numAmount = typeof amount === 'string' ? parseFloat(amount) : amount
    if (isNaN(numAmount)) return `0.00 ${currency}`

    return `${numAmount.toFixed(decimals)} ${currency}`
  } catch (error) {
    console.error('Erreur de formatage de montant:', error)
    return `0.00 ${currency}`
  }
}

/**
 * Alias pour formatAmount
 */
export const formatPrice = formatAmount

/**
 * Formate un montant en euros avec séparateur de milliers
 * @param {number|string} amount - Montant à formater
 * @returns {string} Montant formaté avec séparateurs
 */
export const formatCurrency = (amount) => {
  if (amount === null || amount === undefined || amount === '') return '0,00 €'

  try {
    const numAmount = typeof amount === 'string' ? parseFloat(amount) : amount
    if (isNaN(numAmount)) return '0,00 €'

    return new Intl.NumberFormat('fr-FR', {
      style: 'currency',
      currency: 'EUR'
    }).format(numAmount)
  } catch (error) {
    console.error('Erreur de formatage de devise:', error)
    return '0,00 €'
  }
}

/**
 * Formate un pourcentage
 * @param {number|string} value - Valeur à formater
 * @param {number} decimals - Nombre de décimales (défaut: 2)
 * @returns {string} Pourcentage formaté
 */
export const formatPercentage = (value, decimals = 2) => {
  if (value === null || value === undefined || value === '') return '0%'

  try {
    const numValue = typeof value === 'string' ? parseFloat(value) : value
    if (isNaN(numValue)) return '0%'

    return `${numValue.toFixed(decimals)}%`
  } catch (error) {
    console.error('Erreur de formatage de pourcentage:', error)
    return '0%'
  }
}

/**
 * Formate un numéro de téléphone français
 * @param {string} phone - Numéro de téléphone
 * @returns {string} Téléphone formaté
 */
export const formatPhone = (phone) => {
  if (!phone) return 'N/A'

  // Supprime tous les caractères non numériques
  const cleaned = phone.replace(/\D/g, '')

  // Formate par groupe de 2
  if (cleaned.length === 10) {
    return cleaned.replace(/(\d{2})(?=\d)/g, '$1 ')
  }

  return phone
}

/**
 * Tronque un texte à une longueur maximale
 * @param {string} text - Texte à tronquer
 * @param {number} maxLength - Longueur maximale
 * @param {string} suffix - Suffixe à ajouter (défaut: '...')
 * @returns {string} Texte tronqué
 */
export const truncate = (text, maxLength = 50, suffix = '...') => {
  if (!text) return ''
  if (text.length <= maxLength) return text

  return text.substring(0, maxLength - suffix.length) + suffix
}

/**
 * Capitalise la première lettre d'une chaîne
 * @param {string} str - Chaîne à capitaliser
 * @returns {string} Chaîne capitalisée
 */
export const capitalize = (str) => {
  if (!str) return ''
  return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase()
}

/**
 * Formate un nombre avec des séparateurs de milliers
 * @param {number|string} number - Nombre à formater
 * @returns {string} Nombre formaté
 */
export const formatNumber = (number) => {
  if (number === null || number === undefined || number === '') return '0'

  try {
    const numValue = typeof number === 'string' ? parseFloat(number) : number
    if (isNaN(numValue)) return '0'

    return new Intl.NumberFormat('fr-FR').format(numValue)
  } catch (error) {
    console.error('Erreur de formatage de nombre:', error)
    return '0'
  }
}
