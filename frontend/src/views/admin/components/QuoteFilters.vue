<template>
  <Card padding="md" class="mb-6">
    <div class="flex flex-col lg:flex-row gap-4 mb-4">
      <!-- Barre de recherche -->
      <div class="flex-1">
        <div class="relative">
          <svg class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-dark-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
          </svg>
          <input
            :value="search"
            @input="$emit('update:search', $event.target.value)"
            type="text"
            placeholder="Rechercher par nom, email, référence..."
            class="w-full pl-10 pr-4 py-2 rounded-lg border border-gray-300 dark:border-dark-600 bg-white dark:bg-dark-700 text-dark-800 dark:text-dark-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          />
        </div>
      </div>

      <!-- Filtre par statut -->
      <select
        :value="status"
        @change="$emit('update:status', $event.target.value || null)"
        class="px-4 py-2 rounded-lg border border-gray-300 dark:border-dark-600 bg-white dark:bg-dark-700 text-dark-800 dark:text-dark-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
      >
        <option value="">Tous les statuts</option>
        <option :value="QUOTE_STATUSES.DRAFT">{{ QUOTE_STATUS_LABELS[QUOTE_STATUSES.DRAFT] }}</option>
        <option :value="QUOTE_STATUSES.SENT">{{ QUOTE_STATUS_LABELS[QUOTE_STATUSES.SENT] }}</option>
        <option :value="QUOTE_STATUSES.VIEWED">{{ QUOTE_STATUS_LABELS[QUOTE_STATUSES.VIEWED] }}</option>
        <option :value="QUOTE_STATUSES.ACCEPTED">{{ QUOTE_STATUS_LABELS[QUOTE_STATUSES.ACCEPTED] }}</option>
        <option :value="QUOTE_STATUSES.REJECTED">{{ QUOTE_STATUS_LABELS[QUOTE_STATUSES.REJECTED] }}</option>
        <option :value="QUOTE_STATUSES.EXPIRED">{{ QUOTE_STATUS_LABELS[QUOTE_STATUSES.EXPIRED] }}</option>
      </select>
    </div>

    <!-- Boutons d'export et actions -->
    <div class="flex flex-wrap gap-3">
      <Button
        v-if="filteredCount > 0"
        variant="success"
        size="md"
        @click="$emit('export-excel')"
      >
        <template #icon-left>
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
          </svg>
        </template>
        Exporter Excel
      </Button>

      <Button
        v-if="filteredCount > 0"
        variant="danger"
        size="md"
        @click="$emit('export-pdf')"
      >
        <template #icon-left>
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"></path>
          </svg>
        </template>
        Exporter PDF
      </Button>

      <slot name="extra-actions" />
    </div>
  </Card>
</template>

<script setup>
import { Card, Button } from '@/components/ui'
import { QUOTE_STATUSES, QUOTE_STATUS_LABELS } from '@/utils/constants'

defineProps({
  search: {
    type: String,
    default: ''
  },
  status: {
    type: String,
    default: null
  },
  filteredCount: {
    type: Number,
    default: 0
  }
})

defineEmits(['update:search', 'update:status', 'export-excel', 'export-pdf'])
</script>
