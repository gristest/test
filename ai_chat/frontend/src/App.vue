<template>
  <div id="app">
    <div class="app-container">
      <!-- Sidebar -->
      <div class="sidebar">
        <button class="toggle-sidebar" @click="toggleSidebar">
          {{ sidebarCollapsed ? '»' : '«' }}
        </button>
        <div v-if="!sidebarCollapsed" class="sidebar-content">
          <button class="new-chat" @click="createNewChat">+ New Chat</button>
          <div class="chat-history">
            <div v-for="chat in chats" :key="chat.id" class="chat-item">
              {{ chat.title }}
            </div>
          </div>
        </div>
      </div>

      <!-- Main Chat Area -->
      <div class="main-content">
        <div class="chat-messages">
          <div v-for="message in currentChat.messages" :key="message.id" class="message">
            {{ message.content }}
          </div>
        </div>
        <div class="input-area">
          <textarea v-model="newMessage" placeholder="Type your message..."></textarea>
          <button @click="sendMessage">Send</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      sidebarCollapsed: false,
      chats: [],
      currentChat: {
        id: null,
        messages: []
      },
      newMessage: ''
    }
  },
  methods: {
    toggleSidebar() {
      this.sidebarCollapsed = !this.sidebarCollapsed
    },
    async createNewChat() {
      try {
        const response = await this.$http.post('/chats', { title: `Chat ${this.chats.length + 1}` })
        this.chats.push(response.data)
        this.currentChat = response.data
      } catch (error) {
        console.error('Error creating chat:', error)
      }
    },
    async sendMessage() {
      if (this.newMessage.trim()) {
        try {
          await this.$http.post(`/chats/${this.currentChat.id}/messages`, {
            content: this.newMessage
          })
          this.currentChat.messages.push({
            id: Date.now(),
            content: this.newMessage
          })
          this.newMessage = ''
        } catch (error) {
          console.error('Error sending message:', error)
        }
      }
    },
    async fetchChats() {
      try {
        const response = await this.$http.get('/chats')
        this.chats = response.data
      } catch (error) {
        console.error('Error fetching chats:', error)
      }
    }
  },
  created() {
    this.fetchChats()
  }
}
</script>

<style>
/* Basic styling - will need to be enhanced */
.app-container {
  display: flex;
  height: 100vh;
}
.sidebar {
  width: 250px;
  background: #f0f0f0;
  transition: width 0.3s;
}
.sidebar.collapsed {
  width: 50px;
}
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}
.chat-messages {
  flex: 1;
  overflow-y: auto;
}
.input-area {
  padding: 10px;
}
</style>
