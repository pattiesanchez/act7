import axios from 'axios'
import { apiUrl } from '@/services/apiUrl'
import { useAuthStore } from '@/stores/authStore'

export function cadastroComposable() {
  function sendData(body) {
    return axios.post(apiUrl('seguranca/registro'), body, {
      headers: { 'content-type': 'application/json' },
    })
  }

  return { sendData }
}

export function loginComposable() {
  const store = useAuthStore()

  async function sendData(body) {
    const response = await axios.post(apiUrl('seguranca/login'), body, {
      headers: { 'content-type': 'application/json' },
    })
    store.iniciarSecao(response.data)
  }

  return { sendData }
}
