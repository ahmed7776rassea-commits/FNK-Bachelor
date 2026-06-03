import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from '../views/LoginPage.vue'

import HinweisePag from '@/views/HinweisePag.vue'
import FunktionenPage from '@/views/FunktionenPage.vue'
import AntragEinsPage from '@/views/AntragEinsPage.vue'
import Antrag2aundbPag from '@/views/Antrag2aundbPag.vue'
import Antrag2a from '@/views/Antrag2a.vue'
import Antrag2bPag from '@/views/Antrag2bPag.vue'
import Antraga3ab from '@/views/Antraga3ab.vue'
import Antrag3a from '@/views/Antrag3a.vue'
import Antrag3b from '@/views/Antrag3b.vue'
import DankePage from '@/views/DankePage.vue'
import HomePage from '@/views/HomePage.vue'
import FnkView from '@/views/FnkAntraege.vue'
import FnkDetail from '@/views/FnkAntragDetail.vue'
import VerlaufList from '@/views/VerlaufList.vue'




const routes = [
{ path: '/', component: LoginPage },
  { path: '/login', component: LoginPage },

  {path:'/hinweise',component:HinweisePag},
  {path:'/funktionen',component:FunktionenPage},
  {path:'/antrag1',component:AntragEinsPage},
  {path:'/antrag2ab',component:Antrag2aundbPag},
  {path:'/antrag2a',component:Antrag2a},
  {path:'/antrag2b',component:Antrag2bPag},
  {path:'/antraga3ab',component:Antraga3ab},
  {path:'/antrag3a',component:Antrag3a},
  {path:'/antrag3b',component:Antrag3b},
  {path:'/danke',component:DankePage},
  { path: '/fnk', component: FnkView },
  { path: '/fnk/antrag/:id', name: 'FnkDetail', component: FnkDetail },
  { path: '/home', component: HomePage },
  { path: '/verlauf/:id', name: 'VerlaufDetail', component: VerlaufList }
  

]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
