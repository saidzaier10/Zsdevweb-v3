<template>
  <div class="relative overflow-hidden" :class="containerClass">
    <!-- Placeholder avec shimmer -->
    <div
      v-if="!isLoaded"
      class="absolute inset-0 bg-gray-200 dark:bg-dark-700 shimmer"
      :style="{ aspectRatio: aspectRatio }"
    ></div>

    <!-- Image principale -->
    <img
      ref="imageRef"
      :data-src="src"
      :alt="alt"
      :class="[
        'transition-opacity duration-500',
        isLoaded ? 'opacity-100' : 'opacity-0',
        imageClass
      ]"
      @load="onLoad"
      @error="onError"
    />

    <!-- Fallback en cas d'erreur -->
    <div
      v-if="hasError"
      class="absolute inset-0 flex items-center justify-center bg-gray-100 dark:bg-dark-800"
    >
      <svg class="w-12 h-12 text-gray-400 dark:text-dark-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
      </svg>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  src: {
    type: String,
    required: true
  },
  alt: {
    type: String,
    default: ''
  },
  aspectRatio: {
    type: String,
    default: '16/9'
  },
  containerClass: {
    type: String,
    default: ''
  },
  imageClass: {
    type: String,
    default: 'w-full h-full object-cover'
  }
})

const imageRef = ref(null)
const isLoaded = ref(false)
const hasError = ref(false)
let observer = null

const onLoad = () => {
  isLoaded.value = true
}

const onError = () => {
  hasError.value = true
}

const observeImage = () => {
  if ('IntersectionObserver' in window) {
    observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting && imageRef.value) {
          const img = imageRef.value
          const dataSrc = img.getAttribute('data-src')
          if (dataSrc) {
            img.src = dataSrc
            img.removeAttribute('data-src')
          }
          observer.unobserve(img)
        }
      })
    }, {
      rootMargin: '50px' // Charge l'image 50px avant qu'elle soit visible
    })

    if (imageRef.value) {
      observer.observe(imageRef.value)
    }
  } else {
    // Fallback pour les navigateurs sans IntersectionObserver
    if (imageRef.value) {
      imageRef.value.src = props.src
    }
  }
}

onMounted(() => {
  observeImage()
})

onUnmounted(() => {
  if (observer && imageRef.value) {
    observer.unobserve(imageRef.value)
  }
})
</script>
