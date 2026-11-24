import { createRouter, createWebHistory } from 'vue-router'
import sobreNos from '@/views/sobreNos.vue'
import Error404 from '@/views/Error404.vue'
import ReceitasDetalhes from '@/views/ReceitasDetalhes.vue'
import Receitas from '@/views/Receitas.vue'
import ReceitasPesquisar from '@/views/ReceitasPesquisar.vue'
import Contato from '@/views/Contato.vue'
import Cadastro from '@/views/Cadastro.vue'
import Login from '@/views/Login.vue'
import Painel from '@/views/Painel.vue'
import PainelEditar from '@/views/PainelEditar.vue'

import { useAuthStore } from '@/stores/authStore'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: ()=>import('@/views/Home.vue'),
      name:'home'
    },
    {
      path: '/sobre-nos',
      component: sobreNos,
      name:'sobreNos'
    },
    {
      path: '/receitas',
      component: Receitas,
      name:'receitas'
    },
    {
      path: '/receitas/pesquisar',
      component: ReceitasPesquisar,
    },
    {
      path: '/receitas/detalhes/:slug',
      component: ReceitasDetalhes,
      name:'receitasDetalhes'
    },
    {
      path: '/contato',
      component: Contato,
      name:'contato'
    },
    {
      path: '/cadastro',
      component: Cadastro,
      name:'cadastro'
    },
    {
      path: '/login',
      component: Login,
      name:'login'
    },
    {
      path: '/painel',
      component: Painel,
      name:'painel',
      meta:{
        secure:true
      }
    },
    {
      path: '/painel/editar/:id',
      component: PainelEditar,
      name:'painel_editar',
      meta:{
        secure:true
      }
    },
    {
      path: '/:pathMatch(.*)*',
      component: Error404,
    },
  ],
})

//security
router.beforeEach((to, from)=>{
  
  let store = useAuthStore();
  if(to.meta.secure){
    store.usuarioLogado();
  }
});

export default router
