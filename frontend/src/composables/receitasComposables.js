import { readonly, ref } from 'vue'
import { useRoute } from 'vue-router'

export function receitasComposables()
{
    let dados = ref([]);
    let categorias = ref([]);
    let error = ref(null);

    let getDados = async()=> 
    {
        let route = useRoute();
        let url;
        if(route.query.categoria_id){
            url=`${import.meta.env.VITE_API_URL}receitas-pesquisa?categoria_id=${route.query.categoria_id}&search=${route.query.search}`
        }else{ 
            url=`${import.meta.env.VITE_API_URL}receitas`
        }
        try {
            const res = await fetch(url, {headers:{'content-type':'application/json'}});
            dados.value=await res.json();
        } catch (err) {
            error.value=err;            
        }

    };  
    getDados();

    let getCategorias = async()=> 
    {
        try {
            const res = await fetch(`${import.meta.env.VITE_API_URL}categorias`,
            {headers:{'content-type':'application/json'}});
            categorias.value=await res.json();
        } catch (err) {
            error.value=err;            
        }

    };  
    getCategorias();

    return{
        dados:readonly(dados),
        error:readonly(error),
        categorias:readonly(categorias)
    }
}