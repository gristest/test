<template>
  <div class="app-container">
    <!-- Sidebar -->
    <div class="sidebar" :class="{ 'sidebar-collapsed': sidebarCollapsed }">
      <button class="toggle-btn" @click="toggleSidebar">
        {{ sidebarCollapsed ? '»' : '«' }}
      </button>
      
      <button class="new-chat-btn" @click="createNewConversation">
        + New Chat
      </button>
      
      <div class="conversation-list">
        <div 
          v-for="conversation in conversations" 
          :key="conversation.id"
          class="conversation-item"
          :class="{ active: activeConversationId === conversation.id }"
          @click="selectConversation(conversation.id)"
        >
          <span v-if="!editingConversationId || editingConversationId !== conversation.id">
            {{ conversation.name }}
            <button class="edit-btn" @click.stop="startEditing(conversation)">✏️</button>
          </span>
          <input 
            v-else
            type="text" 
            v-model="editingName"
            @blur="saveConversationName(conversation)"
            @keyup.enter="saveConversationName(conversation)"
            ref="nameInput"
            autofocus
          />
        </div>
      </div>
    </div>

    <!-- Main Chat Area -->
    <div class="main-content">
      <div class="chat-messages">
        <div 
          v-for="message in activeConversationMessages" 
          :key="message.id"
          class="message"
          :class="{ 'user-message': message.is_user, 'ai-message': !message.is_user }"
        >
          {{ message.content }}
        </div>
      </div>

      <div class="input-area">
        <div class="file-upload">
          <input type="file" @change="handleFileUpload" ref="fileInput" />
          <button @click="triggerFileInput">📎</button>
        </div>
        <textarea 
          v-model="newMessage" 
          @keyup.enter="sendMessage" 
          placeholder="Type your message..."
        ></textarea>
        <button @click="sendMessage">Send</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'App',
  data() {
    return {
      sidebarCollapsed: false,
      conversations: [],
      activeConversationId: null,
      activeConversationMessages: [],
      newMessage: '',
      editingConversationId: null,
      editingName: '',
      file: null
    };
  },
  mounted() {
    this.fetchConversations();
  },
  methods: {
    toggleSidebar() {
      this.sidebarCollapsed = !this.sidebarCollapsed;
    },
    async fetchConversations() {
      try {
        const response = await axios.get('http://localhost:5000/conversations');
        this.conversations = response.data;
        if (this.conversations.length > 0 && !this.activeConversationId) {
          this.selectConversation(this.conversations[0].id);
        }
      } catch (error) {
        console.error('Error fetching conversations:', error);
      }
    },
    async createNewConversation() {
      try {
        const response = await axios.post('http://localhost:5000/conversations');
        const newConversation = response.data;
        this.conversations.push(newConversation);
        this.selectConversation(newConversation.id);
      } catch (error) {
        console.error('Error creating conversation:', error);
      }
    },
    async selectConversation(conversationId) {
      this.activeConversationId = conversationId;
      try {
        const response = await axios.get(`http://localhost:5000/conversations/${conversationId}`);
        this.activeConversationMessages = response.data.messages;
      } catch (error) {
        console.error('Error fetching conversation messages:', error);
      }
    },
    startEditing(conversation) {
      this.editingConversationId = conversation.id;
      this.editingName = conversation.name;
      this.$nextTick(() => {
        this.$refs.nameInput[0].focus();
      });
    },
    async saveConversationName(conversation) {
      if (!this.editingName.trim()) return;
      try {
        await axios.patch(`http://localhost:5000/conversations/${conversation.id}`, {
          name: this.editingName
        });
        conversation.name = this.editingName;
        this.editingConversationId = null;
      } catch (error) {
        console.error('Error updating conversation name:', error);
      }
    },
    triggerFileInput() {
      this.$refs.fileInput.click();
    },
    handleFileUpload(event) {
      this.file = event.target.files[0];
      // In a real implementation, we would upload the file here
      alert(`File selected: ${this.file.name}. Upload functionality would be implemented here.`);
    },
    async sendMessage() {
      if (!this.newMessage.trim()) return;
      
      try {
        // Add user message
        const userMessage = {
          content: this.newMessage,
          is_user: true
        };
        
        // In a real app, we would send to API and get AI response
        // For now, we'll simulate an AI response
        this.activeConversationMessages.push(userMessage);
        
        // Simulate AI thinking
        setTimeout(async () => {
          const aiMessage = {
            content: `This is a simulated response to: "${this.newMessage}"`,
            is_user: false
          };
          this.activeConversationMessages.push(aiMessage);
        }, 1000);
        
        this.newMessage = '';
      } catch (error) {
        console.error('Error sending message:', error);
      }
    }
  }
};
</script>

<style>
/* Base styles */
body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.app-container {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

/* Sidebar styles */
.sidebar {
  width: 250px;
  background-color: #202123;
  color: white;
  transition: width 0.3s;
  position: relative;
}

.sidebar-collapsed {
  width: 50px;
}

.toggle-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  font-size: 1.2rem;
}

.new-chat-btn {
  width: 100%;
  padding: 12px;
  background-color: #343541;
  border: 1px solid #565869;
  color: white;
  text-align: left;
  cursor: pointer;
  margin-top: 40px;
}

.conversation-list {
  margin-top: 10px;
}

.conversation-item {
  padding: 10px 15px;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
}

.conversation-item:hover {
  background-color: #343541;
}

.conversation-item.active {
  background-color: #343541;
  border-left: 3px solid #10a37f;
}

.edit-btn {
  background: none;
  border: none;
  color: #ccc;
  cursor: pointer;
}

/* Main content styles */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  background-color: #343541;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

.message {
  padding: 15px;
  margin-bottom: 15px;
  border-radius: 8px;
  max-width: 80%;
}

.user-message {
  background-color: #444654;
  color: white;
  margin-left: auto;
}

.ai-message {
  background-color: #10a37f;
  color: white;
  margin-right: auto;
}

.input-area {
  display: flex;
  padding: 15px;
  background-color: #40414f;
  align-items: center;
}

.input-area textarea {
  flex: 1;
  padding: 12px;
  border-radius: 5px;
  border: none;
  resize: none;
  height: 50px;
  margin: 0 10px;
}

.input-area button {
  padding: 10px 20px;
  background-color: #10a37f;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.file-upload {
  position: relative;
}

.file-upload input {
  display: none;
}

/* Responsive styles */
@media (max-width: 768px) {
  .sidebar:not(.sidebar-collapsed) {
    position: absolute;
    z-index: 100;
    height: 100%;
  }
  
  .sidebar-collapsed {
    width: 0;
    overflow: hidden;
  }
}
</style>
