<template>
  <div class="min-h-screen">
    <!-- Header -->
    <section class="bg-black text-white py-16">
      <div class="container mx-auto px-4">
        <h1 class="text-5xl font-bold text-center">Mon Portfolio</h1>
        <p class="text-xl text-gray-300 text-center mt-4">Découvrez mes réalisations</p>
      </div>
    </section>

    <!-- Projets -->
    <section class="py-16 bg-white">
      <div class="container mx-auto px-4">
        <div v-if="loading" class="text-center py-16">
          <p class="text-xl">Chargement des projets...</p>
        </div>

        <div v-else-if="projects.length === 0" class="text-center py-16">
          <p class="text-xl text-gray-600">Aucun projet à afficher pour le moment.</p>
        </div>

        <div v-else class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          <div v-for="project in projects" :key="project.id" class="border-2 border-black overflow-hidden hover:shadow-xl transition">
            <img v-if="project.thumbnail" :src="project.thumbnail" :alt="project.title" class="w-full h-64 object-cover">
            <div class="p-6">
              <h3 class="text-2xl font-bold mb-2">{{ project.title }}</h3>
              <p class="text-gray-600 mb-4">{{ project.short_description }}</p>
              
              <div class="flex flex-wrap gap-2 mb-4">
                <span v-for="tech in project.technologies" :key="tech.id" class="bg-black text-white px-3 py-1 text-sm">
                  {{ tech.name }}
                </span>
              </div>

              <div class="flex gap-4">
                <a v-if="project.github_url" :href="project.github_url" target="_blank" class="text-black hover:underline">
                  GitHub
                </a>
                <a v-if="project.live_url" :href="project.live_url" target="_blank" class="text-black hover:underline">
                  Voir le site
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Témoignages -->
    <section class="py-16 bg-gray-100">
      <div class="container mx-auto px-4">
        <h2 class="text-4xl font-bold text-center mb-12">Témoignages Clients</h2>
        
        <div v-if="testimonials.length === 0" class="text-center py-8">
          <p class="text-xl text-gray-600">Aucun témoignage pour le moment.</p>
        </div>

        <div v-else class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          <div v-for="testimonial in testimonials" :key="testimonial.id" class="bg-white border-2 border-black p-6">
            <div class="flex items-center mb-4">
              <div class="text-yellow-500">
                <span v-for="n in testimonial.rating" :key="n">★</span>
                <span v-for="n in (5 - testimonial.rating)" :key="'empty-' + n" class="text-gray-300">★</span>
              </div>
            </div>
            <p class="text-gray-700 mb-4 italic">"{{ testimonial.content }}"</p>
            <div class="font-bold">{{ testimonial.client_name }}</div>
            <div class="text-sm text-gray-600">{{ testimonial.client_position }} {{ testimonial.client_company ? 'chez ' + testimonial.client_company : '' }}</div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import portfolioAPI from '../api/portfolio'

const projects = ref([])
const testimonials = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const [projectsRes, testimonialsRes] = await Promise.all([
      portfolioAPI.getProjects(),
      portfolioAPI.getTestimonials()
    ])
    projects.value = projectsRes.data.results || projectsRes.data
    testimonials.value = testimonialsRes.data.results || testimonialsRes.data
  } catch (error) {
    console.error('Erreur lors du chargement:', error)
  } finally {
    loading.value = false
  }
})
</script>