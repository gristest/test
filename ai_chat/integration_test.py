#!/usr/bin/env python3
"""
集成测试：验证前端和后端的完整功能
"""
import requests
import json
import time
import subprocess
import os

def test_backend_api():
    """测试后端API功能"""
    print("🔧 测试后端API功能...")
    
    base_url = "http://localhost:8000/api"
    
    # 测试健康检查
    try:
        response = requests.get(f"{base_url}/conversations", timeout=5)
        if response.status_code == 200:
            print("✅ 后端API正常运行")
            return True
        else:
            print(f"❌ 后端API响应异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 后端API连接失败: {e}")
        return False

def test_frontend_service():
    """测试前端服务"""
    print("🎨 测试前端服务...")
    
    try:
        response = requests.get("http://localhost:12000", timeout=5)
        if response.status_code == 200 and "AI Chat" in response.text:
            print("✅ 前端服务正常运行")
            return True
        else:
            print(f"❌ 前端服务响应异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 前端服务连接失败: {e}")
        return False

def test_cors_headers():
    """测试CORS配置"""
    print("🌐 测试CORS配置...")
    
    try:
        response = requests.options("http://localhost:8000/api/conversations", 
                                  headers={
                                      'Origin': 'http://localhost:12000',
                                      'Access-Control-Request-Method': 'GET'
                                  })
        
        cors_headers = response.headers.get('Access-Control-Allow-Origin')
        if cors_headers == '*' or 'localhost:12000' in str(cors_headers):
            print("✅ CORS配置正确")
            return True
        else:
            print(f"❌ CORS配置问题: {cors_headers}")
            return False
    except Exception as e:
        print(f"❌ CORS测试失败: {e}")
        return False

def test_complete_workflow():
    """测试完整的聊天工作流程"""
    print("💬 测试完整聊天工作流程...")
    
    base_url = "http://localhost:8000/api"
    
    try:
        # 1. 创建对话
        response = requests.post(f"{base_url}/conversations", 
                               json={"title": "集成测试对话"})
        if response.status_code != 200:
            print(f"❌ 创建对话失败: {response.status_code}")
            return False
        
        conversation = response.json()
        conv_id = conversation['id']
        print(f"✅ 创建对话成功 (ID: {conv_id})")
        
        # 2. 发送用户消息
        response = requests.post(f"{base_url}/conversations/{conv_id}/messages",
                               json={"role": "user", "content": "Hello, this is a test message"})
        if response.status_code != 200:
            print(f"❌ 发送用户消息失败: {response.status_code}")
            return False
        print("✅ 发送用户消息成功")
        
        # 3. 发送AI回复
        response = requests.post(f"{base_url}/conversations/{conv_id}/messages",
                               json={"role": "assistant", "content": "Hello! I'm an AI assistant. How can I help you?"})
        if response.status_code != 200:
            print(f"❌ 发送AI回复失败: {response.status_code}")
            return False
        print("✅ 发送AI回复成功")
        
        # 4. 获取消息历史
        response = requests.get(f"{base_url}/conversations/{conv_id}/messages")
        if response.status_code != 200:
            print(f"❌ 获取消息历史失败: {response.status_code}")
            return False
        
        messages = response.json()
        if len(messages) >= 2:
            print(f"✅ 获取消息历史成功 ({len(messages)} 条消息)")
        else:
            print(f"❌ 消息数量不正确: {len(messages)}")
            return False
        
        # 5. 测试文件上传
        test_file_content = "This is a test file for integration testing."
        with open("/tmp/integration_test.txt", "w") as f:
            f.write(test_file_content)
        
        with open("/tmp/integration_test.txt", "rb") as f:
            files = {"file": ("integration_test.txt", f, "text/plain")}
            response = requests.post(f"{base_url}/upload", files=files)
        
        if response.status_code == 200:
            print("✅ 文件上传成功")
        else:
            print(f"❌ 文件上传失败: {response.status_code}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ 工作流程测试失败: {e}")
        return False

def check_services_status():
    """检查服务状态"""
    print("🔍 检查服务状态...")
    
    # 检查后端进程
    try:
        result = subprocess.run(['pgrep', '-f', 'python.*main.py'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ 后端进程运行中 (PID: {result.stdout.strip()})")
        else:
            print("❌ 后端进程未运行")
    except Exception as e:
        print(f"❌ 检查后端进程失败: {e}")
    
    # 检查前端进程
    try:
        result = subprocess.run(['pgrep', '-f', 'vite.*12000'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ 前端进程运行中 (PID: {result.stdout.strip()})")
        else:
            print("❌ 前端进程未运行")
    except Exception as e:
        print(f"❌ 检查前端进程失败: {e}")

def main():
    """主测试函数"""
    print("🚀 开始AI聊天应用集成测试")
    print("=" * 50)
    
    # 检查服务状态
    check_services_status()
    print()
    
    # 测试各个组件
    tests = [
        ("后端API", test_backend_api),
        ("前端服务", test_frontend_service),
        ("CORS配置", test_cors_headers),
        ("完整工作流程", test_complete_workflow)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"🧪 {test_name}测试...")
        result = test_func()
        results.append((test_name, result))
        print()
    
    # 汇总结果
    print("=" * 50)
    print("📊 测试结果汇总:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n总计: {passed}/{len(results)} 项测试通过")
    
    if passed == len(results):
        print("🎉 所有测试通过！聊天应用运行正常。")
        print("\n📱 访问地址:")
        print("  前端应用: http://localhost:12000")
        print("  后端API: http://localhost:8000/docs")
    else:
        print("⚠️  部分测试失败，请检查相关服务。")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)