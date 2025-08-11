

import axios from 'axios'

const API_BASE_URL = 'http://localhost:5000/api' // Backend runs on port 5000

export const fetchConversations = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/conversations`)
    return response.data
  } catch (error) {
    console.error('Failed to fetch conversations:', error)
    throw error
  }
}

export const createConversation = async (title = null) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/conversations`, {
      title: title || `新对话 ${new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}`
    })
    return response.data
  } catch (error) {
    console.error('Failed to create conversation:', error)
    throw error
  }
}

export const getMessages = async (conversationId) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/conversations/${conversationId}/messages`)
    return response.data
  } catch (error) {
    console.error('Failed to get messages:', error)
    throw error
  }
}

export const sendMessage = async (conversationId, content) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/conversations/${conversationId}/messages`, {
      content
    })
    return response.data
  } catch (error) {
    console.error('Failed to send message:', error)
    throw error
  }
}

export const updateConversationTitle = async (conversationId, title) => {
  try {
    const response = await axios.put(`${API_BASE_URL}/conversations/${conversationId}`, { title })
    return response.data
  } catch (error) {
    console.error('Failed to update conversation title:', error)
    throw error
  }
}

export const deleteConversation = async (conversationId) => {
  try {
    const response = await axios.delete(`${API_BASE_URL}/conversations/${conversationId}`)
    return response.data
  } catch (error) {
    console.error('Failed to delete conversation:', error)
    throw error
  }
}

