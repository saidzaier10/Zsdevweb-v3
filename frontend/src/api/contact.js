import apiClient from './axios'

/**
 * Envoyer un message de contact
 * @param {Object} contactData - Les données du formulaire de contact
 * @param {string} contactData.name - Nom complet
 * @param {string} contactData.email - Email
 * @param {string} contactData.phone - Téléphone (optionnel)
 * @param {string} contactData.subject - Sujet du message
 * @param {string} contactData.message - Message
 * @returns {Promise}
 */
export const sendContactMessage = (contactData) => {
  return apiClient.post('/api/portfolio/contact/', contactData)
}

/**
 * Récupérer tous les messages de contact (admin uniquement)
 * @returns {Promise}
 */
export const getAllContactMessages = () => {
  return apiClient.get('/api/portfolio/contact/')
}

/**
 * Récupérer un message de contact par ID (admin uniquement)
 * @param {number} id - ID du message
 * @returns {Promise}
 */
export const getContactMessage = (id) => {
  return apiClient.get(`/api/portfolio/contact/${id}/`)
}

/**
 * Mettre à jour le statut d'un message (admin uniquement)
 * @param {number} id - ID du message
 * @param {Object} data - Données à mettre à jour
 * @returns {Promise}
 */
export const updateContactMessage = (id, data) => {
  return apiClient.patch(`/api/portfolio/contact/${id}/`, data)
}
