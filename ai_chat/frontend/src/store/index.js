import { defineStore } from 'pinia'
import axios from 'axios'

const API_URL = 'http://localhost:5000/api/v1'

export const useChatStore = defineStore('chat', {
  state: () => ({
    chats: [],
    currentChat: null,
    messages: [],
  }),
  actions: {
    async fetchChats() {
      const response = await axios.get(`${API_URL}/chats`)
      this.chats = response.data
    },
    async fetchChat(id) {
      const response = await axios.get(`${API_URL}/chats/${id}`)
      this.currentChat = response.data
      this.messages = response.data.messages
    },
    async createNewChat() {
      const response = await axios.post(`${API_URL}/chats`, { name: 'New Chat' })
      await this.fetchChats()
      return response.data
    },
    async sendMessage(chatId, message) {
      const response = await axios.post(`${API_URL}/chats/${chatId}/messages`, message)
      this.messages.push(response.data)
    },
  },
})
