<template>
  <Teleport to="body">
    <Transition name="modal">
      <div
        v-if="modelValue"
        class="fixed inset-0 z-50 overflow-y-auto"
        @click.self="handleBackdropClick"
      >
        <!-- Overlay -->
        <div
          class="fixed inset-0 bg-gray-500 dark:bg-gray-900 bg-opacity-75 dark:bg-opacity-75 transition-opacity"
          @click="handleBackdropClick"
        ></div>

        <!-- Modal Container -->
        <div class="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
          <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>

          <!-- Modal Panel -->
          <div
            :class="modalClasses"
            role="dialog"
            aria-modal="true"
          >
            <!-- Header -->
            <div v-if="title || $slots.header || closable" :class="headerClasses">
              <slot name="header">
                <div class="flex items-center justify-between">
                  <h3 class="text-2xl font-bold text-dark-900 dark:text-white">
                    {{ title }}
                  </h3>
                  <button
                    v-if="closable"
                    @click="close"
                    class="text-gray-400 hover:text-gray-500 dark:hover:text-gray-300 transition-colors"
                  >
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                    </svg>
                  </button>
                </div>
              </slot>
            </div>

            <!-- Body -->
            <div :class="bodyClasses">
              <slot />
            </div>

            <!-- Footer -->
            <div v-if="$slots.footer" :class="footerClasses">
              <slot name="footer" />
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { computed, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true
  },
  title: String,
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg', 'xl', 'full'].includes(value)
  },
  closable: {
    type: Boolean,
    default: true
  },
  closeOnBackdrop: {
    type: Boolean,
    default: true
  },
  persistent: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'close'])

const modalClasses = computed(() => {
  const sizes = {
    sm: 'sm:max-w-sm',
    md: 'sm:max-w-2xl',
    lg: 'sm:max-w-4xl',
    xl: 'sm:max-w-6xl',
    full: 'sm:max-w-full sm:mx-4'
  }

  return [
    'relative inline-block align-bottom bg-white dark:bg-dark-800 rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:w-full',
    sizes[props.size]
  ]
})

const headerClasses = computed(() => {
  return 'bg-white dark:bg-dark-800 px-6 pt-5 pb-4 sm:p-6 border-b border-gray-200 dark:border-dark-700'
})

const bodyClasses = computed(() => {
  return 'bg-white dark:bg-dark-800 px-6 py-4 sm:p-6'
})

const footerClasses = computed(() => {
  return 'bg-gray-50 dark:bg-dark-700 px-6 py-4 sm:px-6 sm:flex sm:flex-row-reverse gap-3'
})

const handleBackdropClick = () => {
  if (props.closeOnBackdrop && !props.persistent) {
    close()
  }
}

const close = () => {
  emit('update:modelValue', false)
  emit('close')
}

// Bloquer le scroll du body quand le modal est ouvert
watch(() => props.modelValue, (isOpen) => {
  if (isOpen) {
    document.body.style.overflow = 'hidden'
  } else {
    document.body.style.overflow = ''
  }
})
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
</style>
