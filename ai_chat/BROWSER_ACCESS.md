# 🌐 AI聊天应用浏览器访问指南

## 📱 访问地址

### 本地访问
- **前端应用**: http://localhost:12000
- **后端API**: http://localhost:8000
- **API文档**: http://localhost:8000/docs

### 外部访问（如果配置了端口转发）
- **前端应用**: https://work-1-zrjouldkqnbapmiu.prod-runtime.all-hands.dev
- **后端API**: https://work-2-zrjouldkqnbapmiu.prod-runtime.all-hands.dev

## 🚀 服务状态

当前服务运行状态：
- ✅ 前端服务 (Vue.js + Vite): 运行在端口 12000
- ✅ 后端服务 (FastAPI): 运行在端口 8000
- ✅ 数据库 (SQLite): chat.db 已创建并包含测试数据

## 🎯 功能测试清单

在浏览器中访问 http://localhost:12000 后，您可以测试以下功能：

### 1. 界面展示
- [ ] 查看ChatGPT风格的现代化界面
- [ ] 验证响应式设计（调整浏览器窗口大小）
- [ ] 检查侧边栏和聊天区域布局

### 2. 对话管理
- [ ] 点击"新建对话"按钮创建新对话
- [ ] 在侧边栏中查看对话列表
- [ ] 点击不同对话进行切换
- [ ] 编辑对话标题

### 3. 消息功能
- [ ] 在输入框中输入消息
- [ ] 按回车键或点击发送按钮发送消息
- [ ] 查看用户消息和AI回复的不同样式
- [ ] 验证消息时间戳显示

### 4. 文件上传
- [ ] 点击文件上传按钮
- [ ] 选择文件进行上传
- [ ] 查看上传进度和结果反馈

### 5. 数据持久化
- [ ] 刷新页面后验证对话和消息是否保存
- [ ] 创建多个对话并验证数据保存

## 🔧 故障排除

如果无法访问应用，请检查：

1. **服务状态**
   ```bash
   ps aux | grep -E "(vite|python.*main.py)"
   ```

2. **端口占用**
   ```bash
   netstat -tlnp | grep -E "(12000|8000)"
   ```

3. **重启服务**
   ```bash
   # 重启前端
   cd /workspace/project/test/ai_chat/frontend
   npm run dev -- --host 0.0.0.0 --port 12000
   
   # 重启后端
   cd /workspace/project/test/ai_chat/backend
   python main.py
   ```

4. **检查日志**
   ```bash
   # 查看前端日志
   tail -f /workspace/project/test/ai_chat/frontend/*.log
   
   # 查看后端日志
   tail -f /workspace/project/test/ai_chat/backend/*.log
   ```

## 📊 测试数据

数据库中已包含以下测试数据：
- 5个测试对话
- 多条用户和AI消息
- 2个上传文件记录

## 🎨 界面特色

- **现代化设计**: 仿ChatGPT的专业界面
- **响应式布局**: 完美适配桌面和移动设备
- **消息气泡**: 用户和AI消息有不同的视觉样式
- **侧边栏**: 可折叠的对话管理面板
- **实时反馈**: 消息发送和文件上传的即时反馈

## 🚀 下一步

1. 在浏览器中打开 http://localhost:12000
2. 创建新对话并发送第一条消息
3. 体验完整的聊天功能
4. 测试文件上传功能
5. 验证数据持久化

---

**注意**: 如果遇到任何问题，请检查控制台输出或联系开发团队。