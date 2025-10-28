<template>
  <div class="min-h-screen">
    <!-- Hero Section avec Gradient Animé -->
    <section class="relative overflow-hidden bg-gradient-to-br from-primary-600 via-primary-700 to-secondary-600 text-white">
      <!-- Formes décoratives en arrière-plan -->
      <div class="absolute inset-0 overflow-hidden">
        <div class="absolute -top-40 -right-40 w-80 h-80 bg-secondary-500 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-bounce-slow"></div>
        <div class="absolute -bottom-40 -left-40 w-80 h-80 bg-primary-500 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-bounce-slow animation-delay-2000"></div>
        <div class="absolute top-40 left-1/2 w-60 h-60 bg-purple-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-bounce-slow animation-delay-4000"></div>
      </div>

      <div class="container mx-auto px-4 py-20 md:py-32 relative z-10">
        <div class="max-w-4xl mx-auto text-center animate-fade-in">
          <!-- Badge -->
          <div class="inline-flex items-center space-x-2 bg-white/10 backdrop-blur-md px-4 py-2 rounded-full mb-6 border border-white/20">
            <span class="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
            <span class="text-sm font-medium">Disponible pour de nouveaux projets</span>
          </div>

          <!-- Titre Principal -->
          <h1 class="text-5xl md:text-7xl font-display font-extrabold mb-6 leading-tight animate-slide-up">
            Développeur Web
            <span class="block bg-gradient-to-r from-yellow-300 to-orange-300 bg-clip-text text-transparent">
              Full Stack
            </span>
          </h1>

          <!-- Sous-titre -->
          <p class="text-xl md:text-2xl text-blue-100 mb-10 max-w-3xl mx-auto leading-relaxed animate-slide-up">
            Je transforme vos idées en applications web modernes, performantes et élégantes. 
            De la conception au déploiement, je crée des solutions sur mesure pour votre entreprise.
          </p>

          <!-- CTA Buttons -->
          <div class="flex flex-col sm:flex-row gap-4 justify-center items-center animate-slide-up">
            <router-link 
              to="/portfolio" 
              class="group relative inline-flex items-center space-x-2 bg-white text-primary-700 px-8 py-4 rounded-xl font-bold text-lg shadow-xl hover:shadow-2xl transform hover:-translate-y-1 transition-all duration-300"
            >
              <span>Voir mes projets</span>
              <svg class="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"></path>
              </svg>
            </router-link>
            
            <router-link 
              to="/devis" 
              class="group inline-flex items-center space-x-2 bg-white/10 backdrop-blur-md text-white px-8 py-4 rounded-xl font-bold text-lg border-2 border-white/30 hover:bg-white/20 hover:border-white/50 transition-all duration-300"
            >
              <span>Demander un devis</span>
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
              </svg>
            </router-link>
          </div>

          <!-- Stats -->
          <div class="grid grid-cols-3 gap-6 mt-16 max-w-2xl mx-auto">
            <div class="text-center animate-slide-up">
              <div class="text-4xl md:text-5xl font-bold mb-2">5+</div>
              <div class="text-blue-200 text-sm md:text-base">Ans d'expérience</div>
            </div>
            <div class="text-center animate-slide-up">
              <div class="text-4xl md:text-5xl font-bold mb-2">50+</div>
              <div class="text-blue-200 text-sm md:text-base">Projets réalisés</div>
            </div>
            <div class="text-center animate-slide-up">
              <div class="text-4xl md:text-5xl font-bold mb-2">100%</div>
              <div class="text-blue-200 text-sm md:text-base">Satisfaction client</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Wave Separator -->
      <div class="absolute bottom-0 left-0 w-full">
        <svg viewBox="0 0 1440 120" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M0 0L60 10C120 20 240 40 360 46.7C480 53 600 47 720 43.3C840 40 960 40 1080 46.7C1200 53 1320 67 1380 73.3L1440 80V120H1380C1320 120 1200 120 1080 120C960 120 840 120 720 120C600 120 480 120 360 120C240 120 120 120 60 120H0V0Z" fill="rgb(248, 250, 252)"/>
        </svg>
      </div>
    </section>

    <!-- Services Section -->
    <section class="py-20 bg-dark-50">
      <div class="container mx-auto px-4">
        <div class="text-center mb-16">
          <h2 class="section-title">Mes Services</h2>
          <p class="text-xl text-dark-600 max-w-2xl mx-auto">
            Des solutions complètes pour tous vos besoins digitaux
          </p>
        </div>

        <div class="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          <!-- Service 1 : Sites Vitrines -->
          <div class="card p-8 group cursor-pointer border-2 border-transparent hover:border-primary-500">
            <div class="w-16 h-16 bg-gradient-to-br from-blue-500 to-blue-600 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300 shadow-lg">
              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
              </svg>
            </div>
            <h3 class="text-2xl font-bold mb-4 text-dark-900">Sites Vitrines</h3>
            <p class="text-dark-600 mb-6 leading-relaxed">
              Sites de présentation élégants et professionnels pour mettre en valeur votre activité et attirer de nouveaux clients.
            </p>
            <ul class="space-y-2 text-dark-600">
              <li class="flex items-start space-x-2">
                <svg class="w-5 h-5 text-primary-500 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                </svg>
                <span>Design responsive</span>
              </li>
              <li class="flex items-start space-x-2">
                <svg class="w-5 h-5 text-primary-500 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                </svg>
                <span>SEO optimisé</span>
              </li>
              <li class="flex items-start space-x-2">
                <svg class="w-5 h-5 text-primary-500 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                </svg>
                <span>Performance optimale</span>
              </li>
            </ul>
          </div>

          <!-- Service 2 : E-commerce -->
          <div class="card p-8 group cursor-pointer border-2 border-transparent hover:border-secondary-500">
            <div class="w-16 h-16 bg-gradient-to-br from-secondary-500 to-secondary-600 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300 shadow-lg">
              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"></path>
              </svg>
            </div>
            <h3 class="text-2xl font-bold mb-4 text-dark-900">E-commerce</h3>
            <p class="text-dark-600 mb-6 leading-relaxed">
              Boutiques en ligne complètes et sécurisées avec gestion des produits, paiements et livraisons.
            </p>
            <ul class="space-y-2 text-dark-600">
              <li class="flex items-start space-x-2">
                <svg class="w-5 h-5 text-secondary-500 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                </svg>
                <span>Paiement sécurisé</span>
              </li>
              <li class="flex items-start space-x-2">
                <svg class="w-5 h-5 text-secondary-500 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                </svg>
                <span>Gestion de stock</span>
              </li>
              <li class="flex items-start space-x-2">
                <svg class="w-5 h-5 text-secondary-500 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                </svg>
                <span>Tableau de bord admin</span>
              </li>
            </ul>
          </div>

          <!-- Service 3 : Applications Web -->
          <div class="card p-8 group cursor-pointer border-2 border-transparent hover:border-purple-500">
            <div class="w-16 h-16 bg-gradient-to-br from-purple-500 to-purple-600 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300 shadow-lg">
              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"></path>
              </svg>
            </div>
            <h3 class="text-2xl font-bold mb-4 text-dark-900">Applications Web</h3>
            <p class="text-dark-600 mb-6 leading-relaxed">
              Applications web sur mesure, complexes et évolutives, parfaitement adaptées à vos besoins spécifiques.
            </p>
            <ul class="space-y-2 text-dark-600">
              <li class="flex items-start space-x-2">
                <svg class="w-5 h-5 text-purple-500 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                </svg>
                <span>Architecture scalable</span>
              </li>
              <li class="flex items-start space-x-2">
                <svg class="w-5 h-5 text-purple-500 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                </svg>
                <span>API REST</span>
              </li>
              <li class="flex items-start space-x-2">
                <svg class="w-5 h-5 text-purple-500 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                </svg>
                <span>Maintenance incluse</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <!-- Technologies Section -->
    <section class="py-20 bg-white">
      <div class="container mx-auto px-4">
        <div class="text-center mb-16">
          <h2 class="section-title">Technologies Maîtrisées</h2>
          <p class="text-xl text-dark-600 max-w-2xl mx-auto">
            Stack moderne pour des applications performantes
          </p>
        </div>

        <div class="flex flex-wrap justify-center gap-6 max-w-4xl mx-auto">
          <div class="flex items-center space-x-3 bg-dark-50 px-6 py-4 rounded-xl border-2 border-dark-200 hover:border-primary-500 hover:shadow-lg transition-all duration-300 cursor-pointer">
            <span class="text-2xl">⚡</span>
            <span class="font-semibold text-dark-800">Vue.js</span>
          </div>
          <div class="flex items-center space-x-3 bg-dark-50 px-6 py-4 rounded-xl border-2 border-dark-200 hover:border-primary-500 hover:shadow-lg transition-all duration-300 cursor-pointer">
            <span class="text-2xl">🐍</span>
            <span class="font-semibold text-dark-800">Django</span>
          </div>
          <div class="flex items-center space-x-3 bg-dark-50 px-6 py-4 rounded-xl border-2 border-dark-200 hover:border-primary-500 hover:shadow-lg transition-all duration-300 cursor-pointer">
            <span class="text-2xl">🐘</span>
            <span class="font-semibold text-dark-800">PostgreSQL</span>
          </div>
          <div class="flex items-center space-x-3 bg-dark-50 px-6 py-4 rounded-xl border-2 border-dark-200 hover:border-primary-500 hover:shadow-lg transition-all duration-300 cursor-pointer">
            <span class="text-2xl">🎨</span>
            <span class="font-semibold text-dark-800">Tailwind CSS</span>
          </div>
          <div class="flex items-center space-x-3 bg-dark-50 px-6 py-4 rounded-xl border-2 border-dark-200 hover:border-primary-500 hover:shadow-lg transition-all duration-300 cursor-pointer">
            <span class="text-2xl">🐳</span>
            <span class="font-semibold text-dark-800">Docker</span>
          </div>
          <div class="flex items-center space-x-3 bg-dark-50 px-6 py-4 rounded-xl border-2 border-dark-200 hover:border-primary-500 hover:shadow-lg transition-all duration-300 cursor-pointer">
            <span class="text-2xl">☁️</span>
            <span class="font-semibold text-dark-800">AWS</span>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Final Section -->
    <section class="py-20 bg-gradient-to-r from-primary-600 to-secondary-600 text-white relative overflow-hidden">
      <div class="absolute inset-0">
        <div class="absolute top-0 left-0 w-96 h-96 bg-primary-500 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-pulse"></div>
        <div class="absolute bottom-0 right-0 w-96 h-96 bg-secondary-500 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-pulse animation-delay-2000"></div>
      </div>

      <div class="container mx-auto px-4 text-center relative z-10">
        <h2 class="text-4xl md:text-5xl font-bold mb-6">
          Prêt à démarrer votre projet ?
        </h2>
        <p class="text-xl md:text-2xl text-blue-100 mb-10 max-w-2xl mx-auto">
          Obtenez un devis gratuit et personnalisé en quelques minutes
        </p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <router-link 
            to="/devis" 
            class="inline-flex items-center space-x-2 bg-white text-primary-700 px-8 py-4 rounded-xl font-bold text-lg shadow-xl hover:shadow-2xl transform hover:-translate-y-1 transition-all duration-300"
          >
            <span>Obtenir un devis gratuit</span>
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"></path>
            </svg>
          </router-link>
          <router-link 
            to="/contact" 
            class="inline-flex items-center space-x-2 bg-white/10 backdrop-blur-md text-white px-8 py-4 rounded-xl font-bold text-lg border-2 border-white/30 hover:bg-white/20 transition-all duration-300"
          >
            <span>Me contacter</span>
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
            </svg>
          </router-link>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
// Pas de logique nécessaire pour le moment
</script>