import { readonly, ref } from 'vue'

export function receitaComposable(slug)
{
    let dado = ref([]);
    let error = ref(null);

    let getDados = async()=>
    {
        try {
            const res = await fetch(`${import.meta.env.VITE_API_URL}receitas/slug/${slug}`,
            {headers:{'content-type':'application/json'}});
            if(res.status==404){
                window.location="/error";
            }
            dado.value=await res.json();
        } catch (err) {
            error.value=err;            
        }
    };  
    getDados();

    return{
        dado:readonly(dado),
        error:readonly(error),
    }
}