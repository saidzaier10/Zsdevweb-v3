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
    path: '/admin/devis',
    name: 'AdminDevis',
    component: () => import('../views/AdminDevis.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/signature/:token',
    name: 'SignatureDevis',
    component: () => import('../views/SignatureDevis.vue'),
    meta: { requiresAuth: false } // Route publique accessible via token
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
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// Guard pour protéger les routes
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth) {
    const token = localStorage.getItem('accessToken')
    if (!token) {
      next('/login')
    } else {
      // Vérifier si la route nécessite des droits admin
      if (to.meta.requiresAdmin) {
        // Vérifier si l'utilisateur est admin (à adapter selon votre structure de données)
        const user = authStore.user
        if (user && user.is_staff) {
          next()
        } else {
          // Rediriger vers la page d'accueil si pas admin
          next('/')
        }
      } else {
        next()
      }
    }
  } else {
    next()
  }
})

export default router