<template>
  <div class="chat-area">
    <!-- 聊天消息区域 -->
    <div class="messages-container" ref="messagesContainer">
      <div v-if="!currentConversation" class="welcome-message">
        <h2>欢迎使用 AI Chat</h2>
        <p>选择一个对话或创建新对话开始聊天</p>
      </div>
      
      <div v-else class="messages">
        <div 
          v-for="message in currentConversation.messages" 
          :key="message.id"
          class="message"
          :class="{ 'user-message': message.role === 'user', 'assistant-message': message.role === 'assistant' }"
        >
          <div class="message-content">
            <div class="message-text">{{ message.content }}</div>
            <div class="message-time">{{ formatTime(message.created_at) }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 输入区域 -->
    <div class="input-area" v-if="currentConversation">
      <div class="input-container">
        <div class="file-upload-area" v-if="selectedFile">
          <div class="selected-file">
            <span>{{ selectedFile.name }}</span>
            <button @click="removeFile" class="remove-file-btn">×</button>
          </div>
        </div>
        
        <div class="input-row">
          <button class="file-upload-btn" @click="triggerFileUpload">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66L9.64 16.2a2 2 0 0 1-2.83-2.83l8.49-8.48"/>
            </svg>
          </button>
          
          <textarea
            v-model="inputMessage"
            @keydown="handleKeyDown"
            placeholder="输入消息..."
            class="message-input"
            rows="1"
            ref="messageInput"
          ></textarea>
          
          <button 
            @click="sendMessage" 
            :disabled="!inputMessage.trim() && !selectedFile"
            class="send-btn"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z"/>
            </svg>
          </button>
        </div>
      </div>
      
      <input 
        type="file" 
        ref="fileInput" 
        @change="handleFileSelect" 
        style="display: none"
        accept="*/*"
      />
    </div>
  </div>
</template>

<script>
export default {
  name: 'ChatArea',
  props: {
    currentConversation: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      inputMessage: '',
      selectedFile: null
    }
  },
  methods: {
    sendMessage() {
      if (!this.inputMessage.trim() && !this.selectedFile) return
      
      const message = this.inputMessage.trim()
      this.inputMessage = ''
      
      if (this.selectedFile) {
        this.$emit('upload-file', this.selectedFile)
        this.selectedFile = null
      }
      
      if (message) {
        this.$emit('send-message', message)
      }
      
      this.$nextTick(() => {
        this.scrollToBottom()
        this.adjustTextareaHeight()
      })
    },
    
    handleKeyDown(event) {
      if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault()
        this.sendMessage()
      }
    },
    
    triggerFileUpload() {
      this.$refs.fileInput.click()
    },
    
    handleFileSelect(event) {
      const file = event.target.files[0]
      if (file) {
        // 检查文件大小（10MB限制）
        const maxSize = 10 * 1024 * 1024 // 10MB
        if (file.size > maxSize) {
          alert('文件大小不能超过10MB')
          return
        }
        this.selectedFile = file
      }
      // 清空input值，允许重复选择同一文件
      event.target.value = ''
    },
    
    removeFile() {
      this.selectedFile = null
    },
    
    formatTime(timestamp) {
      const date = new Date(timestamp)
      return date.toLocaleTimeString('zh-CN', { 
        hour: '2-digit', 
        minute: '2-digit' 
      })
    },
    
    scrollToBottom() {
      this.$nextTick(() => {
        const container = this.$refs.messagesContainer
        if (container) {
          container.scrollTop = container.scrollHeight
        }
      })
    },
    
    adjustTextareaHeight() {
      const textarea = this.$refs.messageInput
      if (textarea) {
        textarea.style.height = 'auto'
        textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px'
      }
    }
  },
  
  watch: {
    currentConversation: {
      handler() {
        this.$nextTick(() => {
          this.scrollToBottom()
        })
      },
      deep: true
    },
    
    inputMessage() {
      this.$nextTick(() => {
        this.adjustTextareaHeight()
      })
    }
  },
  
  mounted() {
    this.scrollToBottom()
  }
}
</script>

<style scoped>
.chat-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #ffffff;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background-color: #ffffff;
}

.welcome-message {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  text-align: center;
  color: #6b7280;
}

.welcome-message h2 {
  font-size: 24px;
  margin-bottom: 8px;
  color: #374151;
}

.messages {
  max-width: 800px;
  margin: 0 auto;
}

.message {
  margin-bottom: 24px;
  display: flex;
}

.user-message {
  justify-content: flex-end;
}

.assistant-message {
  justify-content: flex-start;
}

.message-content {
  max-width: 70%;
  padding: 12px 16px;
  border-radius: 18px;
  position: relative;
}

.user-message .message-content {
  background-color: #10a37f;
  color: white;
  border-bottom-right-radius: 4px;
}

.assistant-message .message-content {
  background-color: #f7f7f8;
  color: #374151;
  border-bottom-left-radius: 4px;
}

.message-text {
  line-height: 1.5;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.message-time {
  font-size: 11px;
  opacity: 0.7;
  margin-top: 4px;
}

.input-area {
  border-top: 1px solid #e5e7eb;
  background-color: #ffffff;
  padding: 20px;
}

.input-container {
  max-width: 800px;
  margin: 0 auto;
}

.file-upload-area {
  margin-bottom: 12px;
}

.selected-file {
  display: inline-flex;
  align-items: center;
  background-color: #f3f4f6;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  padding: 8px 12px;
  font-size: 14px;
  color: #374151;
}

.remove-file-btn {
  background: none;
  border: none;
  color: #6b7280;
  cursor: pointer;
  margin-left: 8px;
  font-size: 18px;
  line-height: 1;
}

.remove-file-btn:hover {
  color: #ef4444;
}

.input-row {
  display: flex;
  align-items: flex-end;
  gap: 12px;
  background-color: #ffffff;
  border: 1px solid #d1d5db;
  border-radius: 12px;
  padding: 12px;
}

.file-upload-btn {
  background: none;
  border: none;
  color: #6b7280;
  cursor: pointer;
  padding: 8px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s;
}

.file-upload-btn:hover {
  background-color: #f3f4f6;
}

.message-input {
  flex: 1;
  border: none;
  outline: none;
  resize: none;
  font-size: 16px;
  line-height: 1.5;
  min-height: 24px;
  max-height: 120px;
  font-family: inherit;
}

.message-input::placeholder {
  color: #9ca3af;
}

.send-btn {
  background-color: #10a37f;
  border: none;
  color: white;
  cursor: pointer;
  padding: 8px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s;
}

.send-btn:hover:not(:disabled) {
  background-color: #0d8f6b;
}

.send-btn:disabled {
  background-color: #d1d5db;
  cursor: not-allowed;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .messages-container {
    padding: 16px;
  }
  
  .input-area {
    padding: 16px;
  }
  
  .message-content {
    max-width: 85%;
  }
}
</style>