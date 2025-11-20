<template>
  <Modal
    :show="show"
    :title="`Actions groupées (${selectedCount} sélectionné${selectedCount > 1 ? 's' : ''})`"
    size="md"
    @close="handleClose"
  >
    <template #content>
      <div class="space-y-4">
        <!-- Info message -->
        <div class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
          <div class="flex items-start">
            <svg class="w-5 h-5 text-blue-500 mt-0.5 mr-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <div class="text-sm text-blue-700 dark:text-blue-300">
              <p class="font-medium mb-1">
                {{ selectedCount }} devis sélectionné{{ selectedCount > 1 ? 's' : '' }}
              </p>
              <p class="text-blue-600 dark:text-blue-400">
                Choisissez une action à appliquer à tous les devis sélectionnés.
              </p>
            </div>
          </div>
        </div>

        <!-- Action buttons -->
        <div class="grid grid-cols-1 gap-3">
          <!-- Send quotes -->
          <button
            v-if="canSendQuotes"
            @click="handleAction('send')"
            :disabled="processing"
            class="flex items-center justify-between p-4 rounded-lg border-2 border-gray-200 dark:border-dark-600 hover:border-green-500 dark:hover:border-green-500 hover:bg-green-50 dark:hover:bg-green-900/20 transition-all group disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <div class="flex items-center">
              <div class="w-10 h-10 rounded-lg bg-green-100 dark:bg-green-900/40 flex items-center justify-center group-hover:bg-green-200 dark:group-hover:bg-green-900/60 transition-colors">
                <svg class="w-5 h-5 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                </svg>
              </div>
              <div class="ml-4 text-left">
                <p class="font-semibold text-dark-800 dark:text-dark-100">Envoyer tous les devis</p>
                <p class="text-sm text-dark-600 dark:text-dark-400">Envoie par email aux clients</p>
              </div>
            </div>
            <svg class="w-5 h-5 text-dark-400 group-hover:text-green-600 dark:group-hover:text-green-400 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
            </svg>
          </button>

          <!-- Export Excel -->
          <button
            @click="handleAction('export-excel')"
            :disabled="processing"
            class="flex items-center justify-between p-4 rounded-lg border-2 border-gray-200 dark:border-dark-600 hover:border-blue-500 dark:hover:border-blue-500 hover:bg-blue-50 dark:hover:bg-blue-900/20 transition-all group disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <div class="flex items-center">
              <div class="w-10 h-10 rounded-lg bg-blue-100 dark:bg-blue-900/40 flex items-center justify-center group-hover:bg-blue-200 dark:group-hover:bg-blue-900/60 transition-colors">
                <svg class="w-5 h-5 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
              </div>
              <div class="ml-4 text-left">
                <p class="font-semibold text-dark-800 dark:text-dark-100">Exporter en Excel</p>
                <p class="text-sm text-dark-600 dark:text-dark-400">Télécharge un fichier .xlsx</p>
              </div>
            </div>
            <svg class="w-5 h-5 text-dark-400 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
            </svg>
          </button>

          <!-- Export PDF -->
          <button
            @click="handleAction('export-pdf')"
            :disabled="processing"
            class="flex items-center justify-between p-4 rounded-lg border-2 border-gray-200 dark:border-dark-600 hover:border-red-500 dark:hover:border-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 transition-all group disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <div class="flex items-center">
              <div class="w-10 h-10 rounded-lg bg-red-100 dark:bg-red-900/40 flex items-center justify-center group-hover:bg-red-200 dark:group-hover:bg-red-900/60 transition-colors">
                <svg class="w-5 h-5 text-red-600 dark:text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"></path>
                </svg>
              </div>
              <div class="ml-4 text-left">
                <p class="font-semibold text-dark-800 dark:text-dark-100">Exporter en PDF</p>
                <p class="text-sm text-dark-600 dark:text-dark-400">Génère un rapport PDF</p>
              </div>
            </div>
            <svg class="w-5 h-5 text-dark-400 group-hover:text-red-600 dark:group-hover:text-red-400 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
            </svg>
          </button>

          <!-- Delete quotes (dangerous action) -->
          <button
            v-if="canDeleteQuotes"
            @click="handleAction('delete')"
            :disabled="processing"
            class="flex items-center justify-between p-4 rounded-lg border-2 border-red-200 dark:border-red-900 hover:border-red-500 dark:hover:border-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 transition-all group disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <div class="flex items-center">
              <div class="w-10 h-10 rounded-lg bg-red-100 dark:bg-red-900/40 flex items-center justify-center group-hover:bg-red-200 dark:group-hover:bg-red-900/60 transition-colors">
                <svg class="w-5 h-5 text-red-600 dark:text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                </svg>
              </div>
              <div class="ml-4 text-left">
                <p class="font-semibold text-red-600 dark:text-red-400">Supprimer les devis</p>
                <p class="text-sm text-dark-600 dark:text-dark-400">Action irréversible</p>
              </div>
            </div>
            <svg class="w-5 h-5 text-dark-400 group-hover:text-red-600 dark:group-hover:text-red-400 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
            </svg>
          </button>
        </div>

        <!-- Processing indicator -->
        <div v-if="processing" class="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-4">
          <div class="flex items-center">
            <svg class="animate-spin w-5 h-5 text-yellow-500 mr-3" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <p class="text-sm font-medium text-yellow-700 dark:text-yellow-300">
              {{ processingMessage }}
            </p>
          </div>
        </div>
      </div>
    </template>

    <template #footer>
      <div class="flex justify-end">
        <Button
          variant="secondary"
          @click="handleClose"
          :disabled="processing"
        >
          Fermer
        </Button>
      </div>
    </template>
  </Modal>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Modal, Button } from '@/components/ui'
