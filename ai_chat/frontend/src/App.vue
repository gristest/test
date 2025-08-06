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

export default {
  name: 'App',
  components: {
    'chat-sidebar': ChatSidebar,
    'chat-main-content': ChatMainContent
  },
  data() {
    return {
      currentConversation: null,
      sidebarCollapsed: false
    }
  },
  methods: {
    handleNewConversation(convId) {
      this.currentConversation = convId
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
