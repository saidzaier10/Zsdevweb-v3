<template>
  <div class="min-h-screen bg-dark-50">
    <!-- Header Section -->
    <section class="bg-gradient-to-r from-primary-600 to-secondary-600 text-white py-20">
      <div class="container mx-auto px-4">
        <div class="max-w-3xl mx-auto text-center">
          <h1 class="text-5xl md:text-6xl font-display font-bold mb-6 animate-fade-in">
            Mon Portfolio
          </h1>
          <p class="text-xl md:text-2xl text-blue-100 animate-slide-up">
            Découvrez mes projets récents et mes réalisations
          </p>
        </div>
      </div>
    </section>

    <!-- Filtres de Technologies -->
    <section class="py-8 bg-white border-b border-gray-200 sticky top-16 z-40 shadow-sm">
      <div class="container mx-auto px-4">
        <div class="flex flex-wrap gap-3 justify-center">
          <button 
            @click="selectedFilter = 'all'"
            :class="[
              'px-6 py-2 rounded-full font-medium transition-all duration-300',
              selectedFilter === 'all' 
                ? 'bg-gradient-to-r from-primary-600 to-primary-500 text-white shadow-lg' 
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            ]"
          >
            Tous les projets
          </button>
          <button 
            @click="selectedFilter = 'frontend'"
            :class="[
              'px-6 py-2 rounded-full font-medium transition-all duration-300',
              selectedFilter === 'frontend' 
                ? 'bg-gradient-to-r from-primary-600 to-primary-500 text-white shadow-lg' 
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            ]"
          >
            Frontend
          </button>
          <button 
            @click="selectedFilter = 'backend'"
            :class="[
              'px-6 py-2 rounded-full font-medium transition-all duration-300',
              selectedFilter === 'backend' 
                ? 'bg-gradient-to-r from-primary-600 to-primary-500 text-white shadow-lg' 
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            ]"
          >
            Backend
          </button>
          <button 
            @click="selectedFilter = 'fullstack'"
            :class="[
              'px-6 py-2 rounded-full font-medium transition-all duration-300',
              selectedFilter === 'fullstack' 
                ? 'bg-gradient-to-r from-primary-600 to-primary-500 text-white shadow-lg' 
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            ]"
          >
            Full Stack
          </button>
        </div>
      </div>
    </section>

    <!-- Projects Grid -->
    <section class="py-16">
      <div class="container mx-auto px-4">
        <div v-if="loading" class="text-center py-20">
          <div class="inline-block animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-primary-600"></div>
          <p class="mt-4 text-gray-600 font-medium">Chargement des projets...</p>
        </div>

        <div v-else-if="error" class="text-center py-20">
          <div class="inline-flex items-center justify-center w-16 h-16 bg-red-100 rounded-full mb-4">
            <svg class="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </div>
          <p class="text-red-600 font-medium">{{ error }}</p>
        </div>

        <div v-else-if="projects.length === 0" class="text-center py-20">
          <div class="inline-flex items-center justify-center w-16 h-16 bg-gray-100 rounded-full mb-4">
            <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"></path>
            </svg>
          </div>
          <p class="text-gray-600 font-medium">Aucun projet disponible pour le moment</p>
        </div>

        <div v-else class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          <div 
            v-for="project in filteredProjects" 
            :key="project.id"
            class="group card overflow-hidden cursor-pointer animate-fade-in"
          >
            <!-- Image du Projet -->
            <div class="relative h-56 overflow-hidden bg-gradient-to-br from-primary-100 to-secondary-100">
              <img 
                v-if="project.thumbnail" 
                :src="project.thumbnail" 
                :alt="project.title"
                class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
              />
              <div v-else class="w-full h-full flex items-center justify-center">
                <svg class="w-20 h-20 text-primary-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                </svg>
              </div>
              
              <!-- Badge Featured -->
              <div v-if="project.featured" class="absolute top-4 right-4">
                <span class="inline-flex items-center space-x-1 bg-yellow-400 text-yellow-900 px-3 py-1 rounded-full text-xs font-bold shadow-lg">
                  <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path>
                  </svg>
                  <span>Featured</span>
                </span>
              </div>

              <!-- Overlay avec liens -->
              <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-end justify-center pb-6 space-x-4">
                <a 
                  v-if="project.github_url" 
                  :href="project.github_url" 
                  target="_blank"
                  class="flex items-center space-x-2 bg-white/90 text-gray-900 px-4 py-2 rounded-lg font-semibold hover:bg-white transition-colors"
                  @click.stop
                >
                  <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                  </svg>
                  <span>Code</span>
                </a>
                <a 
                  v-if="project.live_url" 
                  :href="project.live_url" 
                  target="_blank"
                  class="flex items-center space-x-2 bg-primary-600 text-white px-4 py-2 rounded-lg font-semibold hover:bg-primary-700 transition-colors"
                  @click.stop
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path>
                  </svg>
                  <span>Demo</span>
                </a>
              </div>
            </div>

            <!-- Contenu de la Card -->
            <div class="p-6">
              <h3 class="text-xl font-bold text-dark-900 mb-2 group-hover:text-primary-600 transition-colors">
                {{ project.title }}
              </h3>
              <p class="text-dark-600 mb-4 line-clamp-2">
                {{ project.short_description || project.description }}
              </p>

              <!-- Technologies -->
              <div class="flex flex-wrap gap-2">
                <span 
                  v-for="tech in project.technologies?.slice(0, 4)" 
                  :key="tech.id"
                  class="inline-flex items-center px-3 py-1 bg-primary-50 text-primary-700 rounded-full text-xs font-medium"
                >
                  {{ tech.name }}
                </span>
                <span 
                  v-if="project.technologies?.length > 4"
                  class="inline-flex items-center px-3 py-1 bg-gray-100 text-gray-600 rounded-full text-xs font-medium"
                >
                  +{{ project.technologies.length - 4 }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Testimonials Section -->
    <section v-if="testimonials.length > 0" class="py-20 bg-white">
      <div class="container mx-auto px-4">
        <div class="text-center mb-16">
          <h2 class="section-title">Ce que disent mes clients</h2>
          <p class="text-xl text-dark-600 max-w-2xl mx-auto">
            Découvrez les retours d'expérience de mes clients satisfaits
          </p>
        </div>

        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
          <div 
            v-for="testimonial in testimonials" 
            :key="testimonial.id"
            class="card p-6 hover:shadow-2xl transition-shadow duration-300"
          >
            <!-- Rating Stars -->
            <div class="flex items-center mb-4">
              <div class="flex space-x-1">
                <svg 
                  v-for="star in 5" 
                  :key="star"
                  :class="[
                    'w-5 h-5',
                    star <= testimonial.rating ? 'text-yellow-400' : 'text-gray-300'
                  ]"
                  fill="currentColor" 
                  viewBox="0 0 20 20"
                >
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path>
                </svg>
              </div>
              <span class="ml-2 text-sm font-semibold text-dark-700">{{ testimonial.rating }}/5</span>
            </div>

            <!-- Testimonial Content -->
            <blockquote class="text-dark-700 mb-6 italic leading-relaxed">
              "{{ testimonial.content }}"
            </blockquote>

            <!-- Client Info -->
            <div class="flex items-center space-x-3 pt-4 border-t border-gray-200">
              <div 
                v-if="testimonial.client_photo" 
                class="w-12 h-12 rounded-full overflow-hidden bg-gradient-to-br from-primary-500 to-secondary-500"
              >
                <img :src="testimonial.client_photo" :alt="testimonial.client_name" class="w-full h-full object-cover" />
              </div>
              <div v-else class="w-12 h-12 rounded-full bg-gradient-to-br from-primary-500 to-secondary-500 flex items-center justify-center">
                <span class="text-white font-bold text-lg">{{ testimonial.client_name?.charAt(0) }}</span>
              </div>
              <div>
                <p class="font-semibold text-dark-900">{{ testimonial.client_name }}</p>
                <p class="text-sm text-dark-500">
                  {{ testimonial.client_position }}
                  <span v-if="testimonial.client_company"> • {{ testimonial.client_company }}</span>
                </p>
              </div>
            </div>

            <!-- Project Link -->
            <div v-if="testimonial.project_title" class="mt-4">
              <span class="inline-flex items-center text-xs text-primary-600 font-medium">
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                </svg>
                Projet : {{ testimonial.project_title }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="py-20 bg-gradient-to-r from-primary-600 to-secondary-600 text-white">
      <div class="container mx-auto px-4 text-center">
        <h2 class="text-4xl md:text-5xl font-bold mb-6">
          Vous avez un projet en tête ?
        </h2>
        <p class="text-xl text-blue-100 mb-10 max-w-2xl mx-auto">
          Travaillons ensemble pour créer quelque chose d'extraordinaire
        </p>
        <router-link 
          to="/devis" 
          class="inline-flex items-center space-x-2 bg-white text-primary-700 px-8 py-4 rounded-xl font-bold text-lg shadow-xl hover:shadow-2xl transform hover:-translate-y-1 transition-all duration-300"
        >
          <span>Obtenir un devis gratuit</span>
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"></path>
          </svg>
        </router-link>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getProjects, getTestimonials } from '../api/portfolio'

const projects = ref([])
const testimonials = ref([])
const loading = ref(true)
const error = ref(null)
const selectedFilter = ref('all')

const filteredProjects = computed(() => {
  if (selectedFilter.value === 'all') {
    return projects.value
  }
  return projects.value.filter(project => {
    // Ici vous pouvez ajouter une logique de filtrage basée sur les technologies
    // Pour l'instant on retourne tous les projets
    return true
  })
})

onMounted(async () => {
  try {
    loading.value = true
    const [projectsResponse, testimonialsResponse] = await Promise.all([
      getProjects(),
      getTestimonials()
    ])
    
    projects.value = projectsResponse.data.results || projectsResponse.data
    testimonials.value = testimonialsResponse.data.results || testimonialsResponse.data
  } catch (err) {
    console.error('Erreur lors du chargement:', err)
    error.value = 'Impossible de charger les projets. Veuillez réessayer plus tard.'
  } finally {
    loading.value = false
  }
})
</script>