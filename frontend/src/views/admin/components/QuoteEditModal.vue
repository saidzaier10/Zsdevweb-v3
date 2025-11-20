<template>
  <Modal
    :modelValue="show"
    :title="modalTitle"
    size="lg"
    @close="handleClose"
  >
    <template #content>
      <form @submit.prevent="handleSubmit" class="space-y-6">
        <!-- Informations Client -->
        <div class="bg-gray-50 dark:bg-dark-700 p-4 rounded-lg">
          <h3 class="text-lg font-semibold text-dark-800 dark:text-dark-100 mb-4">
            Informations Client
          </h3>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Input
              v-model="formData.client_name"
              label="Nom du client"
              placeholder="Nom complet"
              :error="errors.client_name"
              :disabled="saving"
              required
            />

            <Input
              v-model="formData.client_email"
              label="Email du client"
              type="email"
              placeholder="email@example.com"
              :error="errors.client_email"
              :disabled="saving"
              required
            />
          </div>
        </div>

        <!-- Remise -->
        <div class="bg-gray-50 dark:bg-dark-700 p-4 rounded-lg">
          <h3 class="text-lg font-semibold text-dark-800 dark:text-dark-100 mb-4">
            Remise
          </h3>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label class="block text-sm font-medium text-dark-700 dark:text-dark-300 mb-2">
                Type de remise
              </label>
              <select
                v-model="formData.discount_type"
                class="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-dark-600 bg-white dark:bg-dark-700 text-dark-800 dark:text-dark-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                :disabled="saving"
              >
                <option value="">Aucune remise</option>
                <option value="percent">Pourcentage (%)</option>
                <option value="fixed">Montant fixe (€)</option>
              </select>
            </div>

            <Input
              v-if="formData.discount_type"
              v-model="formData.discount_value"
              label="Valeur de la remise"
              type="number"
              step="0.01"
              min="0"
              :max="formData.discount_type === 'percent' ? 100 : undefined"
              :placeholder="formData.discount_type === 'percent' ? '10' : '100.00'"
              :error="errors.discount_value"
              :disabled="saving"
            />

            <Input
              v-if="formData.discount_type"
              v-model="formData.discount_reason"
              label="Raison de la remise"
              placeholder="Ex: Client fidèle"
              :error="errors.discount_reason"
              :disabled="saving"
            />
          </div>

          <!-- Aperçu de la remise -->
          <div v-if="discountPreview" class="mt-4 p-3 bg-green-50 dark:bg-green-900/20 rounded-lg">
            <div class="flex items-center justify-between text-sm">
              <span class="text-dark-700 dark:text-dark-300">Montant original:</span>
              <span class="font-semibold text-dark-800 dark:text-dark-100">
                {{ formatAmount(quote?.total_price || 0) }}
              </span>
            </div>
            <div class="flex items-center justify-between text-sm text-green-600 dark:text-green-400 mt-1">
              <span>Remise:</span>
              <span class="font-semibold">-{{ formatAmount(discountPreview.amount) }}</span>
            </div>
            <div class="flex items-center justify-between text-base font-bold mt-2 pt-2 border-t border-green-200 dark:border-green-700">
              <span class="text-dark-800 dark:text-dark-100">Nouveau total:</span>
              <span class="text-primary-600 dark:text-primary-400">
                {{ formatAmount(discountPreview.newTotal) }}
              </span>
            </div>
          </div>
        </div>

        <!-- Notes / Description -->
        <div>
          <label class="block text-sm font-medium text-dark-700 dark:text-dark-300 mb-2">
            Notes internes
          </label>
          <textarea
            v-model="formData.notes"
            rows="4"
            class="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-dark-600 bg-white dark:bg-dark-700 text-dark-800 dark:text-dark-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none"
            placeholder="Notes internes visibles uniquement par l'équipe..."
            :disabled="saving"
          ></textarea>
        </div>
      </form>
    </template>

    <template #footer>
      <div class="flex justify-end gap-3">
        <Button
          variant="secondary"
          @click="handleClose"
          :disabled="saving"
        >
          Annuler
        </Button>
        <Button
          variant="primary"
          @click="handleSubmit"
          :disabled="saving || !isFormValid"
        >
          <template v-if="saving" #icon-left>
            <svg class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          </template>
          {{ saving ? 'Enregistrement...' : 'Enregistrer' }}
        </Button>
      </div>
    </template>
  </Modal>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { Modal, Input, Button } from '@/components/ui'
