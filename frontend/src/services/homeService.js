import { apiUrl } from '@/services/apiUrl'

export async function getDadosHome() {
  const response = await fetch(apiUrl('receitas-home'))
  if (!response.ok) throw new Error('Não foi possível carregar os destaques.')

  const { data } = await response.json()
  if (!Array.isArray(data)) throw new Error('A resposta de receitas é inválida.')

  return data
}
