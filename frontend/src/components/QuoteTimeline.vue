<template>
  <div class="relative">
    <!-- Timeline verticale -->
    <div class="absolute left-4 top-0 bottom-0 w-0.5 bg-gray-200 dark:bg-dark-600"></div>

    <div class="space-y-6">
      <!-- Événement: Création -->
      <div class="relative flex items-start gap-4">
        <div class="flex-shrink-0 w-8 h-8 rounded-full bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center z-10 border-2 border-white dark:border-dark-800">
          <svg class="w-4 h-4 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
          </svg>
        </div>
        <div class="flex-1 bg-gray-50 dark:bg-dark-700 rounded-lg p-3">
          <div class="flex items-center justify-between mb-1">
            <p class="font-semibold text-dark-800 dark:text-dark-100">Devis créé</p>
            <span class="text-xs text-dark-500 dark:text-dark-400">{{ formatDate(quote.created_at) }}</span>
          </div>
          <p class="text-sm text-dark-600 dark:text-dark-300">Le devis a été créé et sauvegardé</p>
        </div>
      </div>

      <!-- Événement: Envoi -->
      <div v-if="quote.sent_at" class="relative flex items-start gap-4">
        <div class="flex-shrink-0 w-8 h-8 rounded-full bg-purple-100 dark:bg-purple-900/30 flex items-center justify-center z-10 border-2 border-white dark:border-dark-800">
          <svg class="w-4 h-4 text-purple-600 dark:text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
          </svg>
        </div>
        <div class="flex-1 bg-gray-50 dark:bg-dark-700 rounded-lg p-3">
          <div class="flex items-center justify-between mb-1">
            <p class="font-semibold text-dark-800 dark:text-dark-100">Devis envoyé</p>
            <span class="text-xs text-dark-500 dark:text-dark-400">{{ formatDate(quote.sent_at) }}</span>
          </div>
          <p class="text-sm text-dark-600 dark:text-dark-300">Le devis a été envoyé par email au client</p>
        </div>
      </div>

      <!-- Événement: Consultation -->
      <div v-if="quote.viewed_at" class="relative flex items-start gap-4">
        <div class="flex-shrink-0 w-8 h-8 rounded-full bg-indigo-100 dark:bg-indigo-900/30 flex items-center justify-center z-10 border-2 border-white dark:border-dark-800">
          <svg class="w-4 h-4 text-indigo-600 dark:text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
          </svg>
        </div>
        <div class="flex-1 bg-gray-50 dark:bg-dark-700 rounded-lg p-3">
          <div class="flex items-center justify-between mb-1">
            <p class="font-semibold text-dark-800 dark:text-dark-100">Devis consulté</p>
            <span class="text-xs text-dark-500 dark:text-dark-400">{{ formatDate(quote.viewed_at) }}</span>
          </div>
          <p class="text-sm text-dark-600 dark:text-dark-300">Le client a ouvert le devis</p>
        </div>
      </div>

      <!-- Événement: Signature -->
      <div v-if="quote.signed_at" class="relative flex items-start gap-4">
        <div class="flex-shrink-0 w-8 h-8 rounded-full bg-green-100 dark:bg-green-900/30 flex items-center justify-center z-10 border-2 border-white dark:border-dark-800">
          <svg class="w-4 h-4 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
        </div>
        <div class="flex-1 bg-gray-50 dark:bg-dark-700 rounded-lg p-3">
          <div class="flex items-center justify-between mb-1">
            <p class="font-semibold text-dark-800 dark:text-dark-100">Devis signé</p>
            <span class="text-xs text-dark-500 dark:text-dark-400">{{ formatDate(quote.signed_at) }}</span>
          </div>
          <p class="text-sm text-dark-600 dark:text-dark-300">Le client a signé électroniquement le devis</p>
          <div v-if="quote.signer_name" class="mt-2 text-xs text-dark-500 dark:text-dark-400">
            Signé par: {{ quote.signer_name }}
          </div>
        </div>
      </div>

      <!-- Événement: Acceptation -->
      <div v-if="quote.status === 'accepted' && !quote.signed_at" class="relative flex items-start gap-4">
        <div class="flex-shrink-0 w-8 h-8 rounded-full bg-green-100 dark:bg-green-900/30 flex items-center justify-center z-10 border-2 border-white dark:border-dark-800">
          <svg class="w-4 h-4 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
          </svg>
        </div>
        <div class="flex-1 bg-gray-50 dark:bg-dark-700 rounded-lg p-3">
          <div class="flex items-center justify-between mb-1">
            <p class="font-semibold text-dark-800 dark:text-dark-100">Devis accepté</p>
            <span class="text-xs text-dark-500 dark:text-dark-400">{{ formatDate(quote.updated_at) }}</span>
          </div>
          <p class="text-sm text-dark-600 dark:text-dark-300">Le devis a été accepté</p>
        </div>
      </div>

      <!-- Événement: Refus -->
      <div v-if="quote.status === 'rejected'" class="relative flex items-start gap-4">
        <div class="flex-shrink-0 w-8 h-8 rounded-full bg-red-100 dark:bg-red-900/30 flex items-center justify-center z-10 border-2 border-white dark:border-dark-800">
          <svg class="w-4 h-4 text-red-600 dark:text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </div>
        <div class="flex-1 bg-gray-50 dark:bg-dark-700 rounded-lg p-3">
          <div class="flex items-center justify-between mb-1">
            <p class="font-semibold text-dark-800 dark:text-dark-100">Devis refusé</p>
            <span class="text-xs text-dark-500 dark:text-dark-400">{{ formatDate(quote.updated_at) }}</span>
          </div>
          <p class="text-sm text-dark-600 dark:text-dark-300">Le devis a été refusé</p>
        </div>
      </div>

      <!-- Événement: Expiration -->
      <div v-if="quote.status === 'expired'" class="relative flex items-start gap-4">
        <div class="flex-shrink-0 w-8 h-8 rounded-full bg-amber-100 dark:bg-amber-900/30 flex items-center justify-center z-10 border-2 border-white dark:border-dark-800">
          <svg class="w-4 h-4 text-amber-600 dark:text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
        </div>
        <div class="flex-1 bg-gray-50 dark:bg-dark-700 rounded-lg p-3">
          <div class="flex items-center justify-between mb-1">
            <p class="font-semibold text-dark-800 dark:text-dark-100">Devis expiré</p>
            <span class="text-xs text-dark-500 dark:text-dark-400">{{ formatDate(quote.expiry_date) }}</span>
          </div>
          <p class="text-sm text-dark-600 dark:text-dark-300">La date de validité du devis est dépassée</p>
        </div>
      </div>

      <!-- Prochaine étape suggérée -->
      <div v-if="getNextAction()" class="relative flex items-start gap-4 opacity-50">
        <div class="flex-shrink-0 w-8 h-8 rounded-full bg-gray-200 dark:bg-dark-600 flex items-center justify-center z-10 border-2 border-white dark:border-dark-800 border-dashed">
          <svg class="w-4 h-4 text-gray-400 dark:text-dark-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
          </svg>
        </div>
        <div class="flex-1 bg-gray-50 dark:bg-dark-700 rounded-lg p-3 border-2 border-dashed border-gray-300 dark:border-dark-600">
          <p class="font-semibold text-dark-600 dark:text-dark-300">Prochaine étape</p>
          <p class="text-sm text-dark-500 dark:text-dark-400 mt-1">{{ getNextAction() }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'

const props = defineProps({
  quote: {
    type: Object,
    required: true
  }
})

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  const date = new Date(dateString)
  return date.toLocaleDateString('fr-FR', {
    day: '2-digit',
    month: 'long',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getNextAction = () => {
  const quote = props.quote

  if (quote.status === 'draft') {
    return 'Envoyer le devis au client par email'
  } else if (quote.status === 'sent' && !quote.viewed_at) {
    return 'En attente de consultation par le client'
  } else if (quote.status === 'viewed' && !quote.signed_at) {
    return 'En attente de signature du client'
  } else if (quote.status === 'accepted' || quote.signed_at) {
    return 'Projet accepté - Préparer le contrat et commencer le développement'
  }

  return null
}
</script>
