import apiClient from './axios'

// Company types
export const getCompanyTypes = () => {
  return apiClient.get('/api/quotes/companies/')
}

// Project types
export const getProjectTypes = () => {
  return apiClient.get('/api/quotes/project-types/')
}

// Design options
export const getDesignOptions = () => {
  return apiClient.get('/api/quotes/design-options/')
}

// Features
export const getFeatures = () => {
  return apiClient.get('/api/quotes/features/')
}

// Complexity levels
export const getComplexityLevels = () => {
  return apiClient.get('/api/quotes/complexity-levels/')
}

// Supplementary options
export const getSupplementaryOptions = () => {
  return apiClient.get('/api/quotes/supplementary-options/')
}

// Quotes
export const createQuote = (quoteData) => {
  return apiClient.post('/api/quotes/quotes/', quoteData)
}

export const getAllQuotes = (params = {}) => {
  return apiClient.get('/api/quotes/quotes/', { params })
}

export const getMyQuotes = (status = null) => {
  const params = status ? { status } : {}
  return apiClient.get('/api/quotes/quotes/my-quotes/', { params })
}

export const getQuoteById = (id) => {
  return apiClient.get(`/api/quotes/quotes/${id}/`)
}

export const getPublicQuote = (token) => {
  return apiClient.get(`/api/quotes/quotes/public/${token}/`)
}

export const updateQuote = (id, quoteData) => {
  return apiClient.put(`/api/quotes/quotes/${id}/`, quoteData)
}

export const deleteQuote = (id) => {
  return apiClient.delete(`/api/quotes/quotes/${id}/`)
}

export const duplicateQuote = (id) => {
  return apiClient.post(`/api/quotes/quotes/${id}/duplicate/`)
}

export const downloadQuotePDF = (id) => {
  return apiClient.get(`/api/quotes/quotes/${id}/download-pdf/`, {
    responseType: 'blob'
  })
}

export const sendQuoteEmail = (id) => {
  return apiClient.post(`/api/quotes/quotes/${id}/send-email/`)
}

export const signQuote = (token, signatureData) => {
  return apiClient.post(`/api/quotes/quotes/sign/${token}/`, signatureData)
}

export const getQuoteStatistics = () => {
  return apiClient.get('/api/quotes/quotes/statistics/')
}

// Backward compatibility
export const getQuotes = getAllQuotes
export const getQuote = getQuoteById