<template>
  <div class="chat-history">
    <div v-for="record in chatRecords" :key="record.id">
      <p>{{ record.content }}</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      chatRecords: []
    };
  },
  watch: {
    selectedChatId: {
      immediate: true,
      handler(newChatId) {
        if (newChatId) {
          this.fetchChatRecords(newChatId);
        }
      }
    }
  },
  methods: {
    async fetchChatRecords(chatId) {
      try {
        const response = await axios.get(`/api/chats/${chatId}/`);
        this.chatRecords = response.data.records;
      } catch (error) {
        console.error('Error fetching chat records:', error);
      }
    }
  },
  mounted() {
    // Fetch chat records from API
  }
};
</script>

<style scoped>
.chat-history {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
  background-color: #fff;
}
</style>
