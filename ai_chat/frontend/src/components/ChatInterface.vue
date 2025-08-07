<template>
  <div class="chat-interface">
    <Sidebar />
    <div class="main-display">
      <ChatHistory />
      <ChatInput />
    </div>
  </div>
</template>

<script>
import Sidebar from './Sidebar.vue';
import ChatHistory from './ChatHistory.vue';
import ChatInput from './ChatInput.vue';

export default {
  components: {
    Sidebar,
    ChatHistory,
    ChatInput
  }
};
</script>

<style scoped>
.chat-interface {
  display: flex;
  height: 100vh;
}

.main-display {
  flex: 1;
  display: flex;
  flex-direction: column;
}
</style>