import { QUOTE_STATUSES } from '@/utils/constants'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  selectedQuotes: {
    type: Array,
    default: () => []
  },
  quotes: {
    type: Array,
    default: () => []
  },
  processing: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close', 'send-all', 'export-excel', 'export-pdf', 'delete-all'])

const processingMessage = ref('')

// Selected count
const selectedCount = computed(() => props.selectedQuotes.length)

// Get selected quote objects
const selectedQuoteObjects = computed(() => {
  return props.quotes.filter(q => props.selectedQuotes.includes(q.id))
})

// Check if we can send quotes (only draft, viewed, rejected)
const canSendQuotes = computed(() => {
  return selectedQuoteObjects.value.some(q =>
    [QUOTE_STATUSES.DRAFT, QUOTE_STATUSES.VIEWED, QUOTE_STATUSES.REJECTED].includes(q.status)
  )
})

// Check if we can delete quotes (only draft)
const canDeleteQuotes = computed(() => {
  return selectedQuoteObjects.value.every(q => q.status === QUOTE_STATUSES.DRAFT)
})

// Handle action
const handleAction = (action) => {
  switch (action) {
    case 'send':
      processingMessage.value = `Envoi de ${selectedCount.value} devis en cours...`
      emit('send-all')
      break

    case 'export-excel':
      processingMessage.value = `Export Excel de ${selectedCount.value} devis en cours...`
      emit('export-excel')
      break

    case 'export-pdf':
      processingMessage.value = `Génération PDF de ${selectedCount.value} devis en cours...`
      emit('export-pdf')
      break

    case 'delete':
      if (confirm(`Êtes-vous sûr de vouloir supprimer ${selectedCount.value} devis ? Cette action est irréversible.`)) {
        processingMessage.value = `Suppression de ${selectedCount.value} devis en cours...`
        emit('delete-all')
      }
      break
  }
}

// Handle close
const handleClose = () => {
  if (!props.processing) {
    processingMessage.value = ''
    emit('close')
  }
}
</script>
