


<template>
  <div class="chat-window" :class="{ 'sidebar-collapsed': sidebarCollapsed }">
    <div class="chat-header">
      <h2>{{ currentConversation?.title || '新对话' }}</h2>
    </div>
    
    <div class="message-list" ref="messageList">
      <div v-for="(message, index) in messages" 
           :key="index"
           class="message"
           :class="message.role">
        <div class="avatar">
          <span v-if="message.role === 'user'">👤</span>
          <span v-else>🤖</span>
        </div>
        <div class="content">
          <div class="text">{{ message.content }}</div>
          <div class="time">{{ formatTime(message.created_at) }}</div>
        </div>
      </div>
      
      <div v-if="loading" class="message assistant">
        <div class="avatar">🤖</div>
        <div class="content">
          <div class="typing-indicator">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      </div>
    </div>
    
    <div class="input-area">
      <textarea 
        v-model="inputText" 
        placeholder="输入您的消息..." 
        @keydown.enter.exact.prevent="handleSend"
        @keydown.enter.shift.exact="handleShiftEnter"
        :disabled="loading"
      ></textarea>
      <div class="actions">
        <input type="file" @change="handleFileChange" accept=".txt,.pdf,.png,.jpg,.jpeg,.doc,.docx" />
        <button @click="handleSend" :disabled="!inputText.trim() || loading">发送</button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, watch, nextTick } from 'vue'

export default {
  props: {
    currentConversation: Object,
    messages: Array,
    loading: Boolean
  },
  emits: ['send-message', 'upload-file'],
  setup(props, { emit }) {
    const inputText = ref('')
    const messageList = ref(null)
    const sidebarCollapsed = ref(false)

    // Auto-scroll to bottom when new messages arrive
    watch(() => props.messages, () => {
      nextTick(() => {
        if (messageList.value) {
          messageList.value.scrollTop = messageList.value.scrollHeight
        }
      })
    }, { deep: true })

    // Send message
    const handleSend = () => {
      if (inputText.value.trim()) {
        emit('send-message', inputText.value.trim())
        inputText.value = ''
      }
    }

    // Handle shift+enter for new line
    const handleShiftEnter = (e) => {
      inputText.value += '\n'
    }

    // Handle file upload
    const handleFileChange = (e) => {
      const file = e.target.files[0]
      if (file) {
        emit('upload-file', file)
        e.target.value = null // Reset input
      }
    }

    // Format time
    const formatTime = (timestamp) => {
      if (!timestamp) return ''
      const date = new Date(timestamp)
      return `${date.getHours()}:${String(date.getMinutes()).padStart(2, '0')}`
    }

    return {
      inputText,
      messageList,
      sidebarCollapsed,
      handleSend,
      handleShiftEnter,
      handleFileChange,
      formatTime
    }
  }
}
</script>

<style scoped>
.chat-window {
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #f5f7fa;
}

.chat-header {
  padding: 15px 20px;
  border-bottom: 1px solid #e8e8e8;
  background-color: white;
}

.message-list {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

.message {
  display: flex;
  margin-bottom: 20px;
}

.message.user {
  flex-direction: row-reverse;
}

.message.user .content {
  background-color: #3498db;
  color: white;
}

.message.assistant .content {
  background-color: #e8e8e8;
  color: #333;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #ddd;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 10px;
  font-size: 20px;
}

.content {
  max-width: 70%;
  padding: 12px 16px;
  border-radius: 18px;
}

.text {
  line-height: 1.5;
  white-space: pre-wrap;
  word-break: break-word;
}

.time {
  font-size: 12px;
  opacity: 0.7;
  margin-top: 5px;
  text-align: right;
}

.input-area {
  padding: 15px;
  border-top: 1px solid #e8e8e8;
  background-color: white;
}

textarea {
  width: 100%;
  min-height: 80px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
  resize: none;
  font-family: inherit;
  font-size: 14px;
}

.actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 10px;
}

button {
  padding: 8px 20px;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.typing-indicator {
  display: flex;
  gap: 5px;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #888;
  animation: typing 1.4s infinite ease-in-out;
}

.typing-indicator span:nth-child(1) { animation-delay: 0s; }
.typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
.typing-indicator span:nth-child(3) { animation-delay: 0.4s; }

@keyframes typing {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
}

/* Responsive design */
@media (max-width: 768px) {
  .content {
    max-width: 85%;
  }
}
</style>


