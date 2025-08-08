<template>
  <div class="chat-container">
    <!-- 侧边栏 -->
    <div 
      class="sidebar" 
      :class="{ collapsed: chatStore.sidebarCollapsed }"
    >
      <div class="sidebar-header">
        <el-button 
          type="primary" 
          class="new-chat-btn"
          @click="createNewChat"
          :loading="chatStore.loading"
        >
          <el-icon><Plus /></el-icon>
          <span v-if="!chatStore.sidebarCollapsed">新对话</span>
        </el-button>
      </div>
      
      <div class="sidebar-content">
        <div class="conversation-list">
          <div 
            v-for="conversation in chatStore.conversations" 
            :key="conversation.id"
            class="conversation-item"
            :class="{ active: chatStore.currentConversation?.id === conversation.id }"
            @click="selectConversation(conversation.id)"
          >
            <div class="conversation-title" v-if="!chatStore.sidebarCollapsed">
              <span>{{ conversation.title }}</span>
              <div class="conversation-actions">
                <el-icon 
                  class="edit-icon" 
                  @click.stop="editConversationTitle(conversation)"
                >
                  <Edit />
                </el-icon>
                <el-icon 
                  class="delete-icon" 
                  @click.stop="deleteConversation(conversation.id)"
                >
                  <Delete />
                </el-icon>
              </div>
            </div>
            <div class="conversation-time" v-if="!chatStore.sidebarCollapsed">
              {{ formatTime(conversation.updated_at) }}
            </div>
          </div>
        </div>
      </div>
      
      <div class="sidebar-footer">
        <el-button 
          text 
          class="collapse-btn"
          @click="chatStore.toggleSidebar()"
        >
          <el-icon>
            <component :is="chatStore.sidebarCollapsed ? 'Expand' : 'Fold'" />
          </el-icon>
        </el-button>
      </div>
    </div>

    <!-- 主内容区 -->
    <div class="main-content">
      <div v-if="!chatStore.currentConversation" class="welcome-screen">
        <div class="welcome-content">
          <h1>AI Chat</h1>
          <p>欢迎使用AI智能对话助手</p>
          <el-button type="primary" @click="createNewChat">
            开始新对话
          </el-button>
        </div>
      </div>
      
      <div v-else class="chat-area">
        <!-- 对话标题 -->
        <div class="chat-header">
          <h2>{{ chatStore.currentConversation.title }}</h2>
        </div>
        
        <!-- 消息列表 -->
        <div class="message-list" ref="messageListRef">
          <div 
            v-for="message in chatStore.messages" 
            :key="message.id"
            class="message-item"
            :class="message.role"
          >
            <div class="message-avatar">
              <el-icon v-if="message.role === 'user'">
                <User />
              </el-icon>
              <el-icon v-else>
                <Robot />
              </el-icon>
            </div>
            <div class="message-content">
              <div class="message-text">{{ message.content }}</div>
              <div class="message-time">{{ formatTime(message.created_at) }}</div>
            </div>
          </div>
          
          <!-- 加载中提示 -->
          <div v-if="chatStore.loading && isWaitingForResponse" class="message-item assistant">
            <div class="message-avatar">
              <el-icon><Robot /></el-icon>
            </div>
            <div class="message-content">
              <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 输入区域 -->
        <div class="input-area">
          <div class="input-container">
            <el-input
              v-model="inputMessage"
              type="textarea"
              :rows="3"
              placeholder="输入您的消息..."
              @keydown.enter.exact.prevent="sendMessage"
              @keydown.enter.shift.exact="handleShiftEnter"
              :disabled="chatStore.loading"
              resize="none"
            />
            <div class="input-actions">
              <el-upload
                :show-file-list="false"
                :before-upload="handleFileUpload"
                accept=".txt,.pdf,.png,.jpg,.jpeg,.gif,.doc,.docx,.xls,.xlsx"
              >
                <el-button text>
                  <el-icon><Paperclip /></el-icon>
                </el-button>
              </el-upload>
              <el-button 
                type="primary" 
                @click="sendMessage"
                :disabled="!inputMessage.trim() || chatStore.loading"
                :loading="chatStore.loading"
              >
                发送
              </el-button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 编辑对话标题对话框 -->
    <el-dialog
      v-model="editTitleDialogVisible"
      title="编辑对话标题"
      width="400px"
    >
      <el-input
        v-model="editingTitle"
        placeholder="请输入对话标题"
        @keydown.enter="saveConversationTitle"
      />
      <template #footer>
        <el-button @click="editTitleDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveConversationTitle">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useChatStore } from '@/store/chat'
