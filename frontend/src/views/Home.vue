<template>
  <div class="min-h-screen transition-colors duration-200">
    <!-- Animated Background (Home only) -->
    <div class="fixed inset-0 z-10 pointer-events-none opacity-100">
      <InteractiveBackground />
    </div>

    <!-- Hero Section -->
    <section
      class="relative bg-gradient-to-br from-primary-600 via-primary-700 to-secondary-600 dark:from-primary-900 dark:via-primary-800 dark:to-secondary-900 text-white py-32 md:py-48 overflow-hidden">
      <!-- Video Background -->
      <div class="absolute inset-0 z-0 overflow-hidden">
        <video autoplay muted loop playsinline class="absolute inset-0 w-full h-full object-cover opacity-30">
          <!-- Placeholder video (Tech/Abstract theme) -->
          <source src="https://assets.mixkit.co/videos/preview/mixkit-digital-animation-of-blue-lines-996-large.mp4"
            type="video/mp4">
          Votre navigateur ne supporte pas la lecture de vidéos.
        </video>
        <!-- Overlay gradient to ensure text readability -->
        <div class="absolute inset-0 bg-gradient-to-br from-primary-900/80 to-secondary-900/80"></div>
      </div>

      <div class="container mx-auto px-4 relative z-20" :style="{ transform: parallaxTransform }">
        <div class="max-w-4xl mx-auto text-center">
          <h1 class="text-5xl md:text-7xl font-display font-bold mb-6 animate-fade-in-slow pb-4">
            Créons ensemble votre
            <span
              class="block bg-gradient-to-r from-white to-secondary-200 bg-clip-text text-transparent drop-shadow-[0_2px_8px_rgba(0,0,0,0.3)] py-2">
              présence digitale
            </span>
          </h1>
          <p class="text-xl md:text-2xl text-primary-100 dark:text-primary-200 mb-8 leading-relaxed animate-slide-up">
            Solutions web sur mesure, design moderne et performances optimales pour propulser votre business en ligne
          </p>
          <div class="flex flex-col sm:flex-row gap-4 justify-center animate-slide-up" style="animation-delay: 0.2s;">
            <router-link to="/devis"
              class="bg-white text-primary-600 px-8 py-4 rounded-lg font-bold text-lg hover:bg-primary-50 transition-all duration-200 shadow-lg hover:shadow-xl hover:-translate-y-1">
              Demander un devis
            </router-link>
            <router-link to="/portfolio"
              class="bg-transparent border-2 border-white text-white px-8 py-4 rounded-lg font-bold text-lg hover:bg-white hover:text-primary-600 transition-all duration-200">
              Voir nos réalisations
            </router-link>
          </div>
        </div>
      </div>

      <!-- Wave Separator -->
      <div class="absolute bottom-0 left-0 right-0 z-10">
        <svg viewBox="0 0 1440 120" fill="none" xmlns="http://www.w3.org/2000/svg" class="w-full h-auto">
          <path
            d="M0 0L60 10C120 20 240 40 360 46.7C480 53 600 47 720 43.3C840 40 960 40 1080 46.7C1200 53 1320 67 1380 73.3L1440 80V120H1380C1320 120 1200 120 1080 120C960 120 840 120 720 120C600 120 480 120 360 120C240 120 120 120 60 120H0V0Z"
            class="fill-white dark:fill-dark-900" />
        </svg>
      </div>
    </section>

    <!-- Services Section -->
    <section class="py-16 relative">
      <div class="absolute inset-0 bg-white dark:bg-dark-900 z-0"></div>
      <div class="container mx-auto px-4 relative z-20">
        <div class="text-center mb-16">
          <h2 class="text-4xl md:text-5xl font-bold text-dark-900 dark:text-white mb-4">
            Nos Services
          </h2>
          <p class="text-xl text-dark-600 dark:text-dark-300 max-w-2xl mx-auto">
            Des solutions complètes pour tous vos besoins digitaux
          </p>
        </div>

        <div ref="servicesRef" class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          <GlassCard v-for="(service, index) in services" :key="service.title" variant="light" :hover="true"
            border-radius="xl" class="p-8 group transition-all duration-500 opacity-0 translate-y-8"
            :class="{ 'opacity-100 translate-y-0': servicesVisible }" :style="getServiceStyle(index)">
            <div
              class="w-16 h-16 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"
                v-html="service.icon"></svg>
            </div>
            <h3 class="text-2xl font-bold text-dark-900 dark:text-white mb-3">{{ service.title }}</h3>
            <p class="text-dark-600 dark:text-dark-300 leading-relaxed">
              {{ service.description }}
            </p>
          </GlassCard>
        </div>
      </div>
    </section>

    <!-- Technologies Section -->
    <HomeTechnologies />

    <!-- Stats Section -->
    <section
      class="py-16 bg-gradient-to-br from-primary-600 to-secondary-600 dark:from-primary-900 dark:to-secondary-900 text-white">
      <div class="container mx-auto px-4 relative z-20">
        <!-- Chargement -->
        <div v-if="statsLoading" class="text-center">
          <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-white"></div>
          <p class="mt-4 text-primary-100">Chargement des statistiques...</p>
        </div>

        <!-- Statistiques -->
        <div v-else class="grid md:grid-cols-4 gap-8 text-center">
          <div ref="projectRef">
            <div class="text-5xl font-bold mb-2">{{ projectCount }}+</div>
            <div class="text-primary-100 dark:text-primary-200 text-lg">Projets réalisés</div>
          </div>
          <div ref="clientRef">
            <div class="text-5xl font-bold mb-2">{{ clientCount }}+</div>
            <div class="text-primary-100 dark:text-primary-200 text-lg">Clients satisfaits</div>
          </div>
          <div ref="expRef">
            <div class="text-5xl font-bold mb-2">{{ expCount }}+</div>
            <div class="text-primary-100 dark:text-primary-200 text-lg">Années d'expérience</div>
          </div>
          <div ref="satisfactionRef">
            <div class="text-5xl font-bold mb-2">{{ satisfactionCount }}%</div>
            <div class="text-primary-100 dark:text-primary-200 text-lg">Satisfaction client</div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="py-16 relative">
      <div class="absolute inset-0 bg-white dark:bg-dark-900 z-0"></div>
      <div class="container mx-auto px-4 text-center relative z-20">
        <h2 class="text-4xl md:text-5xl font-bold text-dark-900 dark:text-white mb-6">
          Prêt à démarrer votre projet ?
        </h2>
        <p class="text-xl text-dark-600 dark:text-dark-300 mb-8 max-w-2xl mx-auto">
          Contactez-nous dès aujourd'hui pour discuter de vos besoins et obtenir un devis personnalisé
        </p>
        <router-link to="/devis"
          class="inline-block bg-gradient-to-r from-primary-600 to-secondary-500 text-white px-10 py-4 rounded-lg font-bold text-lg hover:from-primary-700 hover:to-secondary-600 transition-all duration-200 shadow-lg hover:shadow-xl hover:-translate-y-1">
          Obtenir un devis gratuit
        </router-link>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { getStatistics } from '../api/portfolio'
