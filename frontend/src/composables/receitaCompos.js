import { readonly, ref, toValue, watch } from 'vue'
import { apiUrl } from '@/services/apiUrl'

export function receitaComposable(slug) {
  const receita = ref(null)
  const erro = ref(null)
  const naoEncontrada = ref(false)
  const carregando = ref(true)
  const versao = ref(0)

  watch([() => toValue(slug), versao], async ([slugAtual], _, onCleanup) => {
    const controller = new AbortController()
    onCleanup(() => controller.abort())
    carregando.value = true
    receita.value = null
    erro.value = null
    naoEncontrada.value = false

    try {
      const resposta = await fetch(apiUrl(`receitas/slug/${encodeURIComponent(slugAtual)}`), {
        signal: controller.signal,
      })

      if (resposta.status === 404) {
        if (!controller.signal.aborted) naoEncontrada.value = true
        return
      }
      if (!resposta.ok) throw new Error(`A API retornou o status ${resposta.status}`)

      const json = await resposta.json()
      if (!json?.data) throw new Error('A API retornou uma receita inválida')
      if (!controller.signal.aborted) receita.value = json.data
    } catch (error) {
      if (!controller.signal.aborted) erro.value = error
    } finally {
      if (!controller.signal.aborted) carregando.value = false
    }
  }, { immediate: true })

  return {
    receita: readonly(receita),
    erro: readonly(erro),
    naoEncontrada: readonly(naoEncontrada),
    carregando: readonly(carregando),
    recarregar: () => versao.value++,
  }
}
