


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
import { fetchConversations, createConversation, getMessages, sendMessage as apiSendMessage} from '@/api/chat'
import { uploadFile as apiUploadFile} from '@/api/file'

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
        conversations.value = (await fetchConversations()).data
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
        const response = await getMessages(id)
        if (response.success) {
          messages.value = response.data
          router.push(`/chat/${id}`)
        } else {
          console.error('Failed to load messages: API returned success=false')
        }
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
        const response = await createConversation()
        if (response.success) {
          const conversation = response.data
          conversations.value.unshift(conversation)
          currentConversation.value = conversation
          messages.value = []
          router.push(`/chat/${conversation.id}`)
        } else {
          console.error('Failed to create conversation: API returned success=false')
        }
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
        messages.value.push({
          content,
          role: 'user',
          timestamp: new Date().toISOString()
        })
        const response = await apiSendMessage(currentConversation.value.id, content)
        if (response.success) {
          messages.value.pop() // Remove user message from UI
          messages.value.push(response.data.user_message)
          messages.value.push(response.data.ai_message)
        } else {
          console.error('Failed to send message: API returned success=false')
        }
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
        const uploadResponse = await apiUploadFile(file)
        if (!uploadResponse.success) {
          console.error('文件上传失败: API returned success=false')
          return
        }
        if (currentConversation.value) {
          const fileMessage = `[文件] ${file.name} (${formatFileSize(file.size)})`
          await apiSendMessage(currentConversation.value.id, fileMessage)
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


