<template>
  <div class="auth-logo-wrapper flex items-center justify-center">
    <svg 
      class="auth-logo-svg" 
      width="24" 
      height="28" 
      viewBox="0 0 24 28" 
      fill="none" 
      xmlns="http://www.w3.org/2000/svg"
      aria-label="Logo"
    >
      <!-- Top shard facet -->
      <polygon points="11,2 4.5,13.5 11.5,13.5" fill="currentColor" />
      <!-- Bottom shard facet -->
      <polygon points="14,14.5 20,14.5 14.5,26" fill="currentColor" />
    </svg>
  </div>
</template>

<script setup lang="ts">
// Minimalist geometric lightning mark matching the reference design without logo text
</script>

<style scoped>
.auth-logo-wrapper {
  color: #111111;
  transition: transform 0.2s ease;
}
.auth-logo-wrapper:hover {
  transform: scale(1.06);
}
.auth-logo-svg {
  display: block;
}
</style>
