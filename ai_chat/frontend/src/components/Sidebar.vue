<template>
  <div class="sidebar" :class="{ collapsed: isCollapsed }">
    <!-- 侧边栏头部 -->
    <div class="sidebar-header">
      <button class="collapse-btn" @click="toggleSidebar">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M3 12h18m-9-9l9 9-9 9"/>
        </svg>
      </button>
      <button v-if="!isCollapsed" class="new-chat-btn" @click="createNewChat">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M12 5v14m-7-7h14"/>
        </svg>
        新对话
      </button>
    </div>

    <!-- 对话历史列表 -->
    <div v-if="!isCollapsed" class="conversations-list">
      <div class="section-title">对话历史</div>
      <div 
        v-for="conversation in conversations" 
        :key="conversation.id"
        class="conversation-item"
        :class="{ active: currentConversationId === conversation.id }"
        @click="selectConversation(conversation.id)"
      >
        <div class="conversation-title" v-if="!conversation.editing">
          {{ conversation.title }}
        </div>
        <input 
          v-else
          v-model="conversation.editTitle"
          class="conversation-title-input"
          @blur="saveTitle(conversation)"
          @keyup.enter="saveTitle(conversation)"
          @keyup.esc="cancelEdit(conversation)"
          ref="titleInput"
        />
        <div class="menu-container" v-if="!conversation.editing">
          <button 
            class="menu-btn"
            @click.stop="toggleMenu(conversation.id)"
          >
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="6" r="1"/>
              <circle cx="12" cy="12" r="1"/>
              <circle cx="12" cy="18" r="1"/>
            </svg>
          </button>
          <div v-if="activeMenu === conversation.id" class="dropdown-menu">
            <div class="menu-item" @click.stop="startEdit(conversation)">Modify Title</div>
            <div class="menu-item" @click.stop="deleteConversation(conversation.id)">Delete</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Sidebar',
  props: {
    conversations: {
      type: Array,
      default: () => []
    },
    currentConversationId: {
      type: Number,
      default: null
    }
  },
  data() {
    return {
      isCollapsed: false,
      activeMenu: null
    }
  },
  methods: {
    toggleSidebar() {
      this.isCollapsed = !this.isCollapsed
    },
    createNewChat() {
      this.$emit('create-new-chat')
    },
    selectConversation(conversationId) {
      this.$emit('select-conversation', conversationId)
    },
    startEdit(conversation) {
      conversation.editing = true
      conversation.editTitle = conversation.title
      this.activeMenu = null
      this.$nextTick(() => {
        const input = this.$refs.titleInput?.[0]
        if (input) {
          input.focus()
          input.select()
        }
      })
    },
    saveTitle(conversation) {
      if (conversation.editTitle && conversation.editTitle.trim() !== conversation.title) {
        this.$emit('update-conversation-title', conversation.id, conversation.editTitle.trim())
      }
      conversation.editing = false
    },
    cancelEdit(conversation) {
      conversation.editing = false
      conversation.editTitle = conversation.title
    },
    toggleMenu(conversationId) {
      this.activeMenu = this.activeMenu === conversationId ? null : conversationId
    },
    deleteConversation(conversationId) {
      this.$emit('delete-conversation', conversationId)
      this.activeMenu = null
    }
  }
}
</script>

<style scoped>
.sidebar {
  width: 260px;
  height: 100vh;
  background-color: #171717;
  color: white;
  display: flex;
  flex-direction: column;
  transition: width 0.3s ease;
  border-right: 1px solid #2d2d2d;
}

.sidebar.collapsed {
  width: 60px;
}

.sidebar-header {
  padding: 16px;
  border-bottom: 1px solid #2d2d2d;
  display: flex;
  align-items: center;
  gap: 12px;
}

.collapse-btn {
  background: none;
  border: none;
  color: #8e8ea0;
  cursor: pointer;
  padding: 8px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s;
}

.collapse-btn:hover {
  background-color: #2d2d2d;
}

.new-chat-btn {
  flex: 1;
  background: none;
  border: 1px solid #2d2d2d;
  color: white;
  padding: 8px 12px;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  transition: background-color 0.2s;
}

.new-chat-btn:hover {
  background-color: #2d2d2d;
}

.conversations-list {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}

.section-title {
  font-size: 12px;
  color: #8e8ea0;
  margin-bottom: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.conversation-item {
  padding: 12px;
  border-radius: 6px;
  cursor: pointer;
  margin-bottom: 4px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  transition: background-color 0.2s;
  group: true;
}

.conversation-item:hover {
  background-color: #2d2d2d;
}

.conversation-item.active {
  background-color: #10a37f;
}

.conversation-title {
  flex: 1;
  font-size: 14px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-right: 8px;
}

.conversation-title-input {
  flex: 1;
  background: #2d2d2d;
  border: 1px solid #4d4d4d;
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 14px;
  margin-right: 8px;
}

.edit-btn {
  background: none;
  border: none;
  color: #8e8ea0;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  opacity: 0;
  transition: opacity 0.2s, background-color 0.2s;
}

.conversation-item:hover .edit-btn {
  opacity: 1;
}

.edit-btn:hover {
  background-color: #4d4d4d;
}

.menu-container {
  position: relative;
  display: flex;
  align-items: center;
}

.menu-btn {
  background: none;
  border: none;
  color: #8e8ea0;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  opacity: 0;
  transition: opacity 0.2s, background-color 0.2s;
}

.conversation-item:hover .menu-btn {
  opacity: 1;
}

.menu-btn:hover {
  background-color: #4d4d4d;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background-color: #2d2d2d;
  border: 1px solid #4d4d4d;
  border-radius: 4px;
  z-index: 100;
  min-width: 120px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.2);
}

.menu-item {
  padding: 8px 12px;
  font-size: 13px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.menu-item:hover {
  background-color: #10a37f;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    z-index: 1000;
    left: 0;
    top: 0;
  }
  
  .sidebar.collapsed {
    transform: translateX(-100%);
  }
}
</style>