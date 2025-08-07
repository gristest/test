<template>
  <div class="sidebar">
    <button @click="toggleSidebar">Toggle Sidebar</button>
    <ul v-if="isVisible">
      <li v-for="chat in chats" :key="chat.id" @click="selectChat(chat.id)">
        {{ chat.name }}
      </li>
      <li @click="createNewChat">+ New Chat</li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isVisible: true,
      chats: []
    };
  },
  methods: {
    async fetchChats() {
      try {
        const response = await axios.get('/api/chats/');
        this.chats = response.data;
      } catch (error) {
        console.error('Error fetching chats:', error);
      }
    },
    async createNewChat() {
      try {
        const response = await axios.post('/api/chats/', { name: 'New Chat' });
        this.chats.push(response.data);
      } catch (error) {
        console.error('Error creating new chat:', error);
      }
    },
    toggleSidebar() {
      this.isVisible = !this.isVisible;
    },
    selectChat(chatId) {
      // Logic to select a chat
    },
    createNewChat() {
      // Logic to create a new chat
    }
  }
};
</script>

<style scoped>
.sidebar {
  width: 250px;
  background-color: #f4f4f4;
  padding: 10px;
}
</style>
