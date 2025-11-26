import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './style.css'
import App from './App.vue'
import router from './router'

import { vLazyLoad } from './utils/performance'

const pinia = createPinia()
const app = createApp(App)

// IMPORTANT : Pinia AVANT le router
app.use(pinia)
app.use(router)

// Global Directives
app.directive('lazy', vLazyLoad)

app.mount('#app')