import apiClient from './axios'

// Catégories de projets
export const getCategories = () => {
  return apiClient.get('/api/quotes/categories/')
}

export const getCategoryBySlug = (slug) => {
  return apiClient.get(`/api/quotes/categories/${slug}/`)
}

// Configuration des types de projets
export const getProjectTypes = (categorySlug = null) => {
  const params = categorySlug ? { category: categorySlug } : {}
  return apiClient.get('/api/quotes/project-types/', { params })
}

export const getDesignOptions = () => {
  return apiClient.get('/api/quotes/design-options/')
}

export const getComplexityLevels = () => {
  return apiClient.get('/api/quotes/complexity-levels/')
}

export const getSupplementaryOptions = (categorySlug = null) => {
  const params = categorySlug ? { category: categorySlug } : {}
  return apiClient.get('/api/quotes/supplementary-options/', { params })
}

// Gestion des devis
export const createQuote = (quoteData) => {
  return apiClient.post('/api/quotes/quotes/', quoteData)
}

// Récupérer tous les devis (admin uniquement)
export const getAllQuotes = () => {
  return apiClient.get('/api/quotes/quotes/')
}

// Récupérer les devis de l'utilisateur connecté
export const getMyQuotes = (status = null) => {
  const params = status ? { status } : {}
  return apiClient.get('/api/quotes/quotes/my-quotes/', { params })
}

// Récupérer un devis par ID
export const getQuote = (id) => {
  return apiClient.get(`/api/quotes/quotes/${id}/`)
}

// Récupérer un devis par token (pour signature publique)
export const getQuoteByToken = (token) => {
  return apiClient.get(`/api/quotes/quotes/public/${token}/`)
}

// Envoyer un devis par email
export const sendQuote = (id) => {
  return apiClient.post(`/api/quotes/quotes/${id}/send-email/`)
}

// Télécharger le PDF d'un devis
export const downloadQuotePDF = (id) => {
  return apiClient.get(`/api/quotes/quotes/${id}/download-pdf/`, {
    responseType: 'blob'
  })
}

// Signer un devis
export const signQuote = (token, signatureData) => {
  return apiClient.post(`/api/quotes/quotes/sign/${token}/`, signatureData)
}

// Refuser un devis (requiert l'ID du devis)
export const rejectQuote = (quoteId, payload = {}) => {
  return apiClient.post(`/api/quotes/quotes/${quoteId}/reject/`, payload)
}

// Dupliquer un devis
export const duplicateQuote = (id) => {
  return apiClient.post(`/api/quotes/quotes/${id}/duplicate/`)
}

// Mettre à jour un devis (admin uniquement)
export const updateQuote = (id, quoteData) => {
  return apiClient.put(`/api/quotes/quotes/${id}/`, quoteData)
}

// Mettre à jour partiellement un devis (admin uniquement)
export const patchQuote = (id, partialData) => {
  return apiClient.patch(`/api/quotes/quotes/${id}/`, partialData)
}

// Statistiques (admin uniquement)
export const getStatistics = () => {
  return apiClient.get('/api/quotes/quotes/statistics/')
}

// Supprimer plusieurs devis (admin uniquement)
export const bulkDeleteQuotes = (ids) => {
  return apiClient.post('/api/quotes/quotes/bulk-delete/', { ids })
}
