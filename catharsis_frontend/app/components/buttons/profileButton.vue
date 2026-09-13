<template>
  <div class="profile-wrapper" ref="wrapperRef">
    <!-- Bouton déclencheur (initiale fixe "PR") -->
    <button class="profile-button" @click="toggleDropdown">
      <!-- 
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
            <path stroke-linecap="round" stroke-linejoin="round" d="M14.857 17.082a23.848 23.848 0 0 0 5.454-1.31A8.967 8.967 0 0 1 18 9.75V9A6 6 0 0 0 6 9v.75a8.967 8.967 0 0 1-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 0 1-5.714 0m5.714 0a3 3 0 1 1-5.714 0M3.124 7.5A8.969 8.969 0 0 1 5.292 3m13.416 0a8.969 8.969 0 0 1 2.168 4.5" />
        </svg>
      -->
        JY
    </button>

    <!-- Dropdown statique -->
    <Transition name="fade">
      <div v-if="isOpen" class="dropdown">
        <ul class="dropdown-menu">
          <li><a href="/profile">Mon profil</a></li>
          <li><a href="/settings">Paramètres</a></li>
          <li><button @click="logout">Déconnexion</button></li>
        </ul>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

// État local
const isOpen = ref(false)
const wrapperRef = ref(null)

// Fonctions
const toggleDropdown = () => {
  isOpen.value = !isOpen.value
}

const closeDropdown = () => {
  isOpen.value = false
}

// Gestion du clic en dehors
const handleClickOutside = (event) => {
  if (wrapperRef.value && !wrapperRef.value.contains(event.target)) {
    closeDropdown()
  }
}

// Déconnexion (à remplacer par ta logique)
const logout = () => {
  console.log('Déconnexion')
  // Appel API, redirection, etc.
  closeDropdown()
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
/* (les mêmes styles que précédemment) */
.profile-wrapper {
  position: relative;
  display: inline-block;
}

.profile-button {
  background-color: var(--primary-color);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  color: white;
  font-size: 0.8rem;
  font-weight: 600;
  padding: 0.8rem;
  transition: 0.4s;
}

.profile-button:hover {
  transform: translateY(-2px);
  transition: 0.2s;
}

.dropdown {
  position: absolute;
  top: calc(100% + 0.5rem);
  right: 0;
  min-width: 180px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  overflow: hidden;
  padding: 0.5rem;
}

.dropdown-menu {
  list-style: none;
  margin: 0;
  padding: 0;
}

.dropdown-menu li {
  padding: 0;
}

.dropdown-menu a,
.dropdown-menu button {
  display: block;
  width: 100%;
  padding: 10px 16px;
  text-decoration: none;
  color: #333;
  background: none;
  border: none;
  text-align: left;
  cursor: pointer;
  font-size: 0.9rem;
}

.dropdown-menu a:hover,
.dropdown-menu button:hover {
  background-color: #f5f5f5;
  border-radius: 0.5rem;
}

/* Animation */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>