import { fileApi } from '@/api/file'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  Plus, Edit, Delete, User, Robot, Paperclip, 
  Expand, Fold 
} from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const chatStore = useChatStore()

const inputMessage = ref('')
const messageListRef = ref(null)
const editTitleDialogVisible = ref(false)
const editingTitle = ref('')
const editingConversation = ref(null)
const isWaitingForResponse = ref(false)

// 初始化
onMounted(async () => {
  await chatStore.fetchConversations()
  
  // 如果URL中有对话ID，选择该对话
  if (route.params.id) {
    const conversationId = parseInt(route.params.id)
    await chatStore.selectConversation(conversationId)
  }
})

// 监听路由变化
watch(() => route.params.id, async (newId) => {
  if (newId) {
    const conversationId = parseInt(newId)
    await chatStore.selectConversation(conversationId)
  } else {
    chatStore.clearCurrentConversation()
  }
})

// 监听消息变化，自动滚动到底部
watch(() => chatStore.messages, () => {
  nextTick(() => {
    scrollToBottom()
  })
}, { deep: true })

// 创建新对话
const createNewChat = async () => {
  try {
    const conversation = await chatStore.createConversation()
    router.push(`/chat/${conversation.id}`)
  } catch (error) {
    ElMessage.error('创建对话失败')
  }
}

// 选择对话
const selectConversation = async (conversationId) => {
  router.push(`/chat/${conversationId}`)
}

// 发送消息
const sendMessage = async () => {
  if (!inputMessage.value.trim() || !chatStore.currentConversation) {
    return
  }

  const content = inputMessage.value.trim()
  inputMessage.value = ''
  isWaitingForResponse.value = true

  try {
    await chatStore.sendMessage(chatStore.currentConversation.id, content)
  } catch (error) {
    ElMessage.error('发送消息失败')
  } finally {
    isWaitingForResponse.value = false
  }
}

// 处理Shift+Enter换行
const handleShiftEnter = (event) => {
  // 允许默认行为（换行）
}

// 编辑对话标题
const editConversationTitle = (conversation) => {
  editingConversation.value = conversation
  editingTitle.value = conversation.title
  editTitleDialogVisible.value = true
}

// 保存对话标题
const saveConversationTitle = async () => {
  if (!editingTitle.value.trim()) {
    ElMessage.warning('标题不能为空')
    return
  }

  try {
    await chatStore.updateConversationTitle(
      editingConversation.value.id, 
      editingTitle.value.trim()
    )
    editTitleDialogVisible.value = false
    ElMessage.success('标题更新成功')
  } catch (error) {
    ElMessage.error('更新标题失败')
  }
}

// 删除对话
const deleteConversation = async (conversationId) => {
  try {
    await ElMessageBox.confirm('确定要删除这个对话吗？', '确认删除', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    await chatStore.deleteConversation(conversationId)
    
    // 如果删除的是当前对话，跳转到首页
    if (chatStore.currentConversation?.id === conversationId) {
      router.push('/')
    }
    
    ElMessage.success('对话删除成功')
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除对话失败')
    }
  }
}

// 文件上传
const handleFileUpload = async (file) => {
  try {
    const response = await fileApi.uploadFile(file)
    ElMessage.success(`文件 ${file.name} 上传成功`)
    
    // 可以在这里添加文件到消息中的逻辑
    if (chatStore.currentConversation) {
      const fileMessage = `[文件] ${file.name} (${formatFileSize(file.size)})`
      await chatStore.sendMessage(chatStore.currentConversation.id, fileMessage)
    }
  } catch (error) {
    ElMessage.error('文件上传失败')
  }
  
  return false // 阻止默认上传行为
}

// 滚动到底部
const scrollToBottom = () => {
  if (messageListRef.value) {
    messageListRef.value.scrollTop = messageListRef.value.scrollHeight
  }
}

// 格式化时间
const formatTime = (timeString) => {
  if (!timeString) return ''
  
  const date = new Date(timeString)
  const now = new Date()
  const diff = now - date
  
  if (diff < 60000) { // 1分钟内
    return '刚刚'
  } else if (diff < 3600000) { // 1小时内
    return `${Math.floor(diff / 60000)}分钟前`
  } else if (diff < 86400000) { // 1天内
    return `${Math.floor(diff / 3600000)}小时前`
  } else {
    return date.toLocaleDateString()
  }
}

// 格式化文件大小
const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}
</script>

<style scoped lang="scss">
.chat-container {
  display: flex;
  height: 100vh;
  background-color: #f5f5f5;
}

