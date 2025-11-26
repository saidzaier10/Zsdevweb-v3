<template>
  <div class="relative mb-6">
    <input
      v-if="type !== 'textarea'"
      :id="id"
      :type="type"
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      class="peer block w-full px-4 py-3 bg-white/50 dark:bg-dark-800/50 border-2 border-gray-200 dark:border-dark-600 rounded-xl text-dark-900 dark:text-white placeholder-transparent focus:outline-none focus:border-primary-500 focus:ring-0 transition-all duration-300"
      :class="{ 'border-red-500 focus:border-red-500': error }"
      :placeholder="label"
      v-bind="$attrs"
    />
    <textarea
      v-else
      :id="id"
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      class="peer block w-full px-4 py-3 bg-white/50 dark:bg-dark-800/50 border-2 border-gray-200 dark:border-dark-600 rounded-xl text-dark-900 dark:text-white placeholder-transparent focus:outline-none focus:border-primary-500 focus:ring-0 transition-all duration-300 resize-none"
      :class="{ 'border-red-500 focus:border-red-500': error }"
      :placeholder="label"
      v-bind="$attrs"
    ></textarea>

    <label
      :for="id"
      class="absolute left-4 -top-2.5 bg-white dark:bg-dark-800 px-1 text-sm text-gray-500 dark:text-gray-400 transition-all duration-300 peer-placeholder-shown:text-base peer-placeholder-shown:text-gray-400 peer-placeholder-shown:top-3.5 peer-focus:-top-2.5 peer-focus:text-sm peer-focus:text-primary-500"
      :class="{ 'text-red-500 peer-focus:text-red-500': error }"
    >
      {{ label }} <span v-if="required" class="text-red-500">*</span>
    </label>

    <!-- Icon -->
    <div v-if="icon" class="absolute right-4 top-3.5 text-gray-400 peer-focus:text-primary-500 transition-colors duration-300">
      <slot name="icon"></slot>
    </div>

    <!-- Error Message -->
    <p v-if="error" class="mt-1 text-xs text-red-500 animate-slide-up">
      {{ error }}
    </p>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: {
    type: [String, Number],
    default: ''
  },
  label: {
    type: String,
    required: true
  },
  type: {
    type: String,
    default: 'text'
  },
  id: {
    type: String,
    required: true
  },
  required: {
    type: Boolean,
    default: false
  },
  error: {
    type: String,
    default: ''
  },
  icon: {
    type: Boolean,
    default: false
  }
})

defineEmits(['update:modelValue'])
</script>

<style scoped>
/* Ensure label background matches parent background for seamless floating effect */
input:-webkit-autofill,
input:-webkit-autofill:hover, 
input:-webkit-autofill:focus, 
input:-webkit-autofill:active{
    -webkit-box-shadow: 0 0 0 30px white inset !important;
    -webkit-text-fill-color: inherit !important;
    transition: background-color 5000s ease-in-out 0s;
}

.dark input:-webkit-autofill,
.dark input:-webkit-autofill:hover, 
.dark input:-webkit-autofill:focus, 
.dark input:-webkit-autofill:active{
    -webkit-box-shadow: 0 0 0 30px #1e293b inset !important;
    -webkit-text-fill-color: white !important;
}
</style>
