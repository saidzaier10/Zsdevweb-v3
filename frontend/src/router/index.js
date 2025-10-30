import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import { useAuthStore } from '../stores/auth'

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
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Register.vue'),
  },
  {
    path: '/devis',
    name: 'Devis',
    component: () => import('../views/Devis.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/mes-devis',
    name: 'MesDevis',
    component: () => import('../views/MesDevis.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/devis/:id',
    name: 'DevisDetail',
    component: () => import('../views/DevisDetail.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/signature/:token',
    name: 'SignatureDevis',
    component: () => import('../views/SignatureDevis.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/admin/devis',
    name: 'AdminDevis',
    component: () => import('../views/AdminDevis.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/contact',
    name: 'Contact',
    component: () => import('../views/Contact.vue'),
    meta: { requiresAuth: true }
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Guard pour protéger les routes
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const token = localStorage.getItem('accessToken')
  
  if (to.meta.requiresAuth && !token) {
    // Rediriger vers login si auth requise
    next('/login')
  } else if (to.meta.requiresAdmin) {
    // Vérifier si l'utilisateur est admin
    if (!authStore.user || !authStore.user.is_staff) {
      next('/')
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router