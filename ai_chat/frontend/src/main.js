
import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios'
import { API_BASE_URL } from './config'

// Configure axios
axios.defaults.baseURL = API_BASE_URL

const app = createApp(App)
app.config.globalProperties.$http = axios
app.mount('#app')
