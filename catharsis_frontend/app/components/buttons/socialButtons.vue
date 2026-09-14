<template>
    <button class="social-button">
        <span v-if="!isLoading">
            {{ label }}
        </span>
        <span class="loading loading-spinner loading-md" v-else></span>
    </button>
</template>

<script>
export default {

    props:{
        isLoading:{
            type:Boolean,
            default: false
        },
        label: {
            type: String,
            default:'Commencer'
        }
    }

}
</script>

<style scoped>

.social-button{
    padding: 0.8rem;
    width: 100%;
    max-width: 400px;
    border-radius: 1.5rem;
    border: none;
    background: none;
    color: var(--green);
    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
    transition: 0.3s ease-in-out;
    border: 1px solid #9a9a9a
}

.social-button:hover{
    color: var(--green);
    transition: 0.2s ease-in;
    border: none;
    transform: translateY(-2px);
    border: 1px solid #9a9a9a
}

</style>
