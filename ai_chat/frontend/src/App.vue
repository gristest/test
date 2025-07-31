<template>
  <div class="app">
    <Sidebar 
      :conversations="conversations"
      :current-conversation-id="currentConversationId"
      @create-new-chat="createNewChat"
      @select-conversation="selectConversation"
      @update-conversation-title="updateConversationTitle"
    />
    
    <ChatArea 
      :current-conversation="currentConversation"
      @send-message="sendMessage"
      @upload-file="uploadFile"
    />
    
    <!-- 加载提示 -->
    <div v-if="loading" class="loading-overlay">
      <div class="loading-spinner"></div>
    </div>
  </div>
</template>

<script>
import Sidebar from './components/Sidebar.vue'
import ChatArea from './components/ChatArea.vue'
import { chatApi } from './api/chat.js'

export default {
  name: 'App',
  components: {
    Sidebar,
    ChatArea
  },
  data() {
    return {
      conversations: [],
      currentConversationId: null,
      currentConversation: null,
      loading: false
    }
  },
  
  async mounted() {
    await this.loadConversations()
  },
  
  methods: {
    async loadConversations() {
      try {
        this.loading = true
        const response = await chatApi.getConversations()
        this.conversations = response.data.map(conv => ({
          ...conv,
          editing: false,
          editTitle: conv.title
        }))
      } catch (error) {
        console.error('Failed to load conversations:', error)
        this.showError('加载对话列表失败')
      } finally {
        this.loading = false
      }
    },
    
    async createNewChat() {
      try {
        this.loading = true
        const response = await chatApi.createConversation()
        const newConversation = {
          ...response.data,
          editing: false,
          editTitle: response.data.title
        }
        this.conversations.unshift(newConversation)
        await this.selectConversation(newConversation.id)
      } catch (error) {
        console.error('Failed to create new chat:', error)
        this.showError('创建新对话失败')
      } finally {
        this.loading = false
      }
    },
    
    async selectConversation(conversationId) {
      try {
        this.loading = true
        this.currentConversationId = conversationId
        const response = await chatApi.getConversation(conversationId)
        this.currentConversation = response.data
      } catch (error) {
        console.error('Failed to load conversation:', error)
        this.showError('加载对话失败')
      } finally {
        this.loading = false
      }
    },
    
    async updateConversationTitle(conversationId, newTitle) {
      try {
        await chatApi.updateConversationTitle(conversationId, newTitle)
        
        // 更新本地数据
        const conversation = this.conversations.find(c => c.id === conversationId)
        if (conversation) {
          conversation.title = newTitle
          conversation.editTitle = newTitle
        }
        
        if (this.currentConversation && this.currentConversation.id === conversationId) {
          this.currentConversation.title = newTitle
        }
      } catch (error) {
        console.error('Failed to update conversation title:', error)
        this.showError('更新对话标题失败')
      }
    },
    
    async sendMessage(content) {
      if (!this.currentConversationId || !content.trim()) return
      
      try {
        // 立即添加用户消息到界面
        const userMessage = {
          id: Date.now(), // 临时ID
          role: 'user',
          content: content,
          created_at: new Date().toISOString()
        }
        this.currentConversation.messages.push(userMessage)
        
        // 发送消息到后台
        await chatApi.addMessage(this.currentConversationId, 'user', content)
        
        // 模拟AI回复（这里可以集成真实的AI API）
        setTimeout(async () => {
          const aiResponse = this.generateAIResponse(content)
          const assistantMessage = {
            id: Date.now() + 1,
            role: 'assistant',
            content: aiResponse,
            created_at: new Date().toISOString()
          }
          this.currentConversation.messages.push(assistantMessage)
          
          // 保存AI回复到后台
          await chatApi.addMessage(this.currentConversationId, 'assistant', aiResponse)
        }, 1000)
        
      } catch (error) {
        console.error('Failed to send message:', error)
        this.showError('发送消息失败')
      }
    },
    
    async uploadFile(file) {
      try {
        this.loading = true
        const response = await chatApi.uploadFile(file)
        
        // 添加文件上传成功的消息
        const fileMessage = {
          id: Date.now(),
          role: 'user',
          content: `已上传文件: ${file.name} (${this.formatFileSize(file.size)})`,
          created_at: new Date().toISOString()
        }
        this.currentConversation.messages.push(fileMessage)
        
        // 保存到后台
        await chatApi.addMessage(
          this.currentConversationId, 
          'user', 
          `已上传文件: ${file.name} (${this.formatFileSize(file.size)})`
        )
        
        this.showSuccess('文件上传成功')
      } catch (error) {
        console.error('Failed to upload file:', error)
        this.showError('文件上传失败')
      } finally {
        this.loading = false
      }
    },
    
    generateAIResponse(userMessage) {
      // 简单的AI回复模拟
      const responses = [
        '我理解您的问题。让我来帮助您解决这个问题。',
        '这是一个很好的问题。根据我的理解...',
        '感谢您的提问。我建议您可以考虑以下几个方面：',
        '我明白了您的需求。让我为您提供一些建议。',
        '这个问题很有意思。从我的角度来看...'
      ]
      
      return responses[Math.floor(Math.random() * responses.length)] + 
             `\n\n您刚才提到了："${userMessage}"，我会认真考虑这个问题并为您提供最佳的解决方案。`
    },
    
    formatFileSize(bytes) {
      if (bytes === 0) return '0 Bytes'
      const k = 1024
      const sizes = ['Bytes', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    },
    
    showError(message) {
      alert('错误: ' + message)
    },
    
    showSuccess(message) {
      alert('成功: ' + message)
    }
  }
}
</script>

<style>
.app {
  display: flex;
  height: 100vh;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #10a37f;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 全局样式重置 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
  background-color: #f7f7f8;
  height: 100vh;
  overflow: hidden;
}

/* 滚动条样式 */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>