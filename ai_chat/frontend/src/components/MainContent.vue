

<template>
  <main class="main-content">
    <div class="chat-container">
      <div class="message-list">
        <!-- Messages will be rendered here -->
      </div>
      <div class="input-area">
        <div class="file-upload">
          <input type="file" @change="handleFileUpload" accept=".txt,.pdf,.docx" />
        </div>
        <textarea 
          v-model="message" 
          placeholder="Type your message here..."
          @keydown.enter.prevent="sendMessage"
        ></textarea>
        <button @click="sendMessage">Send</button>
      </div>
    </div>
  </main>
</template>

<script>
import api from '@/services/api'

export default {
  name: 'ChatMainContent',
  props: {
    conversationId: String
  },
  data() {
    return {
      message: '',
      messages: []
    }
  },
  methods: {
    async sendMessage() {
      if (this.message.trim()) {
        try {
          await api.sendMessage(this.conversationId, this.message)
          this.message = ''
          this.fetchMessages()
        } catch (error) {
          console.error('Error sending message:', error)
        }
      }
    },
    async handleFileUpload(event) {
      const file = event.target.files[0]
      if (file) {
        try {
          await api.uploadFile(file)
          // Handle successful upload
        } catch (error) {
          console.error('Error uploading file:', error)
        }
      }
    },
    async fetchMessages() {
      if (this.conversationId) {
        try {
          const response = await api.getConversation(this.conversationId)
          this.messages = response.data.messages || []
        } catch (error) {
          console.error('Error fetching messages:', error)
        }
      }
    }
  },
  watch: {
    conversationId() {
      this.fetchMessages()
    }
  }
}
</script>

<style lang="scss" scoped>
@import '@/styles/variables.scss';

.main-content {
  flex: 1;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.chat-container {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.message-list {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}

.input-area {
  padding: 16px;
  border-top: 1px solid $border-color;
  
  textarea {
    width: 100%;
    min-height: 60px;
    padding: 8px;
    margin-bottom: 8px;
  }
}

.file-upload {
  margin-bottom: 8px;
}
</style>

