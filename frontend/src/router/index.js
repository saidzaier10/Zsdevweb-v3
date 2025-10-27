import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/portfolio',
    name: 'Portfolio',
    component: () => import('../views/Portfolio.vue'),
  },
  {
    path: '/devis',
    name: 'Devis',
    component: () => import('../views/Devis.vue'),
  },
  {
    path: '/contact',
    name: 'Contact',
    component: () => import('../views/Contact.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router