import GlassCard from '../components/ui/GlassCard.vue'
import InteractiveBackground from '../components/ui/InteractiveBackground.vue'
import HomeTechnologies from '../components/HomeTechnologies.vue'
import { useParallax, useIntersectionObserver, useStaggerAnimation, useCountUp } from '../composables/useAnimations'

const stats = ref({
  total_projects: 150,
  total_clients: 120,
  satisfaction_rate: 98,
  years_experience: 5
})
const statsLoading = ref(true)

const { transform: parallaxTransform } = useParallax(0.3)

// Animation des services
const { target: servicesRef, isVisible: servicesVisible } = useIntersectionObserver({ threshold: 0.1 })
const { getStyle: getServiceStyle } = useStaggerAnimation(6, 100)

// Animation des statistiques
const { count: projectCount, elementRef: projectRef } = useCountUp(computed(() => stats.value.total_projects || 150), 2000)
const { count: clientCount, elementRef: clientRef } = useCountUp(computed(() => stats.value.total_clients || 120), 2000)
const { count: expCount, elementRef: expRef } = useCountUp(computed(() => stats.value.years_experience || 5), 2000)
const { count: satisfactionCount, elementRef: satisfactionRef } = useCountUp(computed(() => stats.value.satisfaction_rate || 98), 2000)

const services = [
  {
    title: 'Développement Web',
    description: 'Sites web modernes et performants, développés avec les dernières technologies pour une expérience utilisateur optimale.',
    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"></path>'
  },
  {
    title: 'Design UI/UX',
    description: 'Interfaces intuitives et élégantes, pensées pour offrir la meilleure expérience à vos utilisateurs.',
    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01"></path>'
  },
  {
    title: 'E-commerce',
    description: 'Boutiques en ligne complètes avec systèmes de paiement sécurisés et gestion des stocks simplifiée.',
    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"></path>'
  },
  {
    title: 'SEO & Marketing',
    description: 'Optimisation pour les moteurs de recherche et stratégies marketing pour booster votre visibilité en ligne.',
    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>'
  },
  {
    title: 'Applications Mobiles',
    description: 'Applications natives et cross-platform pour iOS et Android, performantes et intuitives.',
    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z"></path>'
  },
  {
    title: 'Maintenance & Support',
    description: 'Maintenance continue, mises à jour régulières et support technique réactif pour assurer la pérennité de votre site.',
    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>'
  }
]



const loadStatistics = async () => {
  try {
    statsLoading.value = true
    const response = await getStatistics()
    stats.value = response.data
  } catch (error) {
    console.error('Erreur lors du chargement des statistiques:', error)
    // En cas d'erreur, on garde les valeurs par défaut à 0
  } finally {
    statsLoading.value = false
  }
}

onMounted(async () => {
  // Charger les statistiques
  loadStatistics()
})
</script>
