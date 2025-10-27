import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './style.css'
import App from './App.vue'
import router from './router'

const pinia = createPinia()
const app = createApp(App)

// IMPORTANT : Pinia AVANT le router
app.use(pinia)
app.use(router)
app.mount('#app')