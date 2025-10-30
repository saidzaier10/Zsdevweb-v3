import apiClient from './axios'

// ============================================================================
// RÉCUPÉRATION DES DONNÉES DE CONFIGURATION
// ============================================================================

export const getProjectTypes = () => {
  return apiClient.get('/api/project-types/')
}

export const getDesignOptions = () => {
  return apiClient.get('/api/design-options/')
}

export const getComplexityLevels = () => {
  return apiClient.get('/api/complexity-levels/')
}

export const getSupplementaryOptions = () => {
  return apiClient.get('/api/supplementary-options/')
}

export const getQuoteTemplates = () => {
  return apiClient.get('/api/quote-templates/')
}

// ============================================================================
// GESTION DES DEVIS (ADMIN)
// ============================================================================

export const getQuotes = (status = null) => {
  const params = status ? { status } : {}
  return apiClient.get('/api/quotes/', { params })
}

export const getQuote = (id) => {
  return apiClient.get(`/api/quotes/${id}/`)
}

export const createQuote = (quoteData) => {
  return apiClient.post('/api/quotes/', quoteData)
}

export const updateQuote = (id, quoteData) => {
  return apiClient.put(`/api/quotes/${id}/`, quoteData)
}

export const deleteQuote = (id) => {
  return apiClient.delete(`/api/quotes/${id}/`)
}

// ============================================================================
// ACTIONS SUR LES DEVIS
// ============================================================================

export const downloadPDF = (id) => {
  return apiClient.get(`/api/quotes/${id}/download-pdf/`, {
    responseType: 'blob'
  })
}

export const sendEmail = (id) => {
  return apiClient.post(`/api/quotes/${id}/send-email/`)
}

export const duplicateQuote = (id) => {
  return apiClient.post(`/api/quotes/${id}/duplicate/`)
}

export const rejectQuote = (id, reason) => {
  return apiClient.post(`/api/quotes/${id}/reject/`, { reason })
}

// ============================================================================
// DEVIS PUBLICS (SANS AUTHENTIFICATION)
// ============================================================================

export const getPublicQuote = (token) => {
  return apiClient.get(`/api/quotes/public/${token}/`)
}

export const signQuote = (token, signatureData) => {
  return apiClient.post(`/api/quotes/sign/${token}/`, signatureData)
}

// ============================================================================
// STATISTIQUES (ADMIN)
// ============================================================================

export const getQuoteStatistics = () => {
  return apiClient.get('/api/quotes/statistics/')
}

// ============================================================================
// COMPANY
// ============================================================================

export const getCompanyInfo = () => {
  return apiClient.get('/api/company/')
}