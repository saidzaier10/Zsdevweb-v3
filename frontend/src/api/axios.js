import axios from 'axios'

// Détecte si on est sur une IP réseau et ajuste l'URL backend
const getBaseURL = () => {
  const viteApiUrl = import.meta.env.VITE_API_URL

  // 1. Priorité absolue à la variable d'environnement
  if (viteApiUrl) {
    return viteApiUrl
  }

  // 2. Fallback dynamique : même hostname que le frontend, mais port 8000
  // Cela fonctionne pour localhost, 127.0.0.1, et les IP réseau (192.168.x.x)
  const hostname = window.location.hostname
  return `http://${hostname}:8000`
}

const apiClient = axios.create({
  baseURL: getBaseURL(),
  headers: {
    'Content-Type': 'application/json',
  },
})

// Intercepteur pour ajouter le token JWT à chaque requête
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('accessToken')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Intercepteur pour gérer les réponses et les erreurs
// En cas d'erreur 401, le token est invalide ou expiré
apiClient.interceptors.response.use(
  (response) => {
    return response
  },
  async (error) => {
    const originalRequest = error.config

    // Si erreur 401 (non autorisé) et qu'on n'a pas déjà essayé de rafraîchir
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        const refreshToken = localStorage.getItem('refreshToken')

        if (refreshToken) {
          // Tenter de rafraîchir le token
          // On utilise axios directement pour éviter une boucle infinie avec l'intercepteur
          const response = await axios.post(`${getBaseURL()}/api/auth/token/refresh/`, {
            refresh: refreshToken
          })

          const { access } = response.data

          // Mettre à jour le token dans le stockage et les headers
          localStorage.setItem('accessToken', access)
          apiClient.defaults.headers.common['Authorization'] = `Bearer ${access}`
          originalRequest.headers['Authorization'] = `Bearer ${access}`

          // Mettre à jour le store Pinia si possible (accès direct au localStorage est le fallback)
          // Note: On ne peut pas importer le store ici facilement sans créer une dépendance circulaire
          // Le store se mettra à jour au prochain chargement ou via un listener storage

          return apiClient(originalRequest)
        }
      } catch (refreshError) {
        // Si le refresh échoue, on déconnecte l'utilisateur
        console.error('Session expirée, déconnexion...', refreshError)
        localStorage.removeItem('accessToken')
        localStorage.removeItem('refreshToken')
        window.location.href = '/login'
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

export default apiClient