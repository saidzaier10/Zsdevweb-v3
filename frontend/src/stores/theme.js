import { defineStore } from 'pinia'

export const useThemeStore = defineStore('theme', {
  state: () => ({
    isDark: false
  }),

  actions: {
    toggleDarkMode() {
      this.isDark = !this.isDark
      this.applyTheme()
    },

    setDarkMode(value) {
      this.isDark = value
      this.applyTheme()
    },

    applyTheme() {
      const html = document.documentElement
      
      if (this.isDark) {
        html.classList.add('dark')
        localStorage.setItem('darkMode', 'true')
      } else {
        html.classList.remove('dark')
        localStorage.setItem('darkMode', 'false')
      }
      
      console.log('Theme applied:', this.isDark ? 'dark' : 'light')
      console.log('HTML classes:', html.classList.toString())
    },

    initTheme() {
      // Vérifier le localStorage
      const savedTheme = localStorage.getItem('darkMode')
      
      console.log('Saved theme:', savedTheme)
      
      // Si rien n'est sauvegardé, utiliser light mode par défaut
      if (savedTheme === null) {
        this.isDark = false
      } else {
        this.isDark = savedTheme === 'true'
      }
      
      this.applyTheme()
    }
  }
})