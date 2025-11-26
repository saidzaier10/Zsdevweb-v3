<template>
  <div 
    class="skeleton-loader"
    :class="[variantClass, { 'animate-pulse': animate }]"
    :style="customStyle"
  ></div>
</template>

<script setup>
import { computed } from 'vue'

/**
 * SkeletonLoader Component
 * Loading placeholder with shimmer effect
 * 
 * @prop {String} variant - Loader variant: 'text', 'title', 'avatar', 'card', 'image'
 * @prop {String} width - Custom width (CSS value)
 * @prop {String} height - Custom height (CSS value)
 * @prop {Boolean} animate - Enable pulse animation
 * @prop {Boolean} shimmer - Enable shimmer effect
 */
const props = defineProps({
  variant: {
    type: String,
    default: 'text',
    validator: (value) => ['text', 'title', 'avatar', 'card', 'image', 'custom'].includes(value)
  },
  width: {
    type: String,
    default: null
  },
  height: {
    type: String,
    default: null
  },
  animate: {
    type: Boolean,
    default: true
  },
  shimmer: {
    type: Boolean,
    default: true
  }
})

const variantClass = computed(() => {
  const variants = {
    text: 'skeleton-text',
    title: 'skeleton-title',
    avatar: 'skeleton-avatar',
    card: 'skeleton-card',
    image: 'skeleton-image',
    custom: ''
  }
  return variants[props.variant] || variants.text
})

const customStyle = computed(() => {
  const styles = {}
  
  if (props.width) styles.width = props.width
  if (props.height) styles.height = props.height
  
  if (props.shimmer) {
    styles.background = `linear-gradient(
      90deg,
      rgba(255, 255, 255, 0) 0%,
      rgba(255, 255, 255, 0.2) 20%,
      rgba(255, 255, 255, 0.5) 60%,
      rgba(255, 255, 255, 0) 100%
    )`
    styles.backgroundSize = '200% 100%'
    styles.animation = 'shimmer 2s linear infinite'
  }
  
  return styles
})
</script>

<style scoped>
.skeleton-loader {
  background-color: #e2e8f0;
  border-radius: 0.375rem;
  position: relative;
  overflow: hidden;
}

.dark .skeleton-loader {
  background-color: #334155;
}

/* Variants */
.skeleton-text {
  height: 1rem;
  width: 100%;
  margin-bottom: 0.5rem;
}

.skeleton-title {
  height: 2rem;
  width: 60%;
  margin-bottom: 1rem;
}

.skeleton-avatar {
  width: 3rem;
  height: 3rem;
  border-radius: 9999px;
}

.skeleton-card {
  width: 100%;
  height: 12rem;
  border-radius: 0.75rem;
}

.skeleton-image {
  width: 100%;
  height: 16rem;
  border-radius: 0.5rem;
}

/* Shimmer animation */
@keyframes shimmer {
  0% {
    background-position: -200% 0;
  }
  100% {
    background-position: 200% 0;
  }
}
</style>
