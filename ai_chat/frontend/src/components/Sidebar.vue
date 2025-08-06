
<template>
  <aside class="sidebar">
    <div class="sidebar-header">
      <button class="toggle-button" @click="toggleSidebar">
        ☰
      </button>
    </div>
    <div class="conversation-list">
      <div class="new-chat-button">
        <button @click="createNewChat">+ New Chat</button>
      </div>
      <div class="conversation-items">
        <!-- Conversation history will be rendered here -->
      </div>
    </div>
  </aside>
</template>

<script>
import api from '@/services/api'

export default {
  name: 'ChatSidebar',
  data() {
    return {
      conversations: [],
      loading: false
    }
  },
  methods: {
    toggleSidebar() {
      this.$emit('toggle-sidebar')
    },
    async createNewChat() {
      try {
        this.loading = true
        const response = await api.createConversation()
        this.$emit('new-chat', response.data.id)
        this.fetchConversations()
      } catch (error) {
        console.error('Error creating conversation:', error)
      } finally {
        this.loading = false
      }
    },
    async fetchConversations() {
      try {
        const response = await api.getConversations()
        this.conversations = response.data
      } catch (error) {
        console.error('Error fetching conversations:', error)
      }
    }
  },
  created() {
    this.fetchConversations()
  }
}
</script>

<style lang="scss" scoped>
@import '@/styles/variables.scss';

.sidebar {
  width: 260px;
  height: 100%;
  background: $sidebar-bg;
  transition: width 0.3s ease;
  
  &.collapsed {
    width: 60px;
  }
}

.sidebar-header {
  padding: 12px;
  border-bottom: 1px solid $border-color;
}

.conversation-list {
  padding: 8px;
}

.new-chat-button {
  margin-bottom: 12px;
}
</style>
