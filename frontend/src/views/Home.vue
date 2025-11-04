<template>
  <div class="min-h-screen bg-white dark:bg-dark-900 transition-colors duration-200">
    <!-- Hero Section -->
    <section class="relative bg-gradient-to-br from-primary-600 via-primary-700 to-secondary-600 dark:from-primary-900 dark:via-primary-800 dark:to-secondary-900 text-white py-24 md:py-32 overflow-hidden">
      <!-- Video Background -->
      <div class="absolute inset-0 w-full h-full overflow-hidden hero-video-container">
        <!-- Fallback: Animated Blobs (affichés si vidéo ne charge pas) -->
        <div class="absolute inset-0 hero-fallback transition-opacity duration-300">
          <div class="absolute -top-1/2 -left-1/4 w-96 h-96 bg-secondary-400 dark:bg-secondary-700 rounded-full blur-3xl animate-bounce-slow opacity-30"></div>
          <div class="absolute -bottom-1/2 -right-1/4 w-96 h-96 bg-primary-400 dark:bg-primary-700 rounded-full blur-3xl animate-bounce-slow opacity-30" style="animation-delay: 1s;"></div>
        </div>

        <!-- Overlay gradient pour maintenir la lisibilité -->
        <div class="absolute inset-0 bg-gradient-to-br from-primary-900/40 via-primary-800/35 to-secondary-900/40 dark:from-primary-950/50 dark:via-primary-900/45 dark:to-secondary-950/50 z-10"></div>

        <!-- Animated overlay pattern (optionnel - pour effet dynamique) -->
        <div class="absolute inset-0 opacity-10 z-20">
          <div class="absolute -top-1/2 -left-1/4 w-96 h-96 bg-secondary-400 dark:bg-secondary-700 rounded-full blur-3xl animate-bounce-slow"></div>
          <div class="absolute -bottom-1/2 -right-1/4 w-96 h-96 bg-primary-400 dark:bg-primary-700 rounded-full blur-3xl animate-bounce-slow" style="animation-delay: 1s;"></div>
        </div>
      </div>

      <div class="container mx-auto px-4 relative z-10">
        <div class="max-w-4xl mx-auto text-center">
          <h1 class="text-5xl md:text-7xl font-display font-bold mb-6 animate-fade-in-slow pb-4">
            Créons ensemble votre
            <span class="block bg-gradient-to-r from-white to-secondary-200 bg-clip-text text-transparent drop-shadow-[0_2px_8px_rgba(0,0,0,0.3)] py-2">
              présence digitale
            </span>
          </h1>
          <p class="text-xl md:text-2xl text-primary-100 dark:text-primary-200 mb-8 leading-relaxed animate-slide-up">
            Solutions web sur mesure, design moderne et performances optimales pour propulser votre business en ligne
          </p>
          <div class="flex flex-col sm:flex-row gap-4 justify-center animate-slide-up" style="animation-delay: 0.2s;">
            <router-link 
              to="/devis" 
              class="bg-white text-primary-600 px-8 py-4 rounded-lg font-bold text-lg hover:bg-primary-50 transition-all duration-200 shadow-lg hover:shadow-xl hover:-translate-y-1"
            >
              Demander un devis
            </router-link>
            <router-link 
              to="/portfolio" 
              class="bg-transparent border-2 border-white text-white px-8 py-4 rounded-lg font-bold text-lg hover:bg-white hover:text-primary-600 transition-all duration-200"
            >
              Voir nos réalisations
            </router-link>
          </div>
        </div>
      </div>

      <!-- Wave Separator -->
      <div class="absolute bottom-0 left-0 right-0">
        <svg viewBox="0 0 1440 120" fill="none" xmlns="http://www.w3.org/2000/svg" class="w-full h-auto">
          <path d="M0 0L60 10C120 20 240 40 360 46.7C480 53 600 47 720 43.3C840 40 960 40 1080 46.7C1200 53 1320 67 1380 73.3L1440 80V120H1380C1320 120 1200 120 1080 120C960 120 840 120 720 120C600 120 480 120 360 120C240 120 120 120 60 120H0V0Z" class="fill-white dark:fill-dark-900"/>
        </svg>
      </div>
    </section>

    <!-- Services Section -->
    <section class="py-20 bg-white dark:bg-dark-900">
      <div class="container mx-auto px-4">
        <div class="text-center mb-16">
          <h2 class="text-4xl md:text-5xl font-bold text-dark-900 dark:text-white mb-4">
            Nos Services
          </h2>
          <p class="text-xl text-dark-600 dark:text-dark-300 max-w-2xl mx-auto">
            Des solutions complètes pour tous vos besoins digitaux
          </p>
        </div>

        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          <!-- Service 1 -->
          <div class="group bg-white dark:bg-dark-800 border-2 border-gray-200 dark:border-dark-700 rounded-xl p-8 hover:border-primary-500 dark:hover:border-primary-600 hover:shadow-2xl transition-all duration-300 hover:-translate-y-2">
            <div class="w-16 h-16 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"></path>
              </svg>
            </div>
            <h3 class="text-2xl font-bold text-dark-900 dark:text-white mb-3">Développement Web</h3>
            <p class="text-dark-600 dark:text-dark-300 leading-relaxed">
              Sites web modernes et performants, développés avec les dernières technologies pour une expérience utilisateur optimale.
            </p>
          </div>

          <!-- Service 2 -->
          <div class="group bg-white dark:bg-dark-800 border-2 border-gray-200 dark:border-dark-700 rounded-xl p-8 hover:border-primary-500 dark:hover:border-primary-600 hover:shadow-2xl transition-all duration-300 hover:-translate-y-2">
            <div class="w-16 h-16 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01"></path>
              </svg>
            </div>
            <h3 class="text-2xl font-bold text-dark-900 dark:text-white mb-3">Design UI/UX</h3>
            <p class="text-dark-600 dark:text-dark-300 leading-relaxed">
              Interfaces intuitives et élégantes, pensées pour offrir la meilleure expérience à vos utilisateurs.
            </p>
          </div>

          <!-- Service 3 -->
          <div class="group bg-white dark:bg-dark-800 border-2 border-gray-200 dark:border-dark-700 rounded-xl p-8 hover:border-primary-500 dark:hover:border-primary-600 hover:shadow-2xl transition-all duration-300 hover:-translate-y-2">
            <div class="w-16 h-16 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"></path>
              </svg>
            </div>
            <h3 class="text-2xl font-bold text-dark-900 dark:text-white mb-3">E-commerce</h3>
            <p class="text-dark-600 dark:text-dark-300 leading-relaxed">
              Boutiques en ligne complètes avec systèmes de paiement sécurisés et gestion des stocks simplifiée.
            </p>
          </div>

          <!-- Service 4 -->
          <div class="group bg-white dark:bg-dark-800 border-2 border-gray-200 dark:border-dark-700 rounded-xl p-8 hover:border-primary-500 dark:hover:border-primary-600 hover:shadow-2xl transition-all duration-300 hover:-translate-y-2">
            <div class="w-16 h-16 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
              </svg>
            </div>
            <h3 class="text-2xl font-bold text-dark-900 dark:text-white mb-3">SEO & Marketing</h3>
            <p class="text-dark-600 dark:text-dark-300 leading-relaxed">
              Optimisation pour les moteurs de recherche et stratégies marketing pour booster votre visibilité en ligne.
            </p>
          </div>

          <!-- Service 5 -->
          <div class="group bg-white dark:bg-dark-800 border-2 border-gray-200 dark:border-dark-700 rounded-xl p-8 hover:border-primary-500 dark:hover:border-primary-600 hover:shadow-2xl transition-all duration-300 hover:-translate-y-2">
            <div class="w-16 h-16 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z"></path>
              </svg>
            </div>
            <h3 class="text-2xl font-bold text-dark-900 dark:text-white mb-3">Applications Mobiles</h3>
            <p class="text-dark-600 dark:text-dark-300 leading-relaxed">
              Applications natives et cross-platform pour iOS et Android, performantes et intuitives.
            </p>
          </div>

          <!-- Service 6 -->
          <div class="group bg-white dark:bg-dark-800 border-2 border-gray-200 dark:border-dark-700 rounded-xl p-8 hover:border-primary-500 dark:hover:border-primary-600 hover:shadow-2xl transition-all duration-300 hover:-translate-y-2">
            <div class="w-16 h-16 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
              </svg>
            </div>
            <h3 class="text-2xl font-bold text-dark-900 dark:text-white mb-3">Maintenance & Support</h3>
            <p class="text-dark-600 dark:text-dark-300 leading-relaxed">
              Maintenance continue, mises à jour régulières et support technique réactif pour assurer la pérennité de votre site.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Technologies Section -->
    <section class="py-20 bg-gray-50 dark:bg-dark-800">
      <div class="container mx-auto px-4">
        <div class="text-center mb-16">
          <h2 class="text-4xl md:text-5xl font-bold text-dark-900 dark:text-white mb-4">
            Technologies Modernes
          </h2>
          <p class="text-xl text-dark-600 dark:text-dark-300 max-w-2xl mx-auto">
            Nous utilisons les outils les plus performants du marché
          </p>
        </div>

        <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-6">
          <div class="bg-white dark:bg-dark-700 rounded-xl p-6 flex flex-col items-center justify-center hover:shadow-xl transition-shadow border border-gray-200 dark:border-dark-600">
            <div class="text-4xl mb-3">⚛️</div>
            <span class="font-semibold text-dark-900 dark:text-white">React</span>
          </div>
          <div class="bg-white dark:bg-dark-700 rounded-xl p-6 flex flex-col items-center justify-center hover:shadow-xl transition-shadow border border-gray-200 dark:border-dark-600">
            <div class="text-4xl mb-3">💚</div>
            <span class="font-semibold text-dark-900 dark:text-white">Vue.js</span>
          </div>
          <div class="bg-white dark:bg-dark-700 rounded-xl p-6 flex flex-col items-center justify-center hover:shadow-xl transition-shadow border border-gray-200 dark:border-dark-600">
            <div class="text-4xl mb-3">🟢</div>
            <span class="font-semibold text-dark-900 dark:text-white">Node.js</span>
          </div>
          <div class="bg-white dark:bg-dark-700 rounded-xl p-6 flex flex-col items-center justify-center hover:shadow-xl transition-shadow border border-gray-200 dark:border-dark-600">
            <div class="text-4xl mb-3">🐍</div>
            <span class="font-semibold text-dark-900 dark:text-white">Python</span>
          </div>
          <div class="bg-white dark:bg-dark-700 rounded-xl p-6 flex flex-col items-center justify-center hover:shadow-xl transition-shadow border border-gray-200 dark:border-dark-600">
            <div class="text-4xl mb-3">🎨</div>
            <span class="font-semibold text-dark-900 dark:text-white">Tailwind</span>
          </div>
          <div class="bg-white dark:bg-dark-700 rounded-xl p-6 flex flex-col items-center justify-center hover:shadow-xl transition-shadow border border-gray-200 dark:border-dark-600">
            <div class="text-4xl mb-3">🐳</div>
            <span class="font-semibold text-dark-900 dark:text-white">Docker</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Stats Section -->
    <section class="py-20 bg-gradient-to-br from-primary-600 to-secondary-600 dark:from-primary-900 dark:to-secondary-900 text-white">
      <div class="container mx-auto px-4">
        <!-- Chargement -->
        <div v-if="statsLoading" class="text-center">
          <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-white"></div>
          <p class="mt-4 text-primary-100">Chargement des statistiques...</p>
        </div>

        <!-- Statistiques -->
        <div v-else class="grid md:grid-cols-4 gap-8 text-center">
          <div>
            <div class="text-5xl font-bold mb-2">{{ stats.total_projects }}+</div>
            <div class="text-primary-100 dark:text-primary-200 text-lg">Projets réalisés</div>
          </div>
          <div>
            <div class="text-5xl font-bold mb-2">{{ stats.total_clients }}+</div>
            <div class="text-primary-100 dark:text-primary-200 text-lg">Clients satisfaits</div>
          </div>
          <div>
            <div class="text-5xl font-bold mb-2">{{ stats.years_experience }}+</div>
            <div class="text-primary-100 dark:text-primary-200 text-lg">Années d'expérience</div>
          </div>
          <div>
            <div class="text-5xl font-bold mb-2">{{ stats.satisfaction_rate }}%</div>
            <div class="text-primary-100 dark:text-primary-200 text-lg">Satisfaction client</div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="py-20 bg-white dark:bg-dark-900">
      <div class="container mx-auto px-4 text-center">
        <h2 class="text-4xl md:text-5xl font-bold text-dark-900 dark:text-white mb-6">
          Prêt à démarrer votre projet ?
        </h2>
        <p class="text-xl text-dark-600 dark:text-dark-300 mb-8 max-w-2xl mx-auto">
          Contactez-nous dès aujourd'hui pour discuter de vos besoins et obtenir un devis personnalisé
        </p>
        <router-link 
          to="/devis" 
          class="inline-block bg-gradient-to-r from-primary-600 to-secondary-500 text-white px-10 py-4 rounded-lg font-bold text-lg hover:from-primary-700 hover:to-secondary-600 transition-all duration-200 shadow-lg hover:shadow-xl hover:-translate-y-1"
        >
          Obtenir un devis gratuit
        </router-link>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getStatistics } from '../api/portfolio'

