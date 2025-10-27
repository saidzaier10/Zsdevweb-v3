import apiClient from './axios'

export default {
  // Inscription
  register(userData) {
    return apiClient.post('/api/auth/register/', userData)
  },

  // Connexion
  login(credentials) {
    return apiClient.post('/api/auth/login/', credentials)
  },

  // Rafraîchir le token
  refreshToken(refresh) {
    return apiClient.post('/api/auth/token/refresh/', { refresh })
  },

  // Obtenir le profil utilisateur
  getProfile() {
    return apiClient.get('/api/auth/profile/')
  },

  // Déconnexion
  logout(refreshToken) {
    return apiClient.post('/api/auth/logout/', { refresh: refreshToken })
  },
}