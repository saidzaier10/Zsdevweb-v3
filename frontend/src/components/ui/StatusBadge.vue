<template>
  <span :class="badgeClasses">
    {{ label }}
  </span>
</template>

<script setup>
import { computed } from 'vue'
import { QUOTE_STATUS_LABELS, QUOTE_STATUS_CLASSES } from '@/utils/constants'

const props = defineProps({
  status: {
    type: String,
    required: true
  },
  uppercase: {
    type: Boolean,
    default: true
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg'].includes(value)
  }
})

const label = computed(() => {
  const text = QUOTE_STATUS_LABELS[props.status] || props.status
  return props.uppercase ? text.toUpperCase() : text
})

const sizeClasses = computed(() => {
  const sizes = {
    sm: 'px-2 py-0.5 text-xs',
    md: 'px-3 py-1 text-xs',
    lg: 'px-4 py-1.5 text-sm'
  }
  return sizes[props.size]
})

const badgeClasses = computed(() => {
  return [
    'inline-flex items-center rounded-full font-bold tracking-wide',
    sizeClasses.value,
    QUOTE_STATUS_CLASSES[props.status] || 'bg-gray-100 text-gray-800'
  ]
})
</script>
