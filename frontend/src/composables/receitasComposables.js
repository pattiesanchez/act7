import { computed, readonly, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { apiUrl } from '@/services/apiUrl'

function textoDaQuery(value) {
  return (Array.isArray(value) ? value[0] : value) ?? ''
}

function normalizarBusca(texto) {
  return texto.toLocaleLowerCase('pt-BR').normalize('NFD').replace(/\p{Diacritic}/gu, '')
}

async function buscarLista(endpoint, signal) {
  const resposta = await fetch(apiUrl(endpoint), { signal })
  if (!resposta.ok) throw new Error(`A API retornou o status ${resposta.status}`)

  const json = await resposta.json()
  const items = Array.isArray(json) ? json : json?.data
  if (!Array.isArray(items)) throw new Error('A API retornou uma lista inválida')
  return items
}

export function receitasComposables() {
  const route = useRoute()
  const categoriaId = computed(() => {
    const value = textoDaQuery(route.query.categoria_id)
    return value === '0' ? '' : value
  })
  const termo = computed(() => textoDaQuery(route.query.search).trim())
  const receitas = ref([])
  const categorias = ref([])
  const carregando = ref(true)
  const carregandoCategorias = ref(true)
  const erro = ref(null)
  const erroCategorias = ref(null)
  const versaoPesquisa = ref(0)
  const versaoCategorias = ref(0)

  watch([categoriaId, termo, versaoPesquisa], async ([categoria, search], _, onCleanup) => {
    const controller = new AbortController()
    onCleanup(() => controller.abort())
    carregando.value = true
    erro.value = null

    const query = new URLSearchParams({ categoria_id: categoria, search })
    const endpoint = categoria ? `receitas-pesquisa?${query}` : 'receitas'
    try {
      const items = await buscarLista(endpoint, controller.signal)
      const termoNormalizado = normalizarBusca(search)
      if (!controller.signal.aborted) {
        receitas.value = !categoria && termoNormalizado
          ? items.filter((receita) => normalizarBusca(receita.nome).includes(termoNormalizado))
          : items
      }
    } catch (error) {
      if (!controller.signal.aborted) erro.value = error
    } finally {
      if (!controller.signal.aborted) carregando.value = false
    }
  }, { immediate: true })

  watch(versaoCategorias, async (_, __, onCleanup) => {
    const controller = new AbortController()
    onCleanup(() => controller.abort())
    carregandoCategorias.value = true
    erroCategorias.value = null

    try {
      const items = await buscarLista('categorias', controller.signal)
      if (!controller.signal.aborted) categorias.value = items
    } catch (error) {
      if (!controller.signal.aborted) erroCategorias.value = error
    } finally {
      if (!controller.signal.aborted) carregandoCategorias.value = false
    }
  }, { immediate: true })

  return {
    categoriaId,
    termo,
    receitas: readonly(receitas),
    categorias: readonly(categorias),
    erro: readonly(erro),
    erroCategorias: readonly(erroCategorias),
    carregando: readonly(carregando),
    carregandoCategorias: readonly(carregandoCategorias),
    recarregarReceitas: () => versaoPesquisa.value++,
    recarregarCategorias: () => versaoCategorias.value++,
  }
}
