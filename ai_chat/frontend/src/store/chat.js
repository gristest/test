import { defineStore } from 'pinia'
import { chatApi } from '@/api/chat'

export const useChatStore = defineStore('chat', {
  state: () => ({
    conversations: [],
    currentConversation: null,
    messages: [],
    loading: false,
    sidebarCollapsed: false
  }),

  getters: {
    getCurrentConversationId: (state) => {
      return state.currentConversation?.id || null
    },
    
    getConversationById: (state) => {
      return (id) => state.conversations.find(conv => conv.id === parseInt(id))
    }
  },

  actions: {
    // 获取对话列表
    async fetchConversations() {
      try {
        this.loading = true
        const response = await chatApi.getConversations()
        if (response.success) {
          this.conversations = response.data
        }
      } catch (error) {
        console.error('获取对话列表失败:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    // 创建新对话
    async createConversation(title = null) {
      try {
        this.loading = true
        const response = await chatApi.createConversation(title)
        if (response.success) {
          this.conversations.unshift(response.data)
          this.currentConversation = response.data
          this.messages = []
          return response.data
        }
      } catch (error) {
        console.error('创建对话失败:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    // 选择对话
    async selectConversation(conversationId) {
      try {
        this.loading = true
        const conversation = this.getConversationById(conversationId)
        if (conversation) {
          this.currentConversation = conversation
          await this.fetchMessages(conversationId)
        }
      } catch (error) {
        console.error('选择对话失败:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    // 获取对话消息
    async fetchMessages(conversationId) {
      try {
        const response = await chatApi.getMessages(conversationId)
        if (response.success) {
          this.messages = response.data
        }
      } catch (error) {
        console.error('获取消息失败:', error)
        throw error
      }
    },

    // 发送消息
    async sendMessage(conversationId, content) {
      try {
        this.loading = true
        const response = await chatApi.sendMessage(conversationId, content)
        if (response.success) {
          // 添加用户消息和AI回复到消息列表
          this.messages.push(response.data.user_message)
          this.messages.push(response.data.ai_message)
          
          // 更新对话列表中的时间戳
          const conversation = this.conversations.find(conv => conv.id === conversationId)
          if (conversation) {
            conversation.updated_at = new Date().toISOString()
            // 将当前对话移到列表顶部
            this.conversations = [
              conversation,
              ...this.conversations.filter(conv => conv.id !== conversationId)
            ]
          }
          
          return response.data
        }
      } catch (error) {
        console.error('发送消息失败:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    // 更新对话标题
    async updateConversationTitle(conversationId, title) {
      try {
        const response = await chatApi.updateConversationTitle(conversationId, title)
        if (response.success) {
          const conversation = this.conversations.find(conv => conv.id === conversationId)
          if (conversation) {
            conversation.title = title
          }
          if (this.currentConversation && this.currentConversation.id === conversationId) {
            this.currentConversation.title = title
          }
        }
        return response
      } catch (error) {
        console.error('更新对话标题失败:', error)
        throw error
      }
    },

    // 删除对话
    async deleteConversation(conversationId) {
      try {
        const response = await chatApi.deleteConversation(conversationId)
        if (response.success) {
          this.conversations = this.conversations.filter(conv => conv.id !== conversationId)
          if (this.currentConversation && this.currentConversation.id === conversationId) {
            this.currentConversation = null
            this.messages = []
          }
        }
        return response
      } catch (error) {
        console.error('删除对话失败:', error)
        throw error
      }
    },

    // 切换侧边栏
    toggleSidebar() {
      this.sidebarCollapsed = !this.sidebarCollapsed
    },

    // 清空当前对话
    clearCurrentConversation() {
      this.currentConversation = null
      this.messages = []
    }
  }
})