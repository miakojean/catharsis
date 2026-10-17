<template>
    <div class="empty-state w-full flex flex-col justify-center items-center gap-4">
        <!-- Wrapper ajouté pour l'animation flottante de l'icône -->
        <div class="icon-wrapper">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-12">
                <path stroke-linecap="round" stroke-linejoin="round" d="m20.25 7.5-.625 10.632a2.25 2.25 0 0 1-2.247 2.118H6.622a2.25 2.25 0 0 1-2.247-2.118L3.75 7.5m6 4.125 2.25 2.25m0 0 2.25 2.25M12 13.875l2.25-2.25M12 13.875l-2.25 2.25M3.375 7.5h17.25c.621 0 1.125-.504 1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125Z" />
            </svg>
        </div>
        <h4>{{ title }}</h4>
        <p>{{ description }}</p>
        <div class="button-wrapper">
            <mainButton :label="actionText" @click="$emit('action')" />
        </div>
  </div>
</template>

<script>
import mainButton from '../buttons/mainButton.vue';

export default {
    components: {
        mainButton
    },
    props: {
        title: {
            type: String,
            default: 'Aucun site enregistré'
        },
        description: {
            type: String,
            default: 'Vos sites enregistrés apparaîtront ici'
        },
        actionText: {
            type: String,
            default: 'Enregistrer un site'
        }
    },
    emits: ['action']
}
</script>

<style scoped>
.empty-state {
    min-height: 360px;
    height: calc(100vh - 170px);
    position: relative;
    overflow: hidden;
    
    /* Motif de fond : Grille de points */
    background-color: #fafafa;
    background-image: radial-gradient(#d1d5db 1.5px, transparent 1.5px);
    background-size: 32px 32px;
    
    /* Animation du motif en arrière-plan */
    animation: panBackground 20s linear infinite;
}

/* Défilement continu et fluide du motif */
@keyframes panBackground {
    0% { background-position: 0 0; }
    100% { background-position: 32px 32px; }
}

/* Effet flottant (lévitation) pour l'icône */
.icon-wrapper {
    animation: float 4s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}

.empty-state svg {
    color: #0f0f0f;
}

.empty-state h4 {
    font-size: 24px;
    font-weight: 600;
    margin-top: 0.5rem;
}

.empty-state p {
    font-size: 16px;
    color: #666;
}

.button-wrapper {
    max-width: 500px;
    padding: 1rem;
    /* Apparition en fondu du bouton au chargement */
    animation: fadeIn 0.8s ease-out forwards;
}

@keyframes fadeIn {
    from { 
        opacity: 0; 
        transform: translateY(10px); 
    }
    to { 
        opacity: 1; 
        transform: translateY(0); 
    }
}
</style>