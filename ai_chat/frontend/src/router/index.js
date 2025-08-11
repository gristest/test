import { createRouter, createWebHistory } from 'vue-router'
// Removed unused import
import ChatView from '../views/ChatView.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: ChatView,
    meta: { requiresAuth: false }
  },
  {
    path: '/chat',
    name: 'Chat',
    component: ChatView,
    meta: { requiresAuth: false }
  },
  {
    path: '/chat/:id',
    name: 'Conversation',
    component: ChatView,
    props: true,
    meta: { requiresAuth: false }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router