<template>
  <Card padding="none">
    <div class="overflow-x-auto">
      <table class="w-full">
        <thead class="bg-gray-50 dark:bg-dark-700 border-b border-gray-200 dark:border-dark-600">
          <tr>
            <th class="px-3 py-4 text-center">
              <input
                type="checkbox"
                :checked="isAllSelected"
                @change="$emit('toggle-select-all')"
                class="w-4 h-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500 cursor-pointer"
              />
            </th>
            <th class="px-6 py-4 text-left text-xs font-semibold text-dark-700 dark:text-dark-300 uppercase tracking-wider">
              Référence
            </th>
            <th class="px-6 py-4 text-left text-xs font-semibold text-dark-700 dark:text-dark-300 uppercase tracking-wider">
              Client
            </th>
            <th class="px-6 py-4 text-left text-xs font-semibold text-dark-700 dark:text-dark-300 uppercase tracking-wider">
              Projet
            </th>
            <th class="px-6 py-4 text-left text-xs font-semibold text-dark-700 dark:text-dark-300 uppercase tracking-wider">
              Montant
            </th>
            <th class="px-6 py-4 text-left text-xs font-semibold text-dark-700 dark:text-dark-300 uppercase tracking-wider">
              Date
            </th>
            <th class="px-6 py-4 text-left text-xs font-semibold text-dark-700 dark:text-dark-300 uppercase tracking-wider">
              Statut
            </th>
            <th class="px-6 py-4 text-right text-xs font-semibold text-dark-700 dark:text-dark-300 uppercase tracking-wider">
              Actions
            </th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-200 dark:divide-dark-600">
          <tr
            v-for="quote in quotes"
            :key="quote.id"
            :class="[
              'hover:bg-gray-50 dark:hover:bg-dark-700/50 transition-colors',
              { 'bg-primary-50 dark:bg-primary-900/20': isSelected(quote.id) }
            ]"
          >
            <td class="px-3 py-4 text-center">
              <input
                type="checkbox"
                :checked="isSelected(quote.id)"
                @change="$emit('toggle-selection', quote.id)"
                class="w-4 h-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500 cursor-pointer"
              />
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span class="text-sm font-medium text-dark-800 dark:text-dark-100">
                #{{ quote.quote_number }}
              </span>
            </td>
            <td class="px-6 py-4">
              <div class="text-sm">
                <div class="font-medium text-dark-800 dark:text-dark-100">{{ quote.client_name }}</div>
                <div class="text-dark-600 dark:text-dark-400">{{ quote.client_email }}</div>
              </div>
            </td>
            <td class="px-6 py-4">
              <div class="text-sm text-dark-800 dark:text-dark-100">
                {{ quote.project_type?.name || 'N/A' }}
              </div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm">
                <div class="font-semibold text-dark-800 dark:text-dark-100">
                  {{ formatAmount(quote.total_price) }}
                </div>
                <div v-if="quote.discount_amount && quote.discount_amount > 0" class="text-xs text-green-600 dark:text-green-400">
                  Remise: -{{ formatAmount(quote.discount_amount) }}
                </div>
              </div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span class="text-sm text-dark-600 dark:text-dark-400">
                {{ formatShortDate(quote.created_at) }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <StatusBadge :status="quote.status" />
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-right">
              <div class="flex items-center justify-end gap-2">
                <router-link
                  :to="`/devis/${quote.id}`"
                  class="text-primary-600 hover:text-primary-700 dark:text-primary-400 font-medium text-sm"
                >
                  Voir
                </router-link>
                <button
                  @click="$emit('edit', quote)"
                  class="text-indigo-600 hover:text-indigo-700 dark:text-indigo-400 font-medium text-sm"
                >
                  Modifier
                </button>
                <button
                  v-if="['draft', 'viewed', 'rejected'].includes(quote.status)"
                  @click="$emit('send', quote.id)"
                  :disabled="sending === quote.id"
                  class="text-green-600 hover:text-green-700 dark:text-green-400 font-medium text-sm disabled:opacity-50"
                  :title="quote.status === 'draft' ? 'Envoyer le devis' : 'Renvoyer le devis'"
                >
                  {{ sending === quote.id ? 'Envoi...' : (quote.status === 'draft' ? 'Envoyer' : 'Renvoyer') }}
                </button>
                <button
                  @click="$emit('download', quote.id, quote.quote_number)"
                  :disabled="downloading === quote.id"
                  class="text-blue-600 hover:text-blue-700 dark:text-blue-400 font-medium text-sm disabled:opacity-50"
                >
                  {{ downloading === quote.id ? 'PDF...' : 'PDF' }}
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Pagination -->
    <div v-if="totalPages > 1" class="px-6 py-4 bg-gray-50 dark:bg-dark-700 border-t border-gray-200 dark:border-dark-600">
      <div class="flex items-center justify-between">
        <p class="text-sm text-dark-600 dark:text-dark-400">
          Affichage de {{ startIndex + 1 }} à {{ Math.min(endIndex, total) }} sur {{ total }} devis
        </p>
        <div class="flex gap-2">
          <Button
            size="sm"
            variant="secondary"
            :disabled="currentPage === 1"
            @click="$emit('previous-page')"
          >
            Précédent
          </Button>
          <span class="px-3 py-1 text-dark-700 dark:text-dark-300">
            Page {{ currentPage }} / {{ totalPages }}
          </span>
          <Button
            size="sm"
            variant="secondary"
            :disabled="currentPage === totalPages"
            @click="$emit('next-page')"
          >
            Suivant
          </Button>
        </div>
      </div>
    </div>
  </Card>
</template>

<script setup>
import { Card, Button, StatusBadge } from '@/components/ui'
import { formatAmount, formatShortDate } from '@/utils/formatters'

const props = defineProps({
  quotes: {
    type: Array,
    required: true
  },
  selectedQuotes: {
    type: Array,
    default: () => []
  },
  isAllSelected: {
    type: Boolean,
    default: false
  },
  sending: {
    type: Number,
    default: null
  },
  downloading: {
    type: Number,
    default: null
  },
  currentPage: {
    type: Number,
    default: 1
  },
  totalPages: {
    type: Number,
    default: 1
  },
  startIndex: {
    type: Number,
    default: 0
  },
  endIndex: {
    type: Number,
    default: 0
  },
  total: {
    type: Number,
    default: 0
  }
})

defineEmits(['toggle-selection', 'toggle-select-all', 'edit', 'send', 'download', 'previous-page', 'next-page'])

const isSelected = (quoteId) => {
  return props.selectedQuotes.includes(quoteId)
}
</script>
