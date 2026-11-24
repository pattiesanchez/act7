export async function getDadosHome()
{
    let resposta = await fetch(`${import.meta.env.VITE_API_URL}receitas-home`,
        {headers:{'content-type':'application/json'}});
    const resultado = await resposta.json();
    
    return resultado; 
}