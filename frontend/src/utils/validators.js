/**
 * Fonctions de validation centralisées
 * Élimine la duplication de code pour la validation des formulaires
 */

import { VALIDATION_REGEX, ERROR_MESSAGES } from './constants'

/**
 * Vérifie si une valeur est vide
 * @param {*} value - Valeur à vérifier
 * @returns {boolean} True si vide
 */
export const isEmpty = (value) => {
  if (value === null || value === undefined) return true
  if (typeof value === 'string') return value.trim() === ''
  if (Array.isArray(value)) return value.length === 0
  if (typeof value === 'object') return Object.keys(value).length === 0
  return false
}

/**
 * Valide un champ requis
 * @param {*} value - Valeur à valider
 * @param {string} customMessage - Message d'erreur personnalisé
 * @returns {Object} { valid: boolean, error: string|null }
 */
export const required = (value, customMessage = null) => {
  const isValid = !isEmpty(value)
  return {
    valid: isValid,
    error: isValid ? null : (customMessage || ERROR_MESSAGES.REQUIRED_FIELD)
  }
}

/**
 * Valide une adresse email
 * @param {string} email - Email à valider
 * @param {boolean} isRequired - Si le champ est requis
 * @returns {Object} { valid: boolean, error: string|null }
 */
export const validateEmail = (email, isRequired = true) => {
  // Si non requis et vide, c'est valide
  if (!isRequired && isEmpty(email)) {
    return { valid: true, error: null }
  }

  // Vérification si requis
  if (isRequired && isEmpty(email)) {
    return { valid: false, error: ERROR_MESSAGES.REQUIRED_FIELD }
  }

  // Validation du format
  const isValid = VALIDATION_REGEX.EMAIL.test(email)
  return {
    valid: isValid,
    error: isValid ? null : ERROR_MESSAGES.INVALID_EMAIL
  }
}

/**
 * Valide un numéro de téléphone français
 * @param {string} phone - Téléphone à valider
 * @param {boolean} isRequired - Si le champ est requis
 * @returns {Object} { valid: boolean, error: string|null }
 */
export const validatePhone = (phone, isRequired = true) => {
  // Si non requis et vide, c'est valide
  if (!isRequired && isEmpty(phone)) {
    return { valid: true, error: null }
  }

  // Vérification si requis
  if (isRequired && isEmpty(phone)) {
    return { valid: false, error: ERROR_MESSAGES.REQUIRED_FIELD }
  }

  // Validation du format
  const isValid = VALIDATION_REGEX.PHONE_FR.test(phone)
  return {
    valid: isValid,
    error: isValid ? null : ERROR_MESSAGES.INVALID_PHONE
  }
}

/**
 * Valide un mot de passe
 * @param {string} password - Mot de passe à valider
 * @returns {Object} { valid: boolean, error: string|null }
 */
export const validatePassword = (password) => {
  if (isEmpty(password)) {
    return { valid: false, error: ERROR_MESSAGES.REQUIRED_FIELD }
  }

  const isValid = VALIDATION_REGEX.PASSWORD.test(password)
  return {
    valid: isValid,
    error: isValid ? null : 'Le mot de passe doit contenir au moins 8 caractères, une majuscule, une minuscule et un chiffre'
  }
}

/**
 * Valide la longueur minimale d'une chaîne
 * @param {string} value - Valeur à valider
 * @param {number} minLength - Longueur minimale
 * @returns {Object} { valid: boolean, error: string|null }
 */
export const minLength = (value, minLength) => {
  if (isEmpty(value)) {
    return { valid: false, error: ERROR_MESSAGES.REQUIRED_FIELD }
  }

  const isValid = value.length >= minLength
  return {
    valid: isValid,
    error: isValid ? null : ERROR_MESSAGES.MIN_LENGTH(minLength)
  }
}

/**
 * Valide la longueur maximale d'une chaîne
 * @param {string} value - Valeur à valider
 * @param {number} maxLength - Longueur maximale
 * @returns {Object} { valid: boolean, error: string|null }
 */
export const maxLength = (value, maxLength) => {
  if (isEmpty(value)) return { valid: true, error: null }

  const isValid = value.length <= maxLength
  return {
    valid: isValid,
    error: isValid ? null : ERROR_MESSAGES.MAX_LENGTH(maxLength)
  }
}

/**
 * Valide qu'une valeur est un nombre
 * @param {*} value - Valeur à valider
 * @param {Object} options - Options de validation
 * @returns {Object} { valid: boolean, error: string|null }
 */
export const validateNumber = (value, options = {}) => {
  const { min = null, max = null, isRequired = true } = options

  if (!isRequired && isEmpty(value)) {
    return { valid: true, error: null }
  }

  if (isRequired && isEmpty(value)) {
    return { valid: false, error: ERROR_MESSAGES.REQUIRED_FIELD }
  }

  const num = Number(value)
  if (isNaN(num)) {
    return { valid: false, error: 'Doit être un nombre valide' }
  }

  if (min !== null && num < min) {
    return { valid: false, error: `Doit être supérieur ou égal à ${min}` }
  }

  if (max !== null && num > max) {
    return { valid: false, error: `Doit être inférieur ou égal à ${max}` }
  }

  return { valid: true, error: null }
}

