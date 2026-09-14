<template>
    <form action="" class="registration-form" @submit.prevent="handleSubmit">
        <div class="form-header">
            <h3>Inscrivez-vous</h3>
            <p>Entrer ci-dessous vos informations</p>
        </div>

        <div class="form-body">
            <BaseInput 
                label="Email" 
                placeholder="Entrer votre email"
                :error-message="errorMessage.email"
            />
            <BaseInput 
                label="Username/entreprise" 
                placeholder="Entrer votre username"
                :error-message="errorMessage.username"
            />
            <BaseInput 
                label="Mot de passe" 
                placeholder="Entrer votre mot de passe"
                type="password"
                :error-message="errorMessage.password"
            />
            <mainButton/>
        </div>

        <p>Ou continuez avec</p>

        <div class="form-footer">
            <socialButtons/>
        </div>
    </form>
</template>

<script lang="ts">
import { ref, onMounted } from 'vue';
import {useAuthStore } from '~/stores/authStore.ts';
import type { User } from '~/stores/authStore.ts';
import BaseInput from '../../components/BaseInput/BaseInput.vue'
import mainButton from '../buttons/mainButton.vue'
import socialButtons from '../buttons/socialButtons.vue';


export default {
    components:{
        BaseInput,
        mainButton,
        socialButtons
    },
    setup(){

        const authStore = useAuthStore();

        const form = ref<User>({
            email: "",
            username: "",
            password: ""
        })

        const errorMessage = ref({
            email: "",
            username:"",
            password:""
        })

        // validate email

        const emailRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;

        function isFormValid (){
            
            let valid = false;

            if (form.value.email.trim()==="" || emailRegex.test(form.value.email)){
                errorMessage.value.email = "Entrer un email ou fourissez un email correct"

            }

            if (form.value.username.trim()===""){
                errorMessage.value.username = "Entrer un nom d'utilisateur";
            }

            if (form.value.password.trim()===""){
                errorMessage.value.password = "Renseignez un mot de passe";
            }

            return valid=true;
        }

        async function handleSubmit(){

            if (!isFormValid()){
                return;
            }

            await authStore.registration(form)

        }

        onMounted(()=>{
            console.log("composant monté")
        })

        return{
            form,
            errorMessage,
            isFormValid,
            handleSubmit
        }
    }
}
</script>

<style scoped>
.registration-form{
    border: 1px solid #bfbfbf;
    border-radius: 1rem;
}
</style>