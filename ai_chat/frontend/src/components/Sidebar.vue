<template>
  <div class="sidebar">
    <button @click="newChat">New Chat</button>
    <ul>
      <li v-for="chat in chats" :key="chat.id">
        <router-link :to="`/chats/${chat.id}`">{{ chat.name }}</router-link>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useChatStore } from '../store'
import { useRouter } from 'vue-router'

const store = useChatStore()
const router = useRouter()

const chats = store.chats

onMounted(() => {
  store.fetchChats()
})

const newChat = async () => {
  const newChat = await store.createNewChat()
  router.push(`/chats/${newChat.id}`)
}
</script>

<style scoped>
.sidebar {
  width: 250px;
  background-color: #f0f0f0;
  padding: 20px;
}
</style>
