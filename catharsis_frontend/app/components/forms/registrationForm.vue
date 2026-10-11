<template>
    <form action="" class="registration-form" @submit.prevent="handleSubmit">
        <div class="form-header">
            <h3>Inscrivez-vous</h3>
            <p>Entrer ci-dessous vos informations</p>
        </div>

        <div v-if="authStore.message.successMessage" class="feedback-alert success-alert w-full flex gap-1 justify-items-start items-center" role="alert">
            <svg class="alert-icon" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
            </svg>
            <span>{{ authStore.message.successMessage }}</span>
        </div>

        <!-- Error Banner -->
        <div v-if="authStore.message.errorMessage" class="feedback-alert error-alert" role="alert">
            <svg class="alert-icon" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
            </svg>
            <span>{{ authStore.message.errorMessage }}</span>
        </div>

        <div class="form-body">
            <BaseInput 
                label="Email" 
                placeholder="Entrer votre email"
                :error-message="errorMessage.email"
                v-model="form.email"
            />
            <BaseInput 
                label="Username/entreprise" 
                placeholder="Entrer votre username"
                :error-message="errorMessage.username"
                v-model="form.username"
            />
            <BaseInput 
                label="Mot de passe" 
                placeholder="Entrer votre mot de passe"
                type="password"
                :error-message="errorMessage.password"
                v-model="form.password"
            />
            <!-- Changement de "button" à "submit" -->
            <mainButton type="submit" :is-loading="authStore.isLoading"/>
        </div>

        <p>Ou continuez avec</p>

        <div class="form-footer">
            <socialButtons/>
        </div>
    </form>
</template>

<script lang="ts">
import { ref, onMounted } from 'vue';
import { useAuthStore } from '~/stores/authStore.ts';
import type { User } from '~/stores/authStore.ts';
import BaseInput from '../../components/BaseInput/BaseInput.vue'
import mainButton from '../buttons/mainButton.vue'
import socialButtons from '../buttons/socialButtons.vue';

export default {
    components: {
        BaseInput,
        mainButton,
        socialButtons
    },

    emits: ['isDone'],
    
    setup(props, {emit}) {
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

        const emailRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;

        function isFormValid () {
            // On réinitialise les erreurs à chaque tentative
            errorMessage.value.email = "";
            errorMessage.value.username = "";
            errorMessage.value.password = "";

            let isValid = true; // On part du principe que tout est valide

            if (form.value.email.trim() === "" || !emailRegex.test(form.value.email)) {
                errorMessage.value.email = "Entrez un email ou fournissez un email correct";
                isValid = false;
            }

            if (form.value.username.trim() === "") {
                errorMessage.value.username = "Entrez un nom d'utilisateur";
                isValid = false;
            }

            if (form.value.password.trim() === "") {
                errorMessage.value.password = "Renseignez un mot de passe";
                isValid = false;
            }

            return isValid; // On retourne le vrai résultat
        }

        async function handleSubmit() {
            if (!isFormValid()) {
                return;
            }

            try {
                await authStore.registration(form.value);
                emit('isDone')
                
            } catch (error) {
                console.error("Erreur lors de l'inscription :", error);
            }
        }

        return {
            form,
            errorMessage,
            isFormValid,
            handleSubmit,
            authStore
        }
    }
}
</script>

<style scoped>
.registration-form{
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    width: 100%;
    max-width: 100%;
    padding: 0;
    align-items: stretch;
}

.success-alert {
  background-color: #f0fdf4;
  border: 1px solid #bbf7d0;
  color: #15803d;
  padding: 0.5rem;
  border-radius: 0.25rem;
}

.error-alert {
  background-color: #fef2f2;
  border: 1px solid #fecaca;
  color: #b91c1c;
}

.alert-icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}
</style>