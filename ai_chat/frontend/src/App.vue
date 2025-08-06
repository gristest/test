<template>
  <div id="app">
    <div class="app-container">
      <chat-sidebar
        :current-conversation="currentConversation"
        :collapsed="sidebarCollapsed"
        @new-chat="handleNewConversation"
        @toggle-sidebar="toggleSidebar"
      />
      <chat-main-content
        :conversation-id="currentConversation"
      />
    </div>
  </div>
</template>

<script>
import ChatSidebar from './components/Sidebar.vue'
import ChatMainContent from './components/MainContent.vue'
import api from '@/services/api'

export default {
  name: 'App',
  components: {
    'chat-sidebar': ChatSidebar,
    'chat-main-content': ChatMainContent
  },
  data() {
    return {
      currentConversation: null,
      sidebarCollapsed: false,
      conversations: []
    }
  },
  async created() {
    await this.loadConversations()
  },
  methods: {
    async loadConversations() {
      try {
        const { data } = await api.getConversations()
        this.conversations = data
        if (data.length && !this.currentConversation) {
          this.currentConversation = data[0].id
        }
      } catch (error) {
        console.error('Failed to load conversations:', error)
      }
    },
    async handleNewConversation() {
      try {
        const { data } = await api.createConversation()
        this.currentConversation = data.id
        await this.loadConversations()
      } catch (error) {
        console.error('Failed to create conversation:', error)
      }
    },
    toggleSidebar() {
      this.sidebarCollapsed = !this.sidebarCollapsed
    }
  }
}
</script>

<style lang="scss">
@import '@/styles/main.scss';

#app {
  display: flex;
  height: 100vh;
  overflow: hidden;

  .app-container {
    display: flex;
    width: 100%;
    height: 100%;
  }
}
</style>
