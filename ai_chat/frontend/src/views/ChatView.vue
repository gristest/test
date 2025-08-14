<template>
  <div v-if="!route.params.id" class="no-chat-selected">
    <h1>{{ $t('ai') }} Chat</h1>
    <p>{{ $t('noChatSelectedHint') }}</p>
  </div>
  <div v-else class="chat-view">
    <div class="messages-container" ref="messagesContainer">
      <div v-for="message in messages" :key="message.id" class="message" :class="`message-${message.sender}`">
        <div class="avatar">{{ message.sender === 'user' ? $t('user') : $t('ai') }}</div>
        <div class="content-wrapper">
          <div class="sender">{{ message.sender === 'user' ? $t('user') : $t('ai') }}</div>
          <div class="content">{{ message.content }}</div>
        </div>
      </div>
    </div>
    <div class="file-management-area" v-if="currentChat && currentChat.files && currentChat.files.length > 0">
      <strong>{{ $t('attachedFiles') }}</strong>
      <ul>
        <li v-for="file in currentChat.files" :key="file.id">
          <span class="filename">{{ file.filename }}</span>
          <button @click="removeFile(file.id)" :disabled="file.isUploading" class="delete-file-btn" :title="$t('delete')">🗑️</button>
        </li>
      </ul>
    </div>
    <div class="input-container">
      <button @click="triggerFileUpload" class="attach-btn">📎</button>
      <input type="file" ref="fileInput" @change="handleFileUpload" style="display: none" />
      <textarea v-model="newMessage" @keyup.enter.prevent="handleEnter" :placeholder="$t('typeMessage')"></textarea>
      <button @click="sendMessage" :disabled="!newMessage.trim()">{{ $t('send') }}</button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed, nextTick } from 'vue'
import { useChatStore } from '../store'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'

const store = useChatStore()
const route = useRoute()
const { t } = useI18n()

const newMessage = ref('')
const fileInput = ref(null)
const messagesContainer = ref(null)

const messages = computed(() => store.messages)
const currentChat = computed(() => store.currentChat)

watch(() => route.params.id, (newId) => {
  if (newId) {
    store.fetchChat(newId)
  }
}, { immediate: true })

watch(messages, () => {
  scrollToBottom();
})

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
    }
  });
}

const handleEnter = (event) => {
  if (!event.shiftKey) {
    sendMessage();
  }
}

const sendMessage = async () => {
  if (newMessage.value.trim() !== '') {
    await store.sendMessage(route.params.id, { content: newMessage.value, sender: 'user' })
    newMessage.value = ''
  }
}

const removeFile = (fileId) => {
  if (confirm(t('deleteFileConfirmation'))) {
    store.deleteFile(route.params.id, fileId);
  }
}

const triggerFileUpload = () => {
  fileInput.value.click();
}

const handleFileUpload = async (event) => {
  const file = event.target.files[0];
  if (file) {
    await store.uploadFile(route.params.id, file);
    // Optionally clear the file input
    event.target.value = '';
  }
}
</script>

<style scoped>
.chat-view {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.no-chat-selected {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
  color: #888;
}

.messages-container {
  flex-grow: 1;
  overflow-y: auto;
  padding: 20px;
}

.message {
  display: flex;
  margin-bottom: 20px;
  max-width: 80%;
}

.message-user {
  margin-left: auto;
  flex-direction: row-reverse;
}

.message-ai {
  margin-right: auto;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #ddd;
  display: flex;
  justify-content: center;
  align-items: center;
  font-weight: bold;
  margin: 0 10px;
}

.message-user .avatar {
  background-color: #007bff;
  color: white;
}

.message-ai .avatar {
  background-color: #6c757d;
  color: white;
}

.content-wrapper {
  display: flex;
  flex-direction: column;
}

.sender {
  font-size: 0.8em;
  color: #666;
  margin-bottom: 4px;
  text-transform: capitalize;
}

.message-user .sender {
  align-self: flex-end;
}

.content {
  padding: 10px 15px;
  border-radius: 18px;
  background-color: #f1f1f1;
}

.file-management-area {
  padding: 10px 20px;
  border-top: 1px solid #ddd;
  background-color: #f8f9fa;
  font-size: 0.9em;
}

.file-management-area ul {
  list-style: none;
  padding: 0;
  margin: 10px 0 0 0;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.file-management-area li {
  display: inline-flex;
  align-items: center;
  padding: 5px 10px;
  background-color: #e9ecef;
  border-radius: 15px;
  border: 1px solid #dee2e6;
}

.filename {
  max-width: 150px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-right: 8px;
}

.delete-file-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  line-height: 1;
}
.input-container {
  display: flex;
  padding: 10px;
  border-top: 1px solid #ddd;
  background-color: #fff;
}

textarea {
  flex-grow: 1;
  resize: none;
  border-radius: 18px;
  padding: 10px 15px;
  border: 1px solid #ccc;
  margin: 0 10px;
}
</style>
