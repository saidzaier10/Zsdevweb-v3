<template>
  <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
    <!-- Graphique: Évolution des devis -->
    <div class="bg-white dark:bg-dark-800 rounded-xl shadow-sm p-6 border border-gray-200 dark:border-dark-700">
      <h3 class="text-lg font-semibold text-dark-800 dark:text-dark-100 mb-4">
        Évolution des devis (30 derniers jours)
      </h3>
      <div class="h-64">
        <Line :data="lineChartData" :options="lineChartOptions" />
      </div>
    </div>

    <!-- Graphique: Répartition par statut -->
    <div class="bg-white dark:bg-dark-800 rounded-xl shadow-sm p-6 border border-gray-200 dark:border-dark-700">
      <h3 class="text-lg font-semibold text-dark-800 dark:text-dark-100 mb-4">
        Répartition par statut
      </h3>
      <div class="h-64">
        <Doughnut :data="doughnutChartData" :options="doughnutChartOptions" />
      </div>
    </div>

    <!-- Graphique: Top 5 types de projets -->
    <div class="bg-white dark:bg-dark-800 rounded-xl shadow-sm p-6 border border-gray-200 dark:border-dark-700">
      <h3 class="text-lg font-semibold text-dark-800 dark:text-dark-100 mb-4">
        Top 5 types de projets
      </h3>
      <div class="h-64">
        <Bar :data="barChartData" :options="barChartOptions" />
      </div>
    </div>

    <!-- Graphique: CA prévisionnel vs réalisé -->
    <div class="bg-white dark:bg-dark-800 rounded-xl shadow-sm p-6 border border-gray-200 dark:border-dark-700">
      <h3 class="text-lg font-semibold text-dark-800 dark:text-dark-100 mb-4">
        Chiffre d'affaires (€)
      </h3>
      <div class="h-64">
        <Bar :data="revenueChartData" :options="revenueChartOptions" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'
import { Line, Bar, Doughnut } from 'vue-chartjs'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler
)

const props = defineProps({
  quotes: {
    type: Array,
    required: true
  }
})

// Configuration commune des couleurs
const isDark = document.documentElement.classList.contains('dark')
const textColor = isDark ? '#e5e7eb' : '#1f2937'
const gridColor = isDark ? '#374151' : '#e5e7eb'

// Données pour le graphique d'évolution (ligne)
const lineChartData = computed(() => {
  const last30Days = Array.from({ length: 30 }, (_, i) => {
    const date = new Date()
    date.setDate(date.getDate() - (29 - i))
    return date.toISOString().split('T')[0]
  })

  const quotesPerDay = last30Days.map(day => {
    return props.quotes.filter(q => {
      const quoteDate = new Date(q.created_at).toISOString().split('T')[0]
      return quoteDate === day
    }).length
  })

  return {
    labels: last30Days.map(date => {
      const d = new Date(date)
      return d.toLocaleDateString('fr-FR', { day: '2-digit', month: '2-digit' })
    }),
    datasets: [
      {
        label: 'Devis créés',
        data: quotesPerDay,
        borderColor: '#3b82f6',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        fill: true,
        tension: 0.4
      }
    ]
  }
})

const lineChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false
    },
    tooltip: {
      mode: 'index',
      intersect: false
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      ticks: {
        color: textColor,
        stepSize: 1
      },
      grid: {
        color: gridColor
      }
    },
    x: {
      ticks: {
        color: textColor,
        maxRotation: 45,
        minRotation: 45
      },
      grid: {
        color: gridColor
      }
    }
  }
}

// Données pour le graphique en donut (statuts)
const doughnutChartData = computed(() => {
  const statusCounts = {
    draft: props.quotes.filter(q => q.status === 'draft').length,
    sent: props.quotes.filter(q => q.status === 'sent').length,
    viewed: props.quotes.filter(q => q.status === 'viewed').length,
    accepted: props.quotes.filter(q => q.status === 'accepted').length,
    rejected: props.quotes.filter(q => q.status === 'rejected').length,
    expired: props.quotes.filter(q => q.status === 'expired').length
  }

  return {
    labels: ['Brouillons', 'Envoyés', 'Consultés', 'Acceptés', 'Refusés', 'Expirés'],
    datasets: [
      {
        data: Object.values(statusCounts),
        backgroundColor: [
          '#6b7280', // gray
          '#3b82f6', // blue
          '#8b5cf6', // indigo
          '#10b981', // green
          '#ef4444', // red
          '#f59e0b'  // amber
        ],
        borderWidth: 2,
        borderColor: isDark ? '#1f2937' : '#ffffff'
      }
    ]
  }
})

const doughnutChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom',
      labels: {
        color: textColor,
        padding: 15,
        font: {
          size: 12
        }
      }
    },
    tooltip: {
      callbacks: {
        label: function(context) {
          const label = context.label || ''
          const value = context.parsed
          const total = context.dataset.data.reduce((a, b) => a + b, 0)
          const percentage = ((value / total) * 100).toFixed(1)
          return `${label}: ${value} (${percentage}%)`
        }
      }
    }
  }
}

// Données pour le graphique en barres (types de projets)
const barChartData = computed(() => {
  const projectTypeCounts = {}

  props.quotes.forEach(quote => {
    const projectType = quote.project_type?.name || 'Non défini'
    projectTypeCounts[projectType] = (projectTypeCounts[projectType] || 0) + 1
  })

  const sortedTypes = Object.entries(projectTypeCounts)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5)

  return {
    labels: sortedTypes.map(([name]) => name),
    datasets: [
      {
        label: 'Nombre de devis',
        data: sortedTypes.map(([, count]) => count),
        backgroundColor: '#8b5cf6',
        borderColor: '#7c3aed',
        borderWidth: 1
      }
    ]
  }
})

const barChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      ticks: {
        color: textColor,
        stepSize: 1
      },
      grid: {
        color: gridColor
      }
    },
    x: {
      ticks: {
        color: textColor
      },
      grid: {
        display: false
      }
    }
  }
}

// Données pour le graphique CA
const revenueChartData = computed(() => {
  const accepted = props.quotes
    .filter(q => q.status === 'accepted')
    .reduce((sum, q) => sum + parseFloat(q.total_price || 0), 0)

  const pending = props.quotes
    .filter(q => ['sent', 'viewed'].includes(q.status))
    .reduce((sum, q) => sum + parseFloat(q.total_price || 0), 0)

  const draft = props.quotes
    .filter(q => q.status === 'draft')
    .reduce((sum, q) => sum + parseFloat(q.total_price || 0), 0)

  return {
    labels: ['Réalisé', 'En attente', 'Brouillon'],
    datasets: [
      {
        label: 'Montant (€)',
        data: [accepted, pending, draft],
        backgroundColor: ['#10b981', '#f59e0b', '#6b7280'],
        borderWidth: 1
      }
    ]
  }
})

const revenueChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false
    },
    tooltip: {
      callbacks: {
        label: function(context) {
          return `${context.label}: ${context.parsed.y.toFixed(2)} €`
        }
      }
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      ticks: {
        color: textColor,
        callback: function(value) {
          return value.toLocaleString('fr-FR') + ' €'
        }
      },
      grid: {
        color: gridColor
      }
    },
    x: {
      ticks: {
        color: textColor
      },
      grid: {
        display: false
      }
    }
  }
}
</script>
