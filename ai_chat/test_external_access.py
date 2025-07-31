#!/usr/bin/env python3
"""
测试外部访问的脚本
"""
import requests
import json

def test_external_frontend():
    """测试外部前端访问"""
    try:
        # 模拟外部访问
        headers = {
            'Host': 'work-1-zrjouldkqnbapmiu.prod-runtime.all-hands.dev',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get("http://localhost:12000", headers=headers, timeout=5)
        if response.status_code == 200:
            print("✅ 外部前端访问 - 正常")
            return True
        else:
            print(f"❌ 外部前端访问 - 状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 外部前端访问 - 失败: {e}")
        return False

def test_external_backend():
    """测试外部后端访问"""
    try:
        # 模拟外部访问
        headers = {
            'Host': 'work-2-zrjouldkqnbapmiu.prod-runtime.all-hands.dev',
            'Origin': 'https://work-1-zrjouldkqnbapmiu.prod-runtime.all-hands.dev'
        }
        response = requests.get("http://localhost:8000/api/conversations", headers=headers, timeout=5)
        if response.status_code == 200:
            print("✅ 外部后端访问 - 正常")
            return True
        else:
            print(f"❌ 外部后端访问 - 状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 外部后端访问 - 失败: {e}")
        return False

def main():
    print("🌐 外部访问测试")
    print("=" * 30)
    
    frontend_ok = test_external_frontend()
    backend_ok = test_external_backend()
    
    print("\n" + "=" * 30)
    if frontend_ok and backend_ok:
        print("🎉 外部访问配置正确！")
        print("\n现在可以通过以下地址访问:")
        print("https://work-1-zrjouldkqnbapmiu.prod-runtime.all-hands.dev")
    else:
        print("⚠️  外部访问可能存在问题")

if __name__ == "__main__":
    main()