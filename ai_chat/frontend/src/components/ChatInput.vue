<template>
  <div class="chat-input">
    <textarea v-model="message" placeholder="Type your message..."></textarea>
    <button @click="sendMessage">Send</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      message: ''
    };
  },
  methods: {
    async sendMessage() {
      if (this.message.trim()) {
        try {
          await axios.post(`/api/chats/${this.$parent.selectedChatId}/records/`, {
            content: this.message
          });
          this.$parent.$refs.chatHistory.fetchChatRecords(this.$parent.selectedChatId);
        } catch (error) {
          console.error('Error sending message:', error);
        }
        this.message = '';
      }
    }
  }
};
</script>

<style scoped>
.chat-input {
  display: flex;
  padding: 10px;
  background-color: #f9f9f9;
}

textarea {
  flex: 1;
  margin-right: 10px;
}
</style>
