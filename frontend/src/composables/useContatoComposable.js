import { apiUrl } from '@/services/apiUrl'

export function useContatoComposable() {
  async function sendData(body) {
    const resposta = await fetch(apiUrl('contato'), {
      method: 'POST',
      body: JSON.stringify(body),
      headers: { 'content-type': 'application/json' },
    })

    if (!resposta.ok) {
      throw new Error('Não foi possível enviar sua mensagem.')
    }
  }

  return { sendData }
}
