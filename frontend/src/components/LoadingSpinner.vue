<template>
  <div :class="['flex items-center justify-center', containerClass]">
    <div class="text-center">
      <!-- Spinner animé -->
      <div
        v-if="type === 'spinner'"
        :class="[
          'spinner mx-auto',
          sizeClasses[size]
        ]"
      ></div>

      <!-- Dots animés -->
      <div
        v-else-if="type === 'dots'"
        class="flex space-x-2"
      >
        <div
          v-for="i in 3"
          :key="i"
          :class="[
            'rounded-full bg-primary-600 animate-bounce',
            dotSizeClasses[size]
          ]"
          :style="{ animationDelay: `${i * 0.1}s` }"
        ></div>
      </div>

      <!-- Pulse -->
      <div
        v-else-if="type === 'pulse'"
        :class="[
          'rounded-full bg-primary-600 animate-pulse',
          sizeClasses[size]
        ]"
      ></div>

      <!-- Message optionnel -->
      <p
        v-if="message"
        class="mt-4 text-dark-600 dark:text-dark-300"
        :class="textSizeClasses[size]"
      >
        {{ message }}
      </p>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  type: {
    type: String,
    default: 'spinner',
    validator: (value) => ['spinner', 'dots', 'pulse'].includes(value)
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg', 'xl'].includes(value)
  },
  message: {
    type: String,
    default: ''
  },
  containerClass: {
    type: String,
    default: 'py-12'
  }
})

const sizeClasses = {
  sm: 'w-6 h-6',
  md: 'w-12 h-12',
  lg: 'w-16 h-16',
  xl: 'w-24 h-24'
}

const dotSizeClasses = {
  sm: 'w-2 h-2',
  md: 'w-3 h-3',
  lg: 'w-4 h-4',
  xl: 'w-6 h-6'
}

const textSizeClasses = {
  sm: 'text-sm',
  md: 'text-base',
  lg: 'text-lg',
  xl: 'text-xl'
}
</script>
