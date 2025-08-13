<template>
  <div class="chat-view">
    <div class="messages-container">
      <div v-for="message in messages" :key="message.id" class="message">
        <div class="sender">{{ message.sender }}</div>
        <div class="content">{{ message.content }}</div>
      </div>
    </div>
    <div class="input-container">
      <textarea v-model="newMessage" @keyup.enter="sendMessage"></textarea>
      <button @click="sendMessage">Send</button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useChatStore } from '../store'
import { useRoute } from 'vue-router'

const store = useChatStore()
const route = useRoute()

const newMessage = ref('')

const messages = store.messages

watch(() => route.params.id, (newId) => {
  if (newId) {
    store.fetchChat(newId)
  }
}, { immediate: true })

const sendMessage = () => {
  if (newMessage.value.trim() !== '') {
    store.sendMessage(route.params.id, { content: newMessage.value, sender: 'user' })
    newMessage.value = ''
  }
}
</script>

<style scoped>
.chat-view {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.messages-container {
  flex-grow: 1;
  overflow-y: auto;
  padding: 20px;
}

.input-container {
  display: flex;
  padding: 10px;
}

textarea {
  flex-grow: 1;
  resize: none;
}
</style>
