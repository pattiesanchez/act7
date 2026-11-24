import { defineStore } from "pinia";

export const useAuthStore = defineStore('auth',
    {
        state: () => ({
            authId:(localStorage.getItem('receitas_flaites_id') !=null) ? localStorage.getItem('receitas_flaites_id'): null,
            authNome:(localStorage.getItem('receitas_flaites_nome') !=null) ? localStorage.getItem('receitas_flaites_nome'): null,
            authToken:(localStorage.getItem('receitas_flaites_token') !=null) ? localStorage.getItem('receitas_flaites_token'): null
        }),
        actions: {
            iniciarSecao(data)
            {
                localStorage.setItem('receitas_flaites_id', data.id);
                localStorage.setItem('receitas_flaites_nome', data.nome);
                localStorage.setItem('receitas_flaites_token', data.token);
            },
            encerrarSecao()
            {
                
            },
        },
    }
);