// Référence pour la vidéo
const heroVideo = ref(null)

// Fonction pour créer et insérer la vidéo dynamiquement
const loadVideo = () => {
  const container = document.querySelector('.hero-video-container')
  if (!container) {
    console.error('Conteneur vidéo non trouvé')
    return
  }

  // Créer l'élément vidéo
  const video = document.createElement('video')
  video.autoplay = true
  video.muted = true
  video.loop = true
  video.playsInline = true
  video.setAttribute('playsinline', 'true') // Important pour iOS
  video.className = 'absolute inset-0 w-full h-full object-cover'
  video.style.cssText = 'z-index: 0; position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover;'

  // Créer et ajouter la source
  const source = document.createElement('source')
  source.src = '/videos/hero-background.mp4'
  source.type = 'video/mp4'
  video.appendChild(source)

  // Événement: vidéo prête
  video.addEventListener('loadeddata', () => {
    console.log('✅ Vidéo chargée et prête')
    video.playbackRate = 0.5
    video.play().then(() => {
      console.log('✅ Lecture vidéo démarrée à vitesse 0.5x')
      // Masquer le fallback
      const fallback = document.querySelector('.hero-fallback')
      if (fallback) {
        fallback.style.opacity = '0'
        setTimeout(() => { fallback.style.display = 'none' }, 300)
      }
    }).catch(err => {
      console.error('❌ Erreur lors du démarrage de la lecture:', err)
    })
  })

  // Événement: erreur
  video.addEventListener('error', (e) => {
    console.error('❌ Erreur de chargement de la vidéo:', e)
    console.error('Détails:', video.error)
  })

  // Insérer la vidéo au début du conteneur
  container.insertBefore(video, container.firstChild)
  heroVideo.value = video

  console.log('📹 Élément vidéo créé et inséré dans le DOM')
}

const stats = ref({
  total_projects: 0,
  total_clients: 0,
  satisfaction_rate: 0,
  years_experience: 0
})
const statsLoading = ref(true)

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

  // Charger la vidéo de fond
  setTimeout(() => {
    loadVideo()
  }, 100)
})
</script>
