
<template>
  <div class="sidebar" :class="{ collapsed: isCollapsed }">
    <div class="sidebar-header">
      <button @click="newChat" class="new-chat-btn">
        <span v-if="!isCollapsed">New Chat</span>
        <span v-else>+</span>
      </button>
      <button @click="toggleSidebar" class="collapse-btn">☰</button>
    </div>
    <ul>
      <li v-for="chat in chats" :key="chat.id" :class="{ 'active-chat': String(chat.id) === router.currentRoute.value.params.id }">
        <router-link :to="`/chats/${chat.id}`" class="chat-link">{{ chat.name }}</router-link>
        <div class="chat-actions" v-if="!isCollapsed">
          <button @click="renameChat(chat)" class="action-btn">✏️</button>
          <button @click="removeChat(chat.id)" class="action-btn">🗑️</button>
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { onMounted, computed, ref } from 'vue'
import { useChatStore } from '../store'
import { useRouter } from 'vue-router'

const store = useChatStore()
const router = useRouter()

const chats = computed(() => store.chats)

onMounted(() => {
  store.fetchChats()
})

const newChat = async () => {
  const newChat = await store.createNewChat()
  router.push(`/chats/${newChat.id}`)
}

const toggleSidebar = () => {
  isCollapsed.value = !isCollapsed.value
}

const isCollapsed = ref(false)

const renameChat = async (chat) => {
  const newName = prompt("Enter new chat name:", chat.name);
  if (newName && newName.trim() !== '') {
    await store.updateChatName(chat.id, newName.trim());
  }
}

const removeChat = async (chatId) => {
  if (confirm("Are you sure you want to delete this chat?")) {
    await store.deleteChat(chatId);
    // If the current chat is deleted, navigate away
    if (router.currentRoute.value.params.id === String(chatId)) {
      router.push('/');
    }
  }
}
</script>

<style scoped>
.sidebar {
  width: 250px;
  background-color: #f0f0f0;
  padding: 20px;
  transition: width 0.3s ease;
  display: flex;
  flex-direction: column;
}

.sidebar.collapsed {
  width: 80px;
  padding: 20px 10px;
}

.sidebar.collapsed .chat-link {
  justify-content: center;
}

.sidebar.collapsed .chat-link,
.sidebar.collapsed .new-chat-btn span {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.sidebar ul {
  list-style: none;
  padding: 0;
  margin: 0;
  overflow-y: auto;
}

.sidebar li {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
  border-radius: 5px;
  padding: 5px;
}

.sidebar li:hover {
  background-color: #e0e0e0;
}

.active-chat {
  background-color: #cce5ff;
  border-left: 4px solid #007bff;
}

.active-chat .chat-link {
  font-weight: bold;
}

.chat-link {
  flex-grow: 1;
  text-decoration: none;
  color: #333;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.action-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 2px 5px;
  visibility: hidden;
}

.sidebar li:hover .action-btn {
  visibility: visible;
}
</style>
