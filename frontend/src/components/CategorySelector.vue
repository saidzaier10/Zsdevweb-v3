<template>
  <div class="category-selector py-8">
    <div class="text-center mb-8">
      <h2 class="text-3xl font-bold text-dark-800 dark:text-white mb-2">
        Choisissez votre type de projet
      </h2>
      <p class="text-dark-600 dark:text-dark-300">
        Sélectionnez la catégorie qui correspond le mieux à vos besoins
      </p>
    </div>

    <!-- Chargement -->
    <div v-if="loading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      <p class="mt-4 text-dark-600 dark:text-dark-300">Chargement des catégories...</p>
    </div>

    <!-- Grille de catégories -->
    <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl mx-auto">
      <div
        v-for="category in categories"
        :key="category.id"
        @click="selectCategory(category)"
        :class="[
          'category-card p-6 rounded-xl cursor-pointer transition-all duration-200 border-2',
          selectedCategory?.id === category.id
            ? 'ring-4 ring-opacity-50 scale-105'
            : 'hover:shadow-xl hover:scale-102'
        ]"
        :style="{
          borderColor: category.color,
          '--category-color': category.color
        }"
      >
        <div class="text-center">
          <!-- Icône -->
          <div
            class="w-20 h-20 mx-auto mb-4 rounded-full flex items-center justify-center transition-transform duration-200"
            :style="{
              backgroundColor: category.color + '20',
              transform: selectedCategory?.id === category.id ? 'scale(1.1)' : 'scale(1)'
            }"
          >
            <i
              :class="[category.icon, 'text-4xl']"
              :style="{ color: category.color }"
            ></i>
          </div>

          <!-- Nom -->
          <h3 class="text-xl font-bold text-dark-800 dark:text-white mb-2">
            {{ category.name }}
          </h3>

          <!-- Description -->
          <p class="text-sm text-dark-600 dark:text-dark-400 mb-4">
            {{ category.description }}
          </p>

          <!-- Stats -->
          <div class="flex justify-center gap-4 text-xs text-dark-500 dark:text-dark-400">
            <span class="flex items-center gap-1">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01"></path>
              </svg>
              {{ category.project_types_count }} types
            </span>
            <span>•</span>
            <span class="flex items-center gap-1">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4"></path>
              </svg>
              {{ category.compatible_options_count }}+ options
            </span>
          </div>

          <!-- Badge de sélection -->
          <div v-if="selectedCategory?.id === category.id" class="mt-4">
            <span
              class="inline-block px-3 py-1 rounded-full text-xs font-semibold text-white"
              :style="{ backgroundColor: category.color }"
            >
              ✓ Sélectionné
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Bouton de confirmation -->
    <div v-if="selectedCategory" class="text-center mt-8">
      <button
        @click="confirmSelection"
        class="px-8 py-3 rounded-lg text-white font-semibold transition-all duration-200 hover:scale-105 shadow-lg"
        :style="{ backgroundColor: selectedCategory.color }"
      >
        Continuer avec {{ selectedCategory.name }}
        <svg class="w-5 h-5 inline-block ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"></path>
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getCategories } from '../api/quotes'
import { useToastStore } from '../stores/toast'

const toastStore = useToastStore()

const categories = ref([])
const loading = ref(true)
const selectedCategory = ref(null)

const emit = defineEmits(['category-selected'])

const loadCategories = async () => {
  try {
    loading.value = true
    const response = await getCategories()

    if (Array.isArray(response.data)) {
      categories.value = response.data
    } else if (response.data && response.data.results) {
      categories.value = response.data.results
    } else {
      categories.value = []
    }
  } catch (error) {
    console.error('Erreur lors du chargement des catégories:', error)
    toastStore.showToast('Erreur lors du chargement des catégories', 'error')
    categories.value = []
  } finally {
    loading.value = false
  }
}

const selectCategory = (category) => {
  selectedCategory.value = category
}

const confirmSelection = () => {
  if (selectedCategory.value) {
    emit('category-selected', selectedCategory.value)
  }
}

onMounted(() => {
  loadCategories()
})
</script>

<style scoped>
.category-card {
  background: white;
  transition: all 0.2s ease-in-out;
}

.dark .category-card {
  background: #1f2937;
}

.category-card:hover {
  transform: translateY(-4px);
}

.category-card.scale-105 {
  transform: scale(1.05);
}

.category-card.scale-102 {
  transform: scale(1.02);
}
</style>