/**
 * Valide un montant (nombre positif avec maximum 2 décimales)
 * @param {*} value - Montant à valider
 * @param {boolean} isRequired - Si le champ est requis
 * @returns {Object} { valid: boolean, error: string|null }
 */
export const validateAmount = (value, isRequired = true) => {
  if (!isRequired && isEmpty(value)) {
    return { valid: true, error: null }
  }

  if (isRequired && isEmpty(value)) {
    return { valid: false, error: ERROR_MESSAGES.REQUIRED_FIELD }
  }

  const num = Number(value)
  if (isNaN(num)) {
    return { valid: false, error: 'Doit être un montant valide' }
  }

  if (num < 0) {
    return { valid: false, error: 'Le montant doit être positif' }
  }

  // Vérifier max 2 décimales
  const decimals = (value.toString().split('.')[1] || '').length
  if (decimals > 2) {
    return { valid: false, error: 'Maximum 2 décimales autorisées' }
  }

  return { valid: true, error: null }
}

/**
 * Valide un pourcentage (0-100)
 * @param {*} value - Pourcentage à valider
 * @param {boolean} isRequired - Si le champ est requis
 * @returns {Object} { valid: boolean, error: string|null }
 */
export const validatePercentage = (value, isRequired = true) => {
  const result = validateNumber(value, { min: 0, max: 100, isRequired })

  if (!result.valid && result.error.includes('supérieur')) {
    result.error = 'Le pourcentage doit être entre 0 et 100'
  }

  return result
}

/**
 * Valide une URL
 * @param {string} url - URL à valider
 * @param {boolean} isRequired - Si le champ est requis
 * @returns {Object} { valid: boolean, error: string|null }
 */
export const validateURL = (url, isRequired = true) => {
  if (!isRequired && isEmpty(url)) {
    return { valid: true, error: null }
  }

  if (isRequired && isEmpty(url)) {
    return { valid: false, error: ERROR_MESSAGES.REQUIRED_FIELD }
  }

  try {
    new URL(url)
    return { valid: true, error: null }
  } catch {
    return { valid: false, error: 'URL invalide' }
  }
}

/**
 * Valide un formulaire complet
 * @param {Object} formData - Données du formulaire
 * @param {Object} validationRules - Règles de validation { field: [validators] }
 * @returns {Object} { valid: boolean, errors: Object }
 *
 * @example
 * const rules = {
 *   email: [(v) => validateEmail(v, true)],
 *   phone: [(v) => validatePhone(v, false)],
 *   amount: [(v) => validateAmount(v, true)]
 * }
 * const result = validateForm(formData, rules)
 */
export const validateForm = (formData, validationRules) => {
  const errors = {}
  let isValid = true

  for (const [field, validators] of Object.entries(validationRules)) {
    const value = formData[field]

    // Exécuter tous les validateurs pour ce champ
    for (const validator of validators) {
      const result = validator(value)

      if (!result.valid) {
        errors[field] = result.error
        isValid = false
        break // Arrêter au premier échec pour ce champ
      }
    }
  }

  return { valid: isValid, errors }
}

/**
 * Valide les données d'un devis
 * @param {Object} quoteData - Données du devis
 * @returns {Object} { valid: boolean, errors: Object }
 */
export const validateQuoteData = (quoteData) => {
  const rules = {
    client_name: [(v) => required(v, 'Le nom du client est requis')],
    client_email: [(v) => validateEmail(v, true)],
    client_phone: [(v) => validatePhone(v, false)],
    project_description: [(v) => required(v, 'La description du projet est requise')],
    project_type: [(v) => required(v, 'Le type de projet est requis')]
  }

  // Validation de la remise si présente
  if (quoteData.discount_type) {
    if (quoteData.discount_type === 'percent') {
      rules.discount_value = [(v) => validatePercentage(v, true)]
    } else if (quoteData.discount_type === 'fixed') {
      rules.discount_value = [(v) => validateAmount(v, true)]
    }
  }

  return validateForm(quoteData, rules)
}

/**
 * Valide les données de contact
 * @param {Object} contactData - Données de contact
 * @returns {Object} { valid: boolean, errors: Object }
 */
export const validateContactData = (contactData) => {
  const rules = {
    name: [(v) => required(v, 'Le nom est requis')],
    email: [(v) => validateEmail(v, true)],
    subject: [(v) => required(v, 'Le sujet est requis')],
    message: [
      (v) => required(v, 'Le message est requis'),
      (v) => minLength(v, 10)
    ]
  }

  if (contactData.phone) {
    rules.phone = [(v) => validatePhone(v, false)]
  }

  return validateForm(contactData, rules)
}
