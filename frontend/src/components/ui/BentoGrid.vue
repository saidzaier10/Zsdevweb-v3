<template>
  <div class="bento-grid">
    <slot></slot>
  </div>
</template>

<style scoped>
.bento-grid {
  display: grid;
  grid-template-columns: repeat(1, 1fr);
  gap: 1.5rem;
  width: 100%;
}

@media (min-width: 768px) {
  .bento-grid {
    grid-template-columns: repeat(2, 1fr);
    grid-auto-rows: minmax(250px, auto);
  }
}

@media (min-width: 1024px) {
  .bento-grid {
    grid-template-columns: repeat(3, 1fr);
    grid-template-rows: repeat(auto-fill, minmax(280px, auto));
  }
}
</style>
