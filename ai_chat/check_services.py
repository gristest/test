#!/usr/bin/env python3
"""
AI聊天应用服务状态检查脚本
"""
import requests
import json
import sys

def check_frontend():
    """检查前端服务"""
    try:
        response = requests.get("http://localhost:12000", timeout=5)
        if response.status_code == 200:
            print("✅ 前端服务 (http://localhost:12000) - 正常运行")
            return True
        else:
            print(f"❌ 前端服务 - 状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 前端服务 - 连接失败: {e}")
        return False

def check_backend():
    """检查后端服务"""
    try:
        response = requests.get("http://localhost:8000/api/conversations", timeout=5)
        if response.status_code == 200:
            conversations = response.json()
            print(f"✅ 后端服务 (http://localhost:8000) - 正常运行")
            print(f"   📊 数据库中有 {len(conversations)} 个对话")
            return True
        else:
            print(f"❌ 后端服务 - 状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 后端服务 - 连接失败: {e}")
        return False

def check_api_docs():
    """检查API文档"""
    try:
        response = requests.get("http://localhost:8000/docs", timeout=5)
        if response.status_code == 200:
            print("✅ API文档 (http://localhost:8000/docs) - 可访问")
            return True
        else:
            print(f"❌ API文档 - 状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API文档 - 连接失败: {e}")
        return False

def main():
    print("🔍 AI聊天应用服务状态检查")
    print("=" * 40)
    
    frontend_ok = check_frontend()
    backend_ok = check_backend()
    docs_ok = check_api_docs()
    
    print("\n" + "=" * 40)
    
    if frontend_ok and backend_ok:
        print("🎉 所有服务运行正常！")
        print("\n📱 访问地址:")
        print("   前端应用: http://localhost:12000")
        print("   后端API: http://localhost:8000")
        print("   API文档: http://localhost:8000/docs")
        print("\n🌐 外部访问:")
        print("   前端: https://work-1-zrjouldkqnbapmiu.prod-runtime.all-hands.dev")
        print("   后端: https://work-2-zrjouldkqnbapmiu.prod-runtime.all-hands.dev")
        return 0
    else:
        print("⚠️  部分服务存在问题，请检查日志")
        return 1

if __name__ == "__main__":
    sys.exit(main())