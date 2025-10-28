import apiClient from './axios'

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

export const createQuote = (quoteData) => {
  return apiClient.post('/api/quotes/quotes/', quoteData)
}

export const getQuotes = () => {
  return apiClient.get('/api/quotes/quotes/')
}

export const getQuote = (id) => {
  return apiClient.get(`/api/quotes/quotes/${id}/`)
}