import { defineStore } from 'pinia'
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api/v1'

export const useChatStore = defineStore('chat', {
  state: () => ({
    chats: [],
    currentChat: null,
    messages: [],
    loading: false,
    error: null,
  }),
  actions: {
    async fetchChats() {
      try {
        this.loading = true;
        const response = await axios.get(`${API_URL}/chats`);
        this.chats = response.data;
      } catch (error) {
        this.error = error;
      } finally {
        this.loading = false;
      }
    },
    async fetchChat(id) {
      try {
        this.loading = true;
        const response = await axios.get(`${API_URL}/chats/${id}`);
        this.currentChat = response.data;
        this.messages = response.data.messages;
      } catch (error) {
        this.error = error;
      } finally {
        this.loading = false;
      }
    },
    async createNewChat() {
      try {
        const response = await axios.post(`${API_URL}/chats`, { name: 'New Chat' });
        this.chats.unshift(response.data); // Add to the top of the list
        return response.data;
      } catch (error) {
        this.error = error;
      }
    },
    async updateChatName(chatId, newName) {
      try {
        const response = await axios.put(`${API_URL}/chats/${chatId}`, { name: newName });
        const index = this.chats.findIndex(c => c.id === chatId);
        if (index !== -1) {
            this.chats[index].name = response.data.name;
        }
        if (this.currentChat && this.currentChat.id === chatId) {
            this.currentChat.name = response.data.name;
        }
      } catch (error) {
        this.error = error;
      }
    },
    async deleteChat(chatId) {
      try {
        await axios.delete(`${API_URL}/chats/${chatId}`);
        this.chats = this.chats.filter(c => c.id !== chatId);
        if (this.currentChat && this.currentChat.id === chatId) {
          this.currentChat = null;
          this.messages = [];
        }
      } catch (error) {
        this.error = error;
      }
    },
    async sendMessage(chatId, message) {
      // 为实现乐观UI更新，先在界面上添加一条临时消息
      const tempId = Date.now();
      const tempMessage = {
        ...message,
        id: tempId,
      };
      this.messages.push(tempMessage);

      try {
        const response = await axios.post(`${API_URL}/chats/${chatId}/messages/`, message);
        const [realUserMessage, aiMessage] = response.data;

        // 收到后端真实数据后，用真实消息替换临时消息，并添加AI消息
        const index = this.messages.findIndex(m => m.id === tempId);
        if (index !== -1) {
          this.messages.splice(index, 1, realUserMessage, aiMessage);
        } else {
          // 如果找不到临时消息（异常情况），直接追加
          this.messages.push(realUserMessage, aiMessage);
        }
      } catch (error) {
        this.error = error;
        // 如果API调用失败，从界面上移除之前添加的临时消息
        this.messages = this.messages.filter(m => m.id !== tempId);
      }
    },
    async deleteFile(chatId, fileId) {
      try {
        await axios.delete(`${API_URL}/chats/${chatId}/files/${fileId}`);
        if (this.currentChat) {
          this.currentChat.files = this.currentChat.files.filter(f => f.id !== fileId);
        }
      } catch (error) {
        this.error = error;
        alert('Failed to delete file.');
      }
    },
    async uploadFile(chatId, file) {
      // 为实现上传状态UI，先添加一个临时文件对象
      const tempFileId = `uploading-${Date.now()}`;
      const tempFile = {
        id: tempFileId,
        filename: `${file.name} (uploading...)`,
        isUploading: true,
      };
      if (this.currentChat) {
        this.currentChat.files.push(tempFile);
      }

      const formData = new FormData();
      formData.append('file', file);
      try {
        const response = await axios.post(`${API_URL}/chats/${chatId}/files/`, formData);
        // 用真实数据替换临时文件
        const index = this.currentChat.files.findIndex(f => f.id === tempFileId);
        if (index !== -1) {
          this.currentChat.files.splice(index, 1, response.data);
        }
      } catch (error) {
        this.error = error;
        alert(`Error uploading ${file.name}: ${error.response?.data?.detail || error.message}`);
        // 上传失败，移除临时文件
        this.currentChat.files = this.currentChat.files.filter(f => f.id !== tempFileId);
      }
    }
  },
})
