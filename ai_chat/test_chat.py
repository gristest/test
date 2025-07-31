#!/usr/bin/env python3
"""
测试聊天应用的完整功能
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000/api"

def test_api():
    print("🚀 开始测试聊天应用API...")
    
    # 1. 测试创建对话
    print("\n1. 测试创建对话...")
    response = requests.post(f"{BASE_URL}/conversations", 
                           json={"title": "测试对话"})
    if response.status_code == 200:
        conversation = response.json()
        print(f"✅ 创建对话成功: {conversation}")
        conversation_id = conversation['id']
    else:
        print(f"❌ 创建对话失败: {response.status_code}")
        return
    
    # 2. 测试发送消息
    print("\n2. 测试发送用户消息...")
    response = requests.post(f"{BASE_URL}/conversations/{conversation_id}/messages",
                           json={"content": "你好，这是一条测试消息", "role": "user"})
    if response.status_code == 200:
        message = response.json()
        print(f"✅ 发送消息成功: {message}")
    else:
        print(f"❌ 发送消息失败: {response.status_code}")
        return
    
    # 3. 测试发送AI回复
    print("\n3. 测试发送AI回复...")
    response = requests.post(f"{BASE_URL}/conversations/{conversation_id}/messages",
                           json={"content": "你好！我是AI助手，很高兴为您服务。", "role": "assistant"})
    if response.status_code == 200:
        message = response.json()
        print(f"✅ AI回复成功: {message}")
    else:
        print(f"❌ AI回复失败: {response.status_code}")
        return
    
    # 4. 测试获取对话列表
    print("\n4. 测试获取对话列表...")
    response = requests.get(f"{BASE_URL}/conversations")
    if response.status_code == 200:
        conversations = response.json()
        print(f"✅ 获取对话列表成功: {len(conversations)} 个对话")
        for conv in conversations:
            print(f"   - {conv['title']} (ID: {conv['id']})")
    else:
        print(f"❌ 获取对话列表失败: {response.status_code}")
        return
    
    # 5. 测试获取消息历史
    print("\n5. 测试获取消息历史...")
    response = requests.get(f"{BASE_URL}/conversations/{conversation_id}/messages")
    if response.status_code == 200:
        messages = response.json()
        print(f"✅ 获取消息历史成功: {len(messages)} 条消息")
        for msg in messages:
            print(f"   - [{msg['role']}] {msg['content'][:50]}...")
    else:
        print(f"❌ 获取消息历史失败: {response.status_code}")
        return
    
    # 6. 测试文件上传
    print("\n6. 测试文件上传...")
    # 创建一个测试文件
    test_content = "这是一个测试文件内容\n用于测试文件上传功能"
    with open("/tmp/test_file.txt", "w", encoding="utf-8") as f:
        f.write(test_content)
    
    with open("/tmp/test_file.txt", "rb") as f:
        files = {"file": ("test_file.txt", f, "text/plain")}
        data = {"conversation_id": conversation_id}
        response = requests.post(f"{BASE_URL}/upload", files=files, data=data)
    
    if response.status_code == 200:
        file_info = response.json()
        print(f"✅ 文件上传成功: {file_info}")
    else:
        print(f"❌ 文件上传失败: {response.status_code}")
        print(f"错误信息: {response.text}")
    
    print("\n🎉 API测试完成！")

if __name__ == "__main__":
    test_api()