export function useContatoComposable(body)
{
    let sendData=async(body)=>{
        try{ 
            let resposta = await fetch(`${import.meta.env.VITE_API_URL}contato`, {
                method: 'POST',
                body: JSON.stringify(body),
                headers:{'content-type':"application/json"}
            })
            
            if(resposta.status==200)
            {
                alert("A sua mensagem foi enviada com sucesso");
                window.location=location.href;
            }
        } catch (error) {
            throw new Error("Erro no envio")
        }
    }

    return{
        sendData
    }
}