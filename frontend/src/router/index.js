import { createRouter, createWebHistory } from 'vue-router'
import ColisListView from '../views/ColisListView.vue'
import ColisCreateView from '../views/ColisCreateView.vue'
import ColisDetailView from '../views/ColisDetailView.vue'
import RoutePlannerView from '../views/RoutePlannerView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', redirect: '/colis' },
    { path: '/colis', name: 'colis-list', component: ColisListView },
    { path: '/colis/nouveau', name: 'colis-create', component: ColisCreateView },
    { path: '/colis/:id', name: 'colis-detail', component: ColisDetailView, props: true },
    { path: '/route-planner', name: 'route-planner', component: RoutePlannerView },
  ],
})

export default router
