import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
})

export const chatApi = {
  // 获取所有对话
  getConversations() {
    return api.get('/conversations')
  },

  // 创建新对话
  createConversation(title = '新对话') {
    return api.post('/conversations', { title })
  },

  // 获取特定对话及其消息
  getConversation(conversationId) {
    return api.get(`/conversations/${conversationId}`)
  },

  // 更新对话标题
  updateConversationTitle(conversationId, title) {
    return api.put(`/conversations/${conversationId}`, { title })
  },

  // 添加消息到对话
  addMessage(conversationId, role, content) {
    return api.post(`/conversations/${conversationId}/messages`, {
      role,
      content
    })
  },

  // 上传文件
  uploadFile(file) {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  }
}