import { validateEmail } from '@/utils/validators'
import { formatAmount } from '@/utils/formatters'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  quote: {
    type: Object,
    default: null
  },
  saving: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close', 'save'])

// Form data
const formData = ref({
  client_name: '',
  client_email: '',
  discount_type: '',
  discount_value: 0,
  discount_reason: '',
  notes: ''
})

// Errors
const errors = ref({})

// Modal title
const modalTitle = computed(() => {
  return props.quote
    ? `Modifier le devis #${props.quote.quote_number}`
    : 'Nouveau devis'
})

// Discount preview calculation
const discountPreview = computed(() => {
  if (!formData.value.discount_type || !formData.value.discount_value || !props.quote) {
    return null
  }

  const originalAmount = parseFloat(props.quote.total_price || 0)
  const discountValue = parseFloat(formData.value.discount_value || 0)

  let discountAmount = 0

  if (formData.value.discount_type === 'percent') {
    discountAmount = (originalAmount * discountValue) / 100
  } else if (formData.value.discount_type === 'fixed') {
    discountAmount = discountValue
  }

  // Ensure discount doesn't exceed total
  discountAmount = Math.min(discountAmount, originalAmount)

  return {
    amount: discountAmount,
    newTotal: Math.max(0, originalAmount - discountAmount)
  }
})

// Form validation
const isFormValid = computed(() => {
  if (!formData.value.client_name?.trim()) return false
  if (!formData.value.client_email?.trim()) return false

  const emailValidation = validateEmail(formData.value.client_email, true)
  if (!emailValidation.valid) return false

  // Validate discount if present
  if (formData.value.discount_type) {
    const discountValue = parseFloat(formData.value.discount_value || 0)
    if (discountValue <= 0) return false
    if (formData.value.discount_type === 'percent' && discountValue > 100) return false
  }

  return true
})

// Watch for quote changes to populate form
watch(() => props.quote, (newQuote) => {
  if (newQuote) {
    formData.value = {
      client_name: newQuote.client_name || '',
      client_email: newQuote.client_email || '',
      discount_type: newQuote.discount_type || '',
      discount_value: newQuote.discount_value || 0,
      discount_reason: newQuote.discount_reason || '',
      notes: newQuote.notes || ''
    }
    errors.value = {}
  }
}, { immediate: true })

// Watch for modal close to reset form
watch(() => props.show, (isShown) => {
  if (!isShown) {
    errors.value = {}
  }
})

// Validate form
const validateForm = () => {
  errors.value = {}

  // Validate client name
  if (!formData.value.client_name?.trim()) {
    errors.value.client_name = 'Le nom du client est requis'
  }

  // Validate email
  const emailValidation = validateEmail(formData.value.client_email, true)
  if (!emailValidation.valid) {
    errors.value.client_email = emailValidation.error
  }

  // Validate discount
  if (formData.value.discount_type) {
    const discountValue = parseFloat(formData.value.discount_value || 0)

    if (discountValue <= 0) {
      errors.value.discount_value = 'La valeur de la remise doit être supérieure à 0'
    }

    if (formData.value.discount_type === 'percent' && discountValue > 100) {
      errors.value.discount_value = 'La remise ne peut pas dépasser 100%'
    }

    if (formData.value.discount_type === 'fixed') {
      const total = parseFloat(props.quote?.total_price || 0)
      if (discountValue > total) {
        errors.value.discount_value = 'La remise ne peut pas dépasser le montant total'
      }
    }
  }

  return Object.keys(errors.value).length === 0
}

// Handle submit
const handleSubmit = () => {
  if (!validateForm()) {
    return
  }

  // Prepare data for save
  const dataToSave = { ...formData.value }

  // Clean discount data if no discount type selected
  if (!dataToSave.discount_type) {
    dataToSave.discount_value = 0
    dataToSave.discount_reason = ''
  }

  emit('save', dataToSave)
}

// Handle close
const handleClose = () => {
  if (!props.saving) {
    emit('close')
  }
}
</script>
