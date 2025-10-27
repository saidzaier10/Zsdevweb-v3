import apiClient from './axios'

export default {
  // Récupérer toutes les technologies
  getTechnologies() {
    return apiClient.get('/api/portfolio/technologies/')
  },

  // Récupérer tous les projets
  getProjects() {
    return apiClient.get('/api/portfolio/projects/')
  },

  // Récupérer un projet par slug
  getProject(slug) {
    return apiClient.get(`/api/portfolio/projects/${slug}/`)
  },

  // Récupérer tous les témoignages
  getTestimonials() {
    return apiClient.get('/api/portfolio/testimonials/')
  },
}