# AI聊天应用 - 外部访问指南

## 🌐 访问地址

### 主要访问地址
- **前端应用**: https://work-1-zrjouldkqnbapmiu.prod-runtime.all-hands.dev
- **后端API**: https://work-2-zrjouldkqnbapmiu.prod-runtime.all-hands.dev
- **API文档**: https://work-2-zrjouldkqnbapmiu.prod-runtime.all-hands.dev/docs

### 本地访问地址
- **前端应用**: http://localhost:12000
- **后端API**: http://localhost:8000
- **API文档**: http://localhost:8000/docs

## 🔧 已解决的问题

### 1. Vite主机访问限制
**问题**: `This host is not allowed`
**解决方案**: 在 `vite.config.js` 中添加了 `allowedHosts` 配置

```javascript
server: {
  allowedHosts: [
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
    'work-1-zrjouldkqnbapmiu.prod-runtime.all-hands.dev',
    'work-2-zrjouldkqnbapmiu.prod-runtime.all-hands.dev'
  ]
}
```

### 2. CORS跨域配置
**问题**: 前端无法访问后端API
**解决方案**: 在后端 `main.py` 中配置了完整的CORS设置

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:12000",
        "https://work-1-zrjouldkqnbapmiu.prod-runtime.all-hands.dev",
        "https://work-2-zrjouldkqnbapmiu.prod-runtime.all-hands.dev",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 3. 动态API地址配置
**问题**: 前端硬编码localhost地址
**解决方案**: 在 `chat.js` 中添加了动态API地址选择

```javascript
const getApiBaseUrl = () => {
  const hostname = window.location.hostname
  if (hostname === 'work-1-zrjouldkqnbapmiu.prod-runtime.all-hands.dev') {
    return 'https://work-2-zrjouldkqnbapmiu.prod-runtime.all-hands.dev/api'
  }
  return 'http://localhost:8000/api'
}
```

## 🚀 服务状态

运行以下命令检查服务状态：
```bash
python check_services.py
```

## 📱 功能特性

- ✅ 实时聊天界面
- ✅ 多对话管理
- ✅ 文件上传功能
- ✅ 响应式设计
- ✅ 跨域访问支持
- ✅ 外部域名访问

## 🔍 故障排除

如果遇到访问问题：

1. **检查服务状态**
   ```bash
   python check_services.py
   ```

2. **重启服务**
   ```bash
   # 重启前端
   pkill -f "vite.*12000"
   cd frontend && npm run dev

   # 重启后端
   pkill -f "python.*main.py"
   cd backend && python main.py
   ```

3. **检查端口占用**
   ```bash
   netstat -tulpn | grep -E "(12000|8000)"
   ```

## 📊 数据库状态

当前数据库包含 5 个测试对话，所有功能正常运行。

---

**最后更新**: 2025-07-31
**状态**: ✅ 所有服务正常运行，外部访问已配置完成