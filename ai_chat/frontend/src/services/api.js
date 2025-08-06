


import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:5000/api',
  headers: {
    'Content-Type': 'application/json'
  }
})

export default {
  // Conversation endpoints
  getConversations() {
    return api.get('/conversations')
  },
  createConversation() {
    return api.post('/conversations')
  },
  getConversation(id) {
    return api.get(`/conversations/${id}`)
  },
  sendMessage(convId, message) {
    return api.post(`/conversations/${convId}/messages`, { content: message })
  },
  
  // File upload
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


