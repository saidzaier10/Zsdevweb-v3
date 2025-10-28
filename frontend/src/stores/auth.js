import { defineStore } from 'pinia'
import authAPI from '../api/auth'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    accessToken: localStorage.getItem('accessToken') || null,
    refreshToken: localStorage.getItem('refreshToken') || null,
    isAuthenticated: !!localStorage.getItem('accessToken'),
  }),

  actions: {
    async register(userData) {
      try {
        const response = await authAPI.register(userData)
        console.log('Register response:', response.data)
        this.setTokens(response.data.tokens)
        this.user = response.data.user
        return response
      } catch (error) {
        console.error('Register error:', error.response?.data)
        throw error
      }
    },

    async login(credentials) {
      try {
        const response = await authAPI.login(credentials)
        console.log('Login response:', response.data)
        this.setTokens(response.data.tokens)
        this.user = response.data.user
        return response
      } catch (error) {
        console.error('Login error:', error.response?.data)
        throw error
      }
    },

    async fetchUser() {
      try {
        const response = await authAPI.getProfile()
        this.user = response.data
      } catch (error) {
        console.error('Erreur lors de la récupération du profil:', error)
        this.clearAuth()
      }
    },

    async logout() {
      try {
        if (this.refreshToken) {
          await authAPI.logout(this.refreshToken)
        }
      } catch (error) {
        console.error('Erreur lors de la déconnexion:', error)
      } finally {
        this.clearAuth()
      }
    },

    setTokens(tokens) {
      this.accessToken = tokens.access
      this.refreshToken = tokens.refresh
      this.isAuthenticated = true
      localStorage.setItem('accessToken', tokens.access)
      localStorage.setItem('refreshToken', tokens.refresh)
    },

    clearAuth() {
      this.user = null
      this.accessToken = null
      this.refreshToken = null
      this.isAuthenticated = false
      localStorage.removeItem('accessToken')
      localStorage.removeItem('refreshToken')
    },
  },
})