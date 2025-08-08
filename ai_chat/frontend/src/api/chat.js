import request from './request'

export const chatApi = {
  // 获取对话列表
  getConversations() {
    return request.get('/conversations')
  },

  // 创建新对话
  createConversation(title = null) {
    return request.post('/conversations', { title })
  },

  // 获取对话信息
  getConversation(id) {
    return request.get(`/conversations/${id}`)
  },

  // 更新对话标题
  updateConversationTitle(id, title) {
    return request.put(`/conversations/${id}`, { title })
  },

  // 删除对话
  deleteConversation(id) {
    return request.delete(`/conversations/${id}`)
  },

  // 获取对话消息
  getMessages(conversationId) {
    return request.get(`/conversations/${conversationId}/messages`)
  },

  // 发送消息
  sendMessage(conversationId, content) {
    return request.post(`/conversations/${conversationId}/messages`, { content })
  }
}