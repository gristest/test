<template>
  <div class="file-upload">
    <input type="file" @change="uploadFile" />
  </div>
</template>

<script>
import axios from 'axios';

export default {
  methods: {
    async uploadFile(event) {
      const chatId = this.$parent.selectedChatId; // Assuming selectedChatId is managed by parent component
      const file = event.target.files[0];
      if (file) {
        const formData = new FormData();
        formData.append('file', file);

        try {
          const response = await axios.post('/api/upload/', formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          });
          console.log(response.data.info);
        } catch (error) {
          console.error('Error uploading file:', error);
        }
      }
    }
  }
};
</script>

<style scoped>
.file-upload {
  margin: 10px 0;
}
</style>
