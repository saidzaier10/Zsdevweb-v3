<template>
  <div 
    @click="$emit('select')"
    :class="[
      'relative p-6 rounded-xl cursor-pointer transition-all duration-300 group',
      selected 
        ? 'bg-primary-50/80 dark:bg-primary-900/20 border-2 border-primary-500 shadow-glow' 
        : 'bg-white/60 dark:bg-dark-800/60 border-2 border-transparent hover:border-primary-300 dark:hover:border-primary-700 hover:-translate-y-1 backdrop-blur-sm'
    ]"
  >
    <!-- Checkmark for selected state -->
    <div 
      v-if="selected"
      class="absolute top-4 right-4 w-6 h-6 bg-primary-500 rounded-full flex items-center justify-center text-white animate-scale-in"
    >
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
      </svg>
    </div>

    <h3 
      class="text-xl font-bold mb-2 transition-colors"
      :class="selected ? 'text-primary-600 dark:text-primary-400' : 'text-dark-900 dark:text-white'"
    >
      {{ title }}
    </h3>
    
    <p 
      class="text-sm mb-4 transition-colors"
      :class="selected ? 'text-dark-700 dark:text-dark-300' : 'text-dark-600 dark:text-dark-400'"
    >
      {{ description }}
    </p>
    
    <div class="flex items-center justify-between mt-auto">
      <p 
        class="text-2xl font-bold transition-colors"
        :class="selected ? 'text-primary-600 dark:text-primary-400' : 'text-dark-900 dark:text-white'"
      >
        {{ priceDisplay }}
      </p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true
  },
  description: {
    type: String,
    required: true
  },
  priceDisplay: {
    type: String,
    required: true
  },
  selected: {
    type: Boolean,
    default: false
  }
})

defineEmits(['select'])
</script>

<style scoped>
.shadow-glow {
  box-shadow: 0 0 15px rgba(59, 130, 246, 0.3);
}
</style>
