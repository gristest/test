import { createRouter, createWebHistory } from 'vue-router'
import SimpleTest from '../views/SimpleTest.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: SimpleTest
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router