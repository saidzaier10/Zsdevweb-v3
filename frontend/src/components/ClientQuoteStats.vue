<template>
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
    <!-- Total des devis -->
    <div class="bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl shadow-lg p-6 text-white">
      <div class="flex items-center justify-between mb-2">
        <div>
          <p class="text-sm font-medium opacity-90">Total des devis</p>
          <p class="text-3xl font-bold mt-1">{{ quotes.length }}</p>
        </div>
        <div class="bg-white/20 rounded-full p-3">
          <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
          </svg>
        </div>
      </div>
      <div class="mt-2 text-sm opacity-80">
        {{ pendingCount }} en attente
      </div>
    </div>

    <!-- Devis acceptés -->
    <div class="bg-gradient-to-br from-green-500 to-green-600 rounded-xl shadow-lg p-6 text-white">
      <div class="flex items-center justify-between mb-2">
        <div>
          <p class="text-sm font-medium opacity-90">Acceptés</p>
          <p class="text-3xl font-bold mt-1">{{ acceptedCount }}</p>
        </div>
        <div class="bg-white/20 rounded-full p-3">
          <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
        </div>
      </div>
      <div class="mt-2 text-sm opacity-80">
        {{ acceptedPercentage }}% du total
      </div>
    </div>

    <!-- Montant total -->
    <div class="bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl shadow-lg p-6 text-white">
      <div class="flex items-center justify-between mb-2">
        <div>
          <p class="text-sm font-medium opacity-90">Montant total</p>
          <p class="text-3xl font-bold mt-1">{{ totalAmount }} €</p>
        </div>
        <div class="bg-white/20 rounded-full p-3">
          <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
        </div>
      </div>
      <div class="mt-2 text-sm opacity-80">
        {{ acceptedAmount }} € accepté
      </div>
    </div>

    <!-- Taux de conversion -->
    <div class="bg-gradient-to-br from-amber-500 to-amber-600 rounded-xl shadow-lg p-6 text-white">
      <div class="flex items-center justify-between mb-2">
        <div>
          <p class="text-sm font-medium opacity-90">Taux de conversion</p>
          <p class="text-3xl font-bold mt-1">{{ conversionRate }}%</p>
        </div>
        <div class="bg-white/20 rounded-full p-3">
          <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path>
          </svg>
        </div>
      </div>
      <div class="mt-2 text-sm opacity-80">
        {{ sentCount }} envoyé{{ sentCount > 1 ? 's' : '' }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  quotes: {
    type: Array,
    required: true
  }
})

const acceptedCount = computed(() => {
  return props.quotes.filter(q => q.status === 'accepted').length
})

const pendingCount = computed(() => {
  return props.quotes.filter(q => ['sent', 'viewed'].includes(q.status)).length
})

const sentCount = computed(() => {
  return props.quotes.filter(q => ['sent', 'viewed', 'accepted', 'rejected'].includes(q.status)).length
})

const totalAmount = computed(() => {
  const total = props.quotes.reduce((sum, q) => sum + parseFloat(q.total_price || 0), 0)
  return Math.round(total)
})

const acceptedAmount = computed(() => {
  const total = props.quotes
    .filter(q => q.status === 'accepted')
    .reduce((sum, q) => sum + parseFloat(q.total_price || 0), 0)
  return Math.round(total)
})

const acceptedPercentage = computed(() => {
  if (props.quotes.length === 0) return 0
  return Math.round((acceptedCount.value / props.quotes.length) * 100)
})

const conversionRate = computed(() => {
  if (sentCount.value === 0) return 0
  return Math.round((acceptedCount.value / sentCount.value) * 100)
})
</script>
