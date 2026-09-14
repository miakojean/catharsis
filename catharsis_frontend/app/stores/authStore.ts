import { defineStore } from "pinia";
import { ref } from "vue";

export interface User{
    id?:string
    username:string
    email:string
    password:string
}

export const useAuthStore = defineStore('auth', ()=>{
    
    const {$api} = useNuxtApp();

    //ui-ux
    const isLoading = ref<boolean>(false);
    const message = ref({
        successMessage:'',
        errorMessage:''
    })

    // state
    const user = ref<User>({
        id:"",
        username:"",
        email:"",
        password:""
    })

    // guetters

    // actions
    async function registration (payload:User){

        //ux
        isLoading.value = true;

        try {
            const response = await $api('/account', {
                method:"POST",
                body:payload
            })

            if (response){
                message.value.successMessage = "Votre compte a été créé avec succès!"
            } else{
                message.value.errorMessage = "Un soucis est intervenue lors de la création de votre comte"
            }
        }

        catch{
            message.value.errorMessage = "Un soucis est survenu lors de la création veuillez ressayer après"
        }

        finally{
            isLoading.value = false
        }

    }

    // return
    return {
        isLoading,
        message,
        user,
        registration
    }
})