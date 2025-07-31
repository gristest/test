import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0',
    port: 12000,
    cors: true,
    strictPort: true,
    allowedHosts: [
      'localhost',
      '127.0.0.1',
      '0.0.0.0',
      'work-1-zrjouldkqnbapmiu.prod-runtime.all-hands.dev',
      'work-2-zrjouldkqnbapmiu.prod-runtime.all-hands.dev'
    ]
  }
})