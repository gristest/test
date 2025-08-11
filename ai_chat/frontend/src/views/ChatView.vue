


<template>
  <div class="chat-container">
    <sidebar :conversations="conversations" 
             @select-conversation="selectConversation"
             @new-conversation="createNewConversation"
             @toggle-sidebar="sidebarCollapsed = !sidebarCollapsed"
             :collapsed="sidebarCollapsed" />
             
    <chat-window :currentConversation="currentConversation" 
                 :messages="messages"
                 :loading="loading"
                 @send-message="sendMessage"
                 @upload-file="uploadFile" />
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Sidebar from '@/components/Sidebar.vue'
import ChatWindow from '@/components/ChatWindow.vue'
import { fetchConversations, createConversation, getMessages, sendMessage } from '@/api/chat'
import { uploadFile } from '@/api/file'

export default {
  components: { Sidebar, ChatWindow },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const conversations = ref([])
    const currentConversation = ref(null)
    const messages = ref([])
    const loading = ref(false)
    const sidebarCollapsed = ref(false)

    // Load conversations on mount
    onMounted(async () => {
      loading.value = true
      try {
        conversations.value = await fetchConversations()
        if (route.params.id) {
          selectConversation(route.params.id)
        }
      } catch (error) {
        console.error('Failed to load conversations:', error)
      } finally {
        loading.value = false
      }
    })

    // Select conversation
    const selectConversation = async (id) => {
      loading.value = true
      try {
        currentConversation.value = conversations.value.find(c => c.id === id)
        messages.value = await getMessages(id)
        router.push(`/chat/${id}`)
      } catch (error) {
        console.error('Failed to load conversation:', error)
      } finally {
        loading.value = false
      }
    }

    // Create new conversation
    const createNewConversation = async () => {
      loading.value = true
      try {
        const conversation = await createConversation()
        conversations.value.unshift(conversation)
        currentConversation.value = conversation
        messages.value = []
        router.push(`/chat/${conversation.id}`)
      } catch (error) {
        console.error('Failed to create conversation:', error)
      } finally {
        loading.value = false
      }
    }

    // Send message
    const sendMessage = async (content) => {
      if (!content.trim() || !currentConversation.value) return
      
      loading.value = true
      try {
        const newMessage = await sendMessage(currentConversation.value.id, content)
        messages.value.push(newMessage)
      } catch (error) {
        console.error('Failed to send message:', error)
      } finally {
        loading.value = false
      }
    }

    // Upload file
    const uploadFile = async (file) => {
      const MAX_SIZE = 10 * 1024 * 1024 // 10MB
      if (file.size > MAX_SIZE) {
        alert(`文件大小不能超过10MB，当前文件为${formatFileSize(file.size)}`)
        return false
      }
      
      loading.value = true
      try {
        await uploadFile(file)
        if (currentConversation.value) {
          const fileMessage = `[文件] ${file.name} (${formatFileSize(file.size)})`
          await sendMessage(currentConversation.value.id, fileMessage)
        }
      } catch (error) {
        console.error('文件上传失败:', error)
      } finally {
        loading.value = false
      }
    }

    // Format file size
    const formatFileSize = (bytes) => {
      if (bytes === 0) return '0 B'
      const k = 1024
      const sizes = ['B', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    }

    return {
      conversations,
      currentConversation,
      messages,
      loading,
      sidebarCollapsed,
      selectConversation,
      createNewConversation,
      sendMessage,
      uploadFile
    }
  }
}
</script>

<style scoped>
.chat-container {
  display: flex;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
}
</style>


