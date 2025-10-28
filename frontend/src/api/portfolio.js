import apiClient from './axios'

export const getTechnologies = () => {
  return apiClient.get('/api/portfolio/technologies/')
}

export const getProjects = () => {
  return apiClient.get('/api/portfolio/projects/')
}

export const getProject = (slug) => {
  return apiClient.get(`/api/portfolio/projects/${slug}/`)
}

export const getTestimonials = () => {
  return apiClient.get('/api/portfolio/testimonials/')
}