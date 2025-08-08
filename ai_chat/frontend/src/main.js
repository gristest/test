import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// by zhb:
import { createPinia } from 'pinia'

const app = createApp(App)

// by zhb: 注册 Pinia
app.use(createPinia())  // <-- 注册 Pinia

app.use(router)
app.mount('#app')