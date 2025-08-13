<template>
  <div v-if="!route.params.id" class="no-chat-selected">
    <h1>AI Chat</h1>
    <p>Select a chat from the sidebar or create a new one to begin.</p>
  </div>
  <div v-else class="chat-view">
    <div class="messages-container" ref="messagesContainer">
      <div v-for="message in messages" :key="message.id" class="message" :class="`message-${message.sender}`">
        <div class="avatar">{{ message.sender === 'user' ? 'U' : 'AI' }}</div>
        <div class="content-wrapper">
          <div class="sender">{{ message.sender }}</div>
          <div class="content">{{ message.content }}</div>
        </div>
      </div>
    </div>
    <div class="input-container">
      <button @click="triggerFileUpload" class="attach-btn">📎</button>
      <input type="file" ref="fileInput" @change="handleFileUpload" style="display: none" />
      <textarea v-model="newMessage" @keyup.enter.prevent="handleEnter" placeholder="Type a message..."></textarea>
      <button @click="sendMessage" :disabled="!newMessage.trim()">Send</button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed, nextTick } from 'vue'
import { useChatStore } from '../store'
import { useRoute } from 'vue-router'

const store = useChatStore()
const route = useRoute()

const newMessage = ref('')
const fileInput = ref(null)
const messagesContainer = ref(null)

const messages = computed(() => store.messages)

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
