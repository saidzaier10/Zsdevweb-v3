import apiClient from './axios'

export default {
  // Récupérer tous les types de projets
  getProjectTypes() {
    return apiClient.get('/api/quotes/project-types/')
  },

  // Récupérer toutes les options de design
  getDesignOptions() {
    return apiClient.get('/api/quotes/design-options/')
  },

  // Récupérer tous les niveaux de complexité
  getComplexityLevels() {
    return apiClient.get('/api/quotes/complexity-levels/')
  },

  // Récupérer toutes les options supplémentaires
  getSupplementaryOptions() {
    return apiClient.get('/api/quotes/supplementary-options/')
  },

  // Créer un devis
  createQuote(quoteData) {
    return apiClient.post('/api/quotes/quotes/', quoteData)
  },

  // Récupérer tous les devis
  getQuotes() {
    return apiClient.get('/api/quotes/quotes/')
  },

  // Récupérer un devis par ID
  getQuote(id) {
    return apiClient.get(`/api/quotes/quotes/${id}/`)
  },
}