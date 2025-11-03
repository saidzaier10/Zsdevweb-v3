import apiClient from './axios'

// Configuration des types de projets
export const getProjectTypes = () => {
  return apiClient.get('/api/quotes/project-types/')
}

export const getDesignOptions = () => {
  return apiClient.get('/api/quotes/design-options/')
}

export const getComplexityLevels = () => {
  return apiClient.get('/api/quotes/complexity-levels/')
}

export const getSupplementaryOptions = () => {
  return apiClient.get('/api/quotes/supplementary-options/')
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
  return apiClient.get('/api/quotes/quotes/my_quotes/', { params })
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

// Refuser un devis
export const rejectQuote = (token) => {
  return apiClient.post(`/api/quotes/quotes/reject/${token}/`)
}

// Dupliquer un devis
export const duplicateQuote = (id) => {
  return apiClient.post(`/api/quotes/quotes/${id}/duplicate/`)
}

// Statistiques (admin uniquement)
export const getStatistics = () => {
  return apiClient.get('/api/quotes/quotes/statistics/')
}