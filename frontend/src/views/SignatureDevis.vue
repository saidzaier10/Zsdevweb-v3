<template>
  <div class="min-h-screen bg-gray-50 dark:bg-dark-900 py-12 transition-colors duration-200">
    <div class="container mx-auto px-4 lg:px-8 max-w-4xl">
      <!-- Chargement -->
      <div v-if="loading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        <p class="mt-4 text-dark-600 dark:text-dark-300">Chargement du devis...</p>
      </div>

      <!-- Erreur -->
      <div v-else-if="error" class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-xl p-6 text-center">
        <svg class="w-12 h-12 mx-auto mb-4 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
        <h3 class="text-xl font-semibold text-red-800 dark:text-red-200 mb-2">Erreur</h3>
        <p class="text-red-700 dark:text-red-300">{{ error }}</p>
      </div>

      <!-- Devis déjà signé -->
      <div v-else-if="quote && quote.status === 'accepted'" class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-xl p-8 text-center">
        <svg class="w-16 h-16 mx-auto mb-4 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
        <h3 class="text-2xl font-semibold text-blue-800 dark:text-blue-200 mb-2">
          Devis déjà accepté
        </h3>
        <p class="text-blue-700 dark:text-blue-300 mb-6">
          Ce devis a déjà été accepté et signé.
        </p>
        <div v-if="quote.signed_at" class="text-sm text-blue-600 dark:text-blue-400">
          <p>Signé le {{ formatDate(quote.signed_at) }}</p>
        </div>
      </div>

      <!-- Formulaire de signature -->
      <div v-else-if="quote" class="space-y-6">
        <!-- En-tête -->
        <div class="bg-white dark:bg-dark-800 rounded-xl shadow-sm p-6 border border-gray-200 dark:border-dark-700">
          <h1 class="text-3xl font-display font-bold gradient-text mb-2">
            Signature du devis
          </h1>
          <p class="text-dark-600 dark:text-dark-400">
            Référence: #{{ quote.quote_number }}
          </p>
        </div>

        <!-- Récapitulatif du devis -->
        <div class="bg-white dark:bg-dark-800 rounded-xl shadow-sm p-6 border border-gray-200 dark:border-dark-700">
          <h2 class="text-xl font-semibold text-dark-800 dark:text-dark-100 mb-4">Récapitulatif du projet</h2>

          <div class="space-y-3">
            <div class="flex justify-between py-2">
              <span class="text-dark-700 dark:text-dark-300">Type de projet</span>
              <span class="font-semibold text-dark-800 dark:text-dark-100">{{ quote.project_type_detail.name }}</span>
            </div>
            <div class="flex justify-between py-2">
              <span class="text-dark-700 dark:text-dark-300">Design</span>
              <span class="font-semibold text-dark-800 dark:text-dark-100">{{ quote.design_option_detail.name }}</span>
            </div>
            <div class="flex justify-between py-2">
              <span class="text-dark-700 dark:text-dark-300">Complexité</span>
              <span class="font-semibold text-dark-800 dark:text-dark-100">{{ quote.complexity_level_detail.name }}</span>
            </div>
            <div v-if="quote.estimated_duration_days" class="flex justify-between py-2">
              <span class="text-dark-700 dark:text-dark-300">Durée estimée</span>
              <span class="font-semibold text-dark-800 dark:text-dark-100">{{ quote.estimated_duration_days }} jours</span>
            </div>
            <div class="flex justify-between py-4 border-t-2 border-gray-300 dark:border-dark-600">
              <span class="text-xl font-bold text-dark-800 dark:text-dark-100">Prix total</span>
              <span class="text-2xl font-bold gradient-text">{{ quote.total_ttc }} €</span>
            </div>
          </div>
        </div>

        <!-- Formulaire de signature -->
        <form @submit.prevent="submitSignature" class="bg-white dark:bg-dark-800 rounded-xl shadow-sm p-6 border border-gray-200 dark:border-dark-700">
          <h2 class="text-xl font-semibold text-dark-800 dark:text-dark-100 mb-4">Signer le devis</h2>

          <!-- Nom du signataire -->
          <div class="mb-6">
            <label for="signature_name" class="block text-sm font-medium text-dark-700 dark:text-dark-300 mb-2">
              Nom complet du signataire *
            </label>
            <input
              id="signature_name"
              v-model="signatureName"
              type="text"
              required
              class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-dark-600 bg-white dark:bg-dark-700 text-dark-800 dark:text-dark-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
              placeholder="Votre nom complet"
            />
          </div>

          <!-- Canvas de signature -->
          <div class="mb-6">
            <label class="block text-sm font-medium text-dark-700 dark:text-dark-300 mb-2">
              Signature électronique *
            </label>
            <div class="border-2 border-dashed border-gray-300 dark:border-dark-600 rounded-lg p-4 bg-gray-50 dark:bg-dark-700">
              <canvas
                ref="signatureCanvas"
                @mousedown="startDrawing"
                @mousemove="draw"
                @mouseup="stopDrawing"
                @mouseleave="stopDrawing"
                @touchstart.prevent="startDrawing"
                @touchmove.prevent="draw"
                @touchend.prevent="stopDrawing"
                class="w-full h-40 bg-white dark:bg-dark-800 rounded cursor-crosshair touch-none"
              ></canvas>
              <div class="flex justify-between items-center mt-3">
                <p class="text-xs text-dark-600 dark:text-dark-400">
                  Dessinez votre signature dans le cadre ci-dessus
                </p>
                <button
                  type="button"
                  @click="clearSignature"
                  class="text-sm text-red-600 hover:text-red-700 dark:text-red-400 font-medium"
                >
                  Effacer
                </button>
              </div>
            </div>
          </div>

          <!-- Acceptation des conditions -->
          <div class="mb-6">
            <label class="flex items-start">
              <input
                v-model="acceptTerms"
                type="checkbox"
                required
                class="mt-1 mr-3 h-5 w-5 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
              />
              <span class="text-sm text-dark-700 dark:text-dark-300">
                J'accepte les termes et conditions de ce devis. Je comprends que cette signature électronique
                a la même valeur légale qu'une signature manuscrite. *
              </span>
            </label>
          </div>

          <!-- Boutons d'action -->
          <div class="flex flex-col sm:flex-row gap-3">
            <button
              type="button"
              @click="rejectQuote"
              :disabled="submitting"
              class="flex-1 px-6 py-3 border-2 border-red-600 text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg font-semibold transition-all disabled:opacity-50"
            >
              Refuser le devis
            </button>
            <button
              type="submit"
              :disabled="submitting || !canSubmit"
              class="flex-1 px-6 py-3 bg-primary-600 hover:bg-primary-700 disabled:bg-gray-400 text-white rounded-lg font-semibold transition-colors flex items-center justify-center"
            >
              <svg v-if="!submitting" class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              <div v-else class="inline-block animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
              {{ submitting ? 'Envoi en cours...' : 'Accepter et signer' }}
            </button>
          </div>
        </form>

        <!-- Info légale -->
        <div class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-xl p-4">
          <p class="text-sm text-blue-800 dark:text-blue-200">
            <strong>Note:</strong> En signant ce devis, vous acceptez formellement les termes et le montant indiqués.
            Une copie signée vous sera envoyée par email à {{ quote.client_email }}.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getQuoteByToken, signQuote, rejectQuote as rejectQuoteAPI } from '../api/quotes'
import { useToastStore } from '../stores/toast'

const route = useRoute()
const router = useRouter()
const toastStore = useToastStore()

const quote = ref(null)
const loading = ref(true)
const error = ref(null)
const submitting = ref(false)

const signatureName = ref('')
const acceptTerms = ref(false)
const signatureCanvas = ref(null)
const isDrawing = ref(false)
const ctx = ref(null)

const canSubmit = computed(() => {
  return signatureName.value.trim() !== '' && acceptTerms.value && hasSignature.value
})

const hasSignature = ref(false)

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('fr-FR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const initCanvas = () => {
  nextTick(() => {
    if (signatureCanvas.value) {
      const canvas = signatureCanvas.value
      const rect = canvas.getBoundingClientRect()
      canvas.width = rect.width * 2
      canvas.height = rect.height * 2
      ctx.value = canvas.getContext('2d')
      ctx.value.scale(2, 2)
      ctx.value.strokeStyle = '#000000'
      ctx.value.lineWidth = 2
      ctx.value.lineCap = 'round'
      ctx.value.lineJoin = 'round'
    }
  })
}

const getMousePos = (e) => {
  const canvas = signatureCanvas.value
  const rect = canvas.getBoundingClientRect()
  const scaleX = canvas.width / rect.width
  const scaleY = canvas.height / rect.height

  if (e.touches && e.touches.length > 0) {
    return {
      x: (e.touches[0].clientX - rect.left) * scaleX / 2,
      y: (e.touches[0].clientY - rect.top) * scaleY / 2
    }
  }

  return {
    x: (e.clientX - rect.left) * scaleX / 2,
    y: (e.clientY - rect.top) * scaleY / 2
  }
}

const startDrawing = (e) => {
  isDrawing.value = true
  const pos = getMousePos(e)
  ctx.value.beginPath()
  ctx.value.moveTo(pos.x, pos.y)
  hasSignature.value = true
}

const draw = (e) => {
  if (!isDrawing.value) return
  const pos = getMousePos(e)
  ctx.value.lineTo(pos.x, pos.y)
  ctx.value.stroke()
}

const stopDrawing = () => {
  if (isDrawing.value) {
    ctx.value.closePath()
    isDrawing.value = false
  }
}

const clearSignature = () => {
  const canvas = signatureCanvas.value
  ctx.value.clearRect(0, 0, canvas.width, canvas.height)
  hasSignature.value = false
}

const submitSignature = async () => {
  if (!canSubmit.value) return

  try {
    submitting.value = true
    const signatureData = signatureCanvas.value.toDataURL('image/png')

    await signQuote(route.params.token, {
      signer_name: signatureName.value,
      signature: signatureData,
      terms_accepted: acceptTerms.value
    })

    toastStore.showToast('Devis signé avec succès !', 'success')

    // Rediriger vers une page de confirmation
    setTimeout(() => {
      router.push('/')
    }, 2000)
  } catch (err) {
    console.error('Erreur lors de la signature:', err)
    toastStore.showToast(
      err.response?.data?.error || 'Erreur lors de la signature du devis',
      'error'
    )
  } finally {
    submitting.value = false
  }
}

const rejectQuote = async () => {
  if (!confirm('Êtes-vous sûr de vouloir refuser ce devis ?')) return

  try {
    submitting.value = true
    if (!quote.value) {
      throw new Error('Quote introuvable')
    }

    await rejectQuoteAPI(quote.value.id)
    toastStore.showToast('Devis refusé', 'info')

    setTimeout(() => {
      router.push('/')
    }, 2000)
  } catch (err) {
    console.error('Erreur lors du refus:', err)
    toastStore.showToast('Erreur lors du refus du devis', 'error')
  } finally {
    submitting.value = false
  }
}

const loadQuote = async () => {
  try {
    loading.value = true
    const response = await getQuoteByToken(route.params.token)
    quote.value = response.data
    initCanvas()
  } catch (err) {
    console.error('Erreur lors du chargement du devis:', err)
    error.value = err.response?.data?.error || 'Lien invalide ou expiré'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadQuote()
})
</script>
