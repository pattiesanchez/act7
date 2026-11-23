import { createRouter, createWebHistory } from 'vue-router'
import SobreNos from '@/views/SobreNos.vue'
import Error404 from '@/views/Error404.vue'

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
      component: SobreNos,
      name:'sobreNos'
    },
    {
      path: '/:pathMatch(.*)*',
      component: Error404,
    },
  ],
})

export default router
