<template>
  <div id="app">
    <h1>AI Chat Application</h1>
    <div id="sidebar">
      <button @click="createNewConversation">New Conversation</button>
      <ul>
        <li v-for="conversation in conversations" :key="conversation.id">
          {{ conversation.name }}
        </li>
      </ul>
    </div>
    <div id="main">
      <textarea v-model="newMessage" placeholder="Type your message here..."></textarea>
      <button @click="sendMessage">Send</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      conversations: [],
      newMessage: '',
    };
  },
  methods: {
    createNewConversation() {
      // Logic to create a new conversation
    },
    sendMessage() {
      // Logic to send a message
    },
  },
  mounted() {
    // Fetch existing conversations from the backend
  },
};
</script>

<style>
#app {
  display: flex;
}
#sidebar {
  width: 200px;
  border-right: 1px solid #ccc;
}
#main {
  flex: 1;
  padding: 10px;
}
</style>