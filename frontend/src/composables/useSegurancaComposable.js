import { useAuthStore } from '@/stores/authStore';
import axios from 'axios'

export function cadastroComposable(body)
{ 
    let sendData = async(body)=>
    {  
        axios.post(
            `${import.meta.env.VITE_API_URL}seguranca/registro`, 
            body, 
            {headers:{'content-type':'application/json'}})
            .then((response) => {
                alert('Cadastrado com sucesso!\n Enviamos um email para ativação de usuário');
                window.location=location.href;
            })
            .catch(() => {
                alert('Ocorreu um erro inesperado');
                window.location=location.href;
            });
    };
    return {sendData};
}

export function loginComposable(body)
{ 
    let sendData = async(body)=>
    {  
        try{
            axios.post(
                `${import.meta.env.VITE_API_URL}seguranca/login`, 
                body, 
                {headers:{'content-type':'application/json'}})
                .then((response) => {
                    let store = useAuthStore();
                    store.iniciarSecao(response.data);
                    window.location="/painel";
                })
                .catch(() => {
                    alert('Ocorreu um erro inesperado');
                    window.location=location.href;
                });
        } catch (error) { 
            alert('Ocorreu um erro inesperado');
            window.location=location.href;
        }
    };
    return {sendData};
}