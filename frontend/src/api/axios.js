import axios from 'axios'

// Détecte si on est sur une IP réseau et ajuste l'URL backend
const getBaseURL = () => {
  const viteApiUrl = import.meta.env.VITE_API_URL
  
  // Si on accède au front via une IP réseau (pas localhost)
  if (window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1') {
    // Utilise la même IP mais port 8000 pour le backend
    return `http://${window.location.hostname.replace(/\.\d+$/, '')}.0.3:8000`
  }
  
  return viteApiUrl || 'http://localhost:8000'
}

const apiClient = axios.create({
  baseURL: getBaseURL(),
  headers: {
    'Content-Type': 'application/json',
  },
})

// Intercepteur pour ajouter le token à chaque requête
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

export default apiClient