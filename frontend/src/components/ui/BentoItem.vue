<template>
  <div 
    class="bento-item group"
    :class="[
      `col-span-${colSpan}`,
      `row-span-${rowSpan}`,
      { 'md:col-span-2': colSpan === 2, 'md:row-span-2': rowSpan === 2 }
    ]"
  >
    <div class="bento-content glass-card h-full w-full overflow-hidden rounded-2xl transition-all duration-300 hover:shadow-glow hover:-translate-y-1">
      <slot></slot>
    </div>
  </div>
</template>

<script setup>
defineProps({
  colSpan: {
    type: Number,
    default: 1,
    validator: (val) => [1, 2, 3].includes(val)
  },
  rowSpan: {
    type: Number,
    default: 1,
    validator: (val) => [1, 2].includes(val)
  }
})
</script>

<style scoped>
.bento-item {
  position: relative;
}

/* Tailwind classes for dynamic spans need to be safelisted or used explicitly */
/* We use style binding or specific classes */

.col-span-1 { grid-column: span 1 / span 1; }
.col-span-2 { grid-column: span 1 / span 1; } /* Default mobile */
.col-span-3 { grid-column: span 1 / span 1; }

.row-span-1 { grid-row: span 1 / span 1; }
.row-span-2 { grid-row: span 1 / span 1; }

@media (min-width: 768px) {
  .md\:col-span-2 { grid-column: span 2 / span 2; }
  .md\:row-span-2 { grid-row: span 2 / span 2; }
}

.glass-card {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.dark .glass-card {
  background: rgba(30, 41, 59, 0.7);
  border-color: rgba(255, 255, 255, 0.1);
}
</style>
