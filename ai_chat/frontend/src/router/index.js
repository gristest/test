import { createRouter, createWebHistory } from 'vue-router'
import SimpleTest from '../views/SimpleTest.vue'
import ChatView from '../views/ChatView.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: ChatView
  },
  {
    path: '/test',
    name: 'test',
    component: SimpleTest
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router