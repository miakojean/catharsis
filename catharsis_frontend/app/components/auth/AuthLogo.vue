<template>
  <div class="auth-logo-wrapper flex items-center justify-center">
    <CatharsisLogo variant="mark" size="lg" />
  </div>
</template>

<script setup lang="ts">
import CatharsisLogo from '~/components/brand/CatharsisLogo.vue'
</script>

<style scoped>
.auth-logo-wrapper {
  transition: transform 0.2s ease;
}
.auth-logo-wrapper:hover {
  transform: scale(1.05);
}
</style>
