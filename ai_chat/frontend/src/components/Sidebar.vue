

<template>
  <div class="sidebar" :class="{ collapsed }" :style="{ width: collapsed ? '60px' : '280px' }">
    <div class="sidebar-header">
      <button class="new-chat-btn" @click="$emit('new-conversation')">
        <i class="icon-plus"></i>
        <span v-if="!collapsed">新对话</span>
      </button>
    </div>

    <div class="conversation-list">
      <div v-for="conversation in conversations" 
           :key="conversation.id"
           class="conversation-item"
           :class="{ active: currentId === conversation.id }"
           @click="$emit('select-conversation', conversation.id)">
        <div class="conversation-title" v-if="!collapsed">
          <span>{{ conversation.title }}</span>
        </div>
        <i class="icon-chat" v-else></i>
      </div>
    </div>

    <div class="sidebar-footer">
      <button class="collapse-btn" @click="$emit('toggle-sidebar')">
        <i :class="collapsed ? 'icon-expand' : 'icon-collapse'"></i>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    conversations: Array,
    collapsed: Boolean,
    currentId: [String, Number]
  },
  emits: ['select-conversation', 'new-conversation', 'toggle-sidebar']
}
</script>

<style scoped>
.sidebar {
  background-color: #2c3e50;
  color: white;
  height: 100%;
  display: flex;
  flex-direction: column;
  transition: width 0.3s ease;
}

.sidebar-header {
  padding: 20px;
  border-bottom: 1px solid #34495e;
}

.new-chat-btn {
  width: 100%;
  height: 40px;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.conversation-list {
  flex: 1;
  overflow-y: auto;
  padding: 10px 0;
}

.conversation-item {
  padding: 12px 20px;
  cursor: pointer;
  border-bottom: 1px solid #34495e;
  transition: background-color 0.2s;
}

.conversation-item:hover {
  background-color: #34495e;
}

.conversation-item.active {
  background-color: #3498db;
}

.conversation-title {
  font-size: 14px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.sidebar-footer {
  padding: 20px;
  border-top: 1px solid #34495e;
}

.collapse-btn {
  width: 100%;
  color: white;
  background: none;
  border: none;
  cursor: pointer;
}

/* Collapsed state */
.collapsed .conversation-title,
.collapsed .new-chat-btn span {
  display: none;
}

.collapsed .conversation-item {
  display: flex;
  justify-content: center;
  padding: 15px 0;
}

.collapsed .new-chat-btn {
  justify-content: center;
}
</style>

