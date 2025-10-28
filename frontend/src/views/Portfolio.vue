<template>
  <div class="min-h-screen bg-white dark:bg-dark-900 transition-colors duration-200">
    <!-- Header -->
    <section class="bg-gradient-to-br from-primary-600 to-secondary-600 dark:from-primary-900 dark:to-secondary-900 text-white py-20">
      <div class="container mx-auto px-4 text-center">
        <h1 class="text-5xl md:text-6xl font-bold mb-4">Notre Portfolio</h1>
        <p class="text-xl text-primary-100 dark:text-primary-200 max-w-2xl mx-auto">
          Découvrez nos réalisations et laissez-vous inspirer par nos projets
        </p>
      </div>
    </section>

    <!-- Filters -->
    <section class="py-8 bg-gray-50 dark:bg-dark-800 sticky top-16 z-40 border-b border-gray-200 dark:border-dark-700">
      <div class="container mx-auto px-4">
        <div class="flex flex-wrap gap-3 justify-center">
          <button
            @click="selectedFilter = 'all'"
            :class="[
              'px-6 py-2 rounded-lg font-semibold transition-all duration-200',
              selectedFilter === 'all' 
                ? 'bg-primary-600 text-white shadow-lg' 
                : 'bg-white dark:bg-dark-700 text-dark-700 dark:text-dark-200 hover:bg-primary-50 dark:hover:bg-dark-600 border border-gray-200 dark:border-dark-600'
            ]"
          >
            Tous les projets
          </button>
          <button
            @click="selectedFilter = 'web'"
            :class="[
              'px-6 py-2 rounded-lg font-semibold transition-all duration-200',
              selectedFilter === 'web' 
                ? 'bg-primary-600 text-white shadow-lg' 
                : 'bg-white dark:bg-dark-700 text-dark-700 dark:text-dark-200 hover:bg-primary-50 dark:hover:bg-dark-600 border border-gray-200 dark:border-dark-600'
            ]"
          >
            Sites Web
          </button>
          <button
            @click="selectedFilter = 'ecommerce'"
            :class="[
              'px-6 py-2 rounded-lg font-semibold transition-all duration-200',
              selectedFilter === 'ecommerce' 
                ? 'bg-primary-600 text-white shadow-lg' 
                : 'bg-white dark:bg-dark-700 text-dark-700 dark:text-dark-200 hover:bg-primary-50 dark:hover:bg-dark-600 border border-gray-200 dark:border-dark-600'
            ]"
          >
            E-commerce
          </button>
          <button
            @click="selectedFilter = 'mobile'"
            :class="[
              'px-6 py-2 rounded-lg font-semibold transition-all duration-200',
              selectedFilter === 'mobile' 
                ? 'bg-primary-600 text-white shadow-lg' 
                : 'bg-white dark:bg-dark-700 text-dark-700 dark:text-dark-200 hover:bg-primary-50 dark:hover:bg-dark-600 border border-gray-200 dark:border-dark-600'
            ]"
          >
            Applications
          </button>
        </div>
      </div>
    </section>

    <!-- Projects Grid -->
    <section class="py-16 bg-white dark:bg-dark-900">
      <div class="container mx-auto px-4">
        <div v-if="loading" class="text-center py-16">
          <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
          <p class="mt-4 text-dark-600 dark:text-dark-300">Chargement des projets...</p>
        </div>

        <div v-else-if="filteredProjects.length === 0" class="text-center py-16">
          <p class="text-xl text-dark-600 dark:text-dark-300">Aucun projet disponible dans cette catégorie.</p>
        </div>

        <div v-else class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          <div
            v-for="project in filteredProjects"
            :key="project.id"
            class="group bg-white dark:bg-dark-800 rounded-xl overflow-hidden shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-2 border border-gray-200 dark:border-dark-700"
          >
            <div class="relative h-64 overflow-hidden bg-gray-200 dark:bg-dark-700">
              <img
                v-if="project.image"
                :src="project.image"
                :alt="project.title"
                class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
              />
              <div v-else class="w-full h-full flex items-center justify-center">
                <svg class="w-20 h-20 text-gray-400 dark:text-dark-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                </svg>
              </div>
              <div class="absolute top-4 right-4">
                <span class="bg-primary-600 text-white px-3 py-1 rounded-full text-sm font-semibold">
                  {{ getCategoryLabel(project.category) }}
                </span>
              </div>
            </div>
            
            <div class="p-6">
              <h3 class="text-2xl font-bold text-dark-900 dark:text-white mb-2 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors">
                {{ project.title }}
              </h3>
              <p class="text-dark-600 dark:text-dark-300 mb-4 line-clamp-2">
                {{ project.description }}
              </p>
              
              <div class="flex flex-wrap gap-2 mb-4">
                <span
                  v-for="tech in project.technologies?.slice(0, 3)"
                  :key="tech"
                  class="px-3 py-1 bg-primary-50 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300 rounded-full text-xs font-medium"
                >
                  {{ tech }}
                </span>
              </div>

              <a
                v-if="project.url"
                :href="project.url"
                target="_blank"
                class="inline-flex items-center text-primary-600 dark:text-primary-400 font-semibold hover:underline"
              >
                Voir le projet
                <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path>
                </svg>
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Testimonials Section -->
    <section class="py-20 bg-gray-50 dark:bg-dark-800">
      <div class="container mx-auto px-4">
        <div class="text-center mb-16">
          <h2 class="text-4xl md:text-5xl font-bold text-dark-900 dark:text-white mb-4">
            Ce que disent nos clients
          </h2>
          <p class="text-xl text-dark-600 dark:text-dark-300 max-w-2xl mx-auto">
            La satisfaction de nos clients est notre priorité
          </p>
        </div>

        <div v-if="loadingTestimonials" class="text-center py-8">
          <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        </div>

        <div v-else class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          <div
            v-for="testimonial in testimonials"
            :key="testimonial.id"
            class="bg-white dark:bg-dark-700 rounded-xl p-8 shadow-lg border border-gray-200 dark:border-dark-600"
          >
            <div class="flex items-center mb-4">
              <div v-for="n in 5" :key="n" class="mr-1">
                <svg
                  class="w-5 h-5"
                  :class="n <= testimonial.rating ? 'text-yellow-400' : 'text-gray-300 dark:text-dark-500'"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path>
                </svg>
              </div>
            </div>
            
            <p class="text-dark-700 dark:text-dark-200 mb-6 italic leading-relaxed">
              "{{ testimonial.content }}"
            </p>
            
            <div class="flex items-center">
              <div class="w-12 h-12 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-full flex items-center justify-center mr-4">
                <span class="text-white font-bold text-lg">
                  {{ testimonial.client_name?.charAt(0).toUpperCase() }}
                </span>
              </div>
              <div>
                <p class="font-bold text-dark-900 dark:text-white">{{ testimonial.client_name }}</p>
                <p class="text-sm text-dark-600 dark:text-dark-400">{{ testimonial.company || 'Client' }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="py-20 bg-gradient-to-br from-primary-600 to-secondary-600 dark:from-primary-900 dark:to-secondary-900 text-white">
      <div class="container mx-auto px-4 text-center">
        <h2 class="text-4xl md:text-5xl font-bold mb-6">
          Vous avez un projet en tête ?
        </h2>
        <p class="text-xl text-primary-100 dark:text-primary-200 mb-8 max-w-2xl mx-auto">
          Discutons de votre vision et créons ensemble quelque chose d'exceptionnel
        </p>
        <router-link 
          to="/contact" 
          class="inline-block bg-white text-primary-600 px-10 py-4 rounded-lg font-bold text-lg hover:bg-primary-50 transition-all duration-200 shadow-lg hover:shadow-xl hover:-translate-y-1"
        >
          Contactez-nous
        </router-link>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getProjects, getTestimonials } from '../api/portfolio'

const selectedFilter = ref('all')
const projects = ref([])
const testimonials = ref([])
const loading = ref(true)
const loadingTestimonials = ref(true)

const filteredProjects = computed(() => {
  if (selectedFilter.value === 'all') {
    return projects.value
  }
  return projects.value.filter(project => project.category === selectedFilter.value)
})

const getCategoryLabel = (category) => {
  const labels = {
    'web': 'Site Web',
    'ecommerce': 'E-commerce',
    'mobile': 'Application',
    'other': 'Autre'
  }
  return labels[category] || category
}

onMounted(async () => {
  try {
    const [projectsRes, testimonialsRes] = await Promise.all([
      getProjects(),
      getTestimonials()
    ])
    
    projects.value = projectsRes.data.results || projectsRes.data || []
    testimonials.value = testimonialsRes.data.results || testimonialsRes.data || []
  } catch (error) {
    console.error('Erreur lors du chargement:', error)
  } finally {
    loading.value = false
    loadingTestimonials.value = false
  }
})
</script>