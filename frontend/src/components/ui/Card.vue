<template>
  <div :class="cardClasses">
    <!-- En-tête optionnel -->
    <div v-if="title || $slots.header" :class="headerClasses">
      <slot name="header">
        <h3 v-if="title" class="text-lg font-semibold text-dark-800 dark:text-dark-100">
          {{ title }}
        </h3>
        <p v-if="subtitle" class="text-sm text-dark-600 dark:text-dark-300 mt-1">
          {{ subtitle }}
        </p>
      </slot>
    </div>

    <!-- Contenu principal -->
    <div :class="contentClasses">
      <slot />
    </div>

    <!-- Pied de page optionnel -->
    <div v-if="$slots.footer" :class="footerClasses">
      <slot name="footer" />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { CARD_CLASSES } from '@/utils/constants'

const props = defineProps({
  title: String,
  subtitle: String,
  padding: {
    type: String,
    default: 'md',
    validator: (value) => ['none', 'sm', 'md', 'lg'].includes(value)
  },
  hoverable: {
    type: Boolean,
    default: false
  },
  clickable: {
    type: Boolean,
    default: false
  },
  noBorder: {
    type: Boolean,
    default: false
  }
})

const cardClasses = computed(() => {
  return [
    CARD_CLASSES.base,
    {
      'hover:shadow-lg transition-shadow duration-300': props.hoverable,
      'cursor-pointer hover:shadow-xl transition-all duration-300': props.clickable,
      'border-0': props.noBorder
    }
  ]
})

const headerClasses = computed(() => {
  const paddingClass = CARD_CLASSES.padding[props.padding]
  return [
    paddingClass,
    'border-b border-gray-200 dark:border-dark-700'
  ]
})

const contentClasses = computed(() => {
  return CARD_CLASSES.padding[props.padding]
})

const footerClasses = computed(() => {
  const paddingClass = CARD_CLASSES.padding[props.padding]
  return [
    paddingClass,
    'border-t border-gray-200 dark:border-dark-700 bg-gray-50 dark:bg-dark-700'
  ]
})
</script>
