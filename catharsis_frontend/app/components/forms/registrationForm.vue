<template>
    <form action="" class="registration-form" @submit.prevent="$emit('submit')">
        <div class="form-header">
            <h3>Inscrivez-vous</h3>
            <p>Entrer ci-dessous vos informations</p>
        </div>

        <div class="form-body">
            <BaseInput 
                label="Email" 
                placeholder="Entrer votre email"
            />
            <BaseInput 
                label="Username/entreprise" 
                placeholder="Entrer votre username"
            />
            <BaseInput 
                label="Mot de passe" 
                placeholder="Entrer votre mot de passe"
            />
            <mainButton/>
        </div>

        <p>Ou continuez avec</p>

        <div class="form-footer">
            <socialButtons/>
        </div>
    </form>
</template>

<script>
import { ref, onMounted } from 'vue';

import BaseInput from '../../components/BaseInput/BaseInput.vue'
import mainButton from '../buttons/mainButton.vue'
import socialButtons from '../buttons/socialButtons.vue';

import { registrationValidation } from '#imports';

export default {
    components:{
        BaseInput,
        mainButton,
        socialButtons
    },
    setup(){
        const form = ref({
            email: "",
            username: "",
            password: ""
        })

        onMounted(()=>{
            console.log("Bienvenu au pays mon fils")
        })

        return{
            form,
        }
    }
}
</script>

<style scoped>
.registration-form{
    
}
</style>