<template>
    <button class="main-button">
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

.main-button{
    padding: 0.8rem;
    width: 100%;
    max-width: 400px;
    border-radius: 1.5rem;
    border: none;
    background: var(--my-black);
    color: #fff;
    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
    transition: 0.2s ease-in-out;
}

.main-button:hover{
    background: var(--black-forest);
    color: #fff;
    transition: 0.1s ease-in;
    border: none;
    transform: translateY(-2px);
}

</style>