.sidebar {
  width: 280px;
  background-color: #2c3e50;
  color: white;
  display: flex;
  flex-direction: column;
  transition: width 0.3s ease;
  
  &.collapsed {
    width: 60px;
  }
  
  .sidebar-header {
    padding: 20px;
    border-bottom: 1px solid #34495e;
    
    .new-chat-btn {
      width: 100%;
      height: 40px;
    }
  }
  
  .sidebar-content {
    flex: 1;
    overflow-y: auto;
    padding: 10px 0;
    
    .conversation-list {
      .conversation-item {
        padding: 12px 20px;
        cursor: pointer;
        border-bottom: 1px solid #34495e;
        transition: background-color 0.2s;
        
        &:hover {
          background-color: #34495e;
        }
        
        &.active {
          background-color: #3498db;
        }
        
        .conversation-title {
          display: flex;
          justify-content: space-between;
          align-items: center;
          font-size: 14px;
          margin-bottom: 4px;
          
          .conversation-actions {
            display: flex;
            gap: 8px;
            opacity: 0;
            transition: opacity 0.2s;
            
            .edit-icon, .delete-icon {
              font-size: 12px;
              cursor: pointer;
              
              &:hover {
                color: #3498db;
              }
            }
            
            .delete-icon:hover {
              color: #e74c3c;
            }
          }
        }
        
        &:hover .conversation-actions {
          opacity: 1;
        }
        
        .conversation-time {
          font-size: 12px;
          color: #bdc3c7;
        }
      }
    }
  }
  
  .sidebar-footer {
    padding: 20px;
    border-top: 1px solid #34495e;
    
    .collapse-btn {
      width: 100%;
      color: white;
    }
  }
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  background-color: white;
  
  .welcome-screen {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    
    .welcome-content {
      text-align: center;
      
      h1 {
        font-size: 48px;
        color: #2c3e50;
        margin-bottom: 16px;
      }
      
      p {
        font-size: 18px;
        color: #7f8c8d;
        margin-bottom: 32px;
      }
    }
  }
  
  .chat-area {
    flex: 1;
    display: flex;
    flex-direction: column;
    
    .chat-header {
      padding: 20px;
      border-bottom: 1px solid #ecf0f1;
      background-color: #f8f9fa;
      
      h2 {
        color: #2c3e50;
        font-size: 20px;
        margin: 0;
      }
    }
    
    .message-list {
      flex: 1;
      overflow-y: auto;
      padding: 20px;
      
      .message-item {
        display: flex;
        margin-bottom: 20px;
        
        &.user {
          flex-direction: row-reverse;
          
          .message-content {
            background-color: #3498db;
            color: white;
            margin-right: 12px;
          }
        }
        
        &.assistant {
          .message-content {
            background-color: #ecf0f1;
            color: #2c3e50;
            margin-left: 12px;
          }
        }
        
        .message-avatar {
          width: 40px;
          height: 40px;
          border-radius: 50%;
          background-color: #bdc3c7;
          display: flex;
          align-items: center;
          justify-content: center;
          flex-shrink: 0;
          
          .el-icon {
            font-size: 20px;
            color: white;
          }
        }
        
        .message-content {
          max-width: 70%;
          padding: 12px 16px;
          border-radius: 18px;
          
          .message-text {
            line-height: 1.5;
            white-space: pre-wrap;
            word-break: break-word;
          }
          
          .message-time {
            font-size: 12px;
            opacity: 0.7;
            margin-top: 4px;
          }
        }
      }
    }
    
    .input-area {
      padding: 20px;
      border-top: 1px solid #ecf0f1;
      background-color: #f8f9fa;
      
      .input-container {
        display: flex;
        gap: 12px;
        align-items: flex-end;
        
        .el-textarea {
          flex: 1;
        }
        
        .input-actions {
          display: flex;
          gap: 8px;
          align-items: center;
        }
      }
    }
  }
}

// 打字指示器动画
.typing-indicator {
  display: flex;
  gap: 4px;
  
  span {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background-color: #bdc3c7;
    animation: typing 1.4s infinite ease-in-out;
    
    &:nth-child(1) {
      animation-delay: -0.32s;
    }
    
    &:nth-child(2) {
      animation-delay: -0.16s;
    }
  }
}

@keyframes typing {
  0%, 80%, 100% {
    transform: scale(0);
    opacity: 0.5;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}

// 响应式设计
@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    left: 0;
    top: 0;
    height: 100vh;
    z-index: 1000;
    transform: translateX(-100%);
    transition: transform 0.3s ease;
    
    &:not(.collapsed) {
      transform: translateX(0);
    }
  }
  
  .main-content {
    margin-left: 0;
  }
}
</style>