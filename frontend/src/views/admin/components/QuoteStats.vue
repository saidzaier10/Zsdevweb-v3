<template>
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
    <!-- Total des devis -->
    <Card padding="md">
      <div class="flex items-center justify-between mb-2">
        <h3 class="text-sm font-medium text-dark-600 dark:text-dark-400">Total</h3>
        <svg class="w-8 h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
        </svg>
      </div>
      <p class="text-3xl font-bold text-dark-800 dark:text-dark-100">
        {{ statistics.total_quotes || 0 }}
      </p>
    </Card>

    <!-- Devis envoyés -->
    <Card padding="md">
      <div class="flex items-center justify-between mb-2">
        <h3 class="text-sm font-medium text-dark-600 dark:text-dark-400">Envoyés</h3>
        <svg class="w-8 h-8 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
        </svg>
      </div>
      <p class="text-3xl font-bold text-dark-800 dark:text-dark-100">
        {{ countByStatus(QUOTE_STATUSES.SENT) }}
      </p>
    </Card>

    <!-- Devis acceptés -->
    <Card padding="md">
      <div class="flex items-center justify-between mb-2">
        <h3 class="text-sm font-medium text-dark-600 dark:text-dark-400">Acceptés</h3>
        <svg class="w-8 h-8 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
      </div>
      <p class="text-3xl font-bold text-dark-800 dark:text-dark-100">
        {{ countByStatus(QUOTE_STATUSES.ACCEPTED) }}
      </p>
    </Card>

    <!-- Montant total -->
    <Card padding="md">
      <div class="flex items-center justify-between mb-2">
        <h3 class="text-sm font-medium text-dark-600 dark:text-dark-400">Montant total</h3>
        <svg class="w-8 h-8 text-yellow-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
      </div>
      <p class="text-3xl font-bold text-dark-800 dark:text-dark-100">
        {{ formatAmount(statistics.total_amount || 0) }}
      </p>
    </Card>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Card } from '@/components/ui'
import { formatAmount } from '@/utils/formatters'
import { QUOTE_STATUSES } from '@/utils/constants'

const props = defineProps({
  statistics: {
    type: Object,
    required: true
  },
  quotes: {
    type: Array,
    default: () => []
  }
})

const countByStatus = (status) => {
  return props.quotes.filter(q => q.status === status).length
}
</script>
