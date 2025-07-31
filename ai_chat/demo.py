#!/usr/bin/env python3
"""
AI聊天应用演示脚本
展示完整的聊天功能
"""
import requests
import json
import time
import os

def print_header(title):
    print("\n" + "="*60)
    print(f"🎯 {title}")
    print("="*60)

def print_step(step, description):
    print(f"\n📍 步骤 {step}: {description}")

def demo_chat_application():
    """演示聊天应用的完整功能"""
    
    print_header("AI聊天应用功能演示")
    
    base_url = "http://localhost:8000/api"
    
    # 步骤1: 创建新对话
    print_step(1, "创建新对话")
    response = requests.post(f"{base_url}/conversations", 
                           json={"title": "AI助手演示对话"})
    
    if response.status_code == 200:
        conversation = response.json()
        conv_id = conversation['id']
        print(f"✅ 成功创建对话")
        print(f"   对话ID: {conv_id}")
        print(f"   对话标题: {conversation['title']}")
        print(f"   创建时间: {conversation['created_at']}")
    else:
        print(f"❌ 创建对话失败: {response.status_code}")
        return
    
    # 步骤2: 模拟用户提问
    print_step(2, "用户发送问题")
    user_message = "你好！请介绍一下你的功能。"
    response = requests.post(f"{base_url}/conversations/{conv_id}/messages",
                           json={"role": "user", "content": user_message})
    
    if response.status_code == 200:
        message = response.json()
        print(f"✅ 用户消息发送成功")
        print(f"   消息内容: {user_message}")
        print(f"   发送时间: {message['created_at']}")
    else:
        print(f"❌ 发送消息失败: {response.status_code}")
        return
    
    # 步骤3: AI回复
    print_step(3, "AI助手回复")
    ai_response = """你好！我是AI聊天助手，具有以下功能：

🤖 智能对话：可以进行自然语言交流
💬 多轮对话：支持上下文理解和连续对话
📁 文件处理：支持文件上传和内容分析
🗂️ 对话管理：可以创建、切换和管理多个对话
📝 消息历史：完整保存对话记录
🎨 友好界面：现代化的ChatGPT风格界面

有什么我可以帮助您的吗？"""
    
    response = requests.post(f"{base_url}/conversations/{conv_id}/messages",
                           json={"role": "assistant", "content": ai_response})
    
    if response.status_code == 200:
        message = response.json()
        print(f"✅ AI回复发送成功")
        print(f"   回复内容: {ai_response[:100]}...")
        print(f"   回复时间: {message['created_at']}")
    else:
        print(f"❌ AI回复失败: {response.status_code}")
        return
    
    # 步骤4: 继续对话
    print_step(4, "继续多轮对话")
    follow_up_messages = [
        ("user", "能帮我分析一下上传的文件吗？"),
        ("assistant", "当然可以！请上传您需要分析的文件，我会帮您进行内容分析和总结。支持多种文件格式，包括文本、文档等。"),
        ("user", "太好了！这个聊天应用的界面很漂亮。"),
        ("assistant", "谢谢您的夸奖！这个应用采用了现代化的设计，参考了ChatGPT的界面风格，力求提供最佳的用户体验。界面支持响应式设计，在桌面和移动设备上都能完美显示。")
    ]
    
    for role, content in follow_up_messages:
        response = requests.post(f"{base_url}/conversations/{conv_id}/messages",
                               json={"role": role, "content": content})
        if response.status_code == 200:
            print(f"✅ [{role}] 消息发送成功")
        else:
            print(f"❌ [{role}] 消息发送失败")
        time.sleep(0.5)  # 模拟真实对话间隔
    
    # 步骤5: 查看对话历史
    print_step(5, "查看完整对话历史")
    response = requests.get(f"{base_url}/conversations/{conv_id}/messages")
    
    if response.status_code == 200:
        messages = response.json()
        print(f"✅ 成功获取对话历史 ({len(messages)} 条消息)")
        print("\n📜 对话记录:")
        print("-" * 50)
        
        for i, msg in enumerate(messages, 1):
            role_icon = "👤" if msg['role'] == 'user' else "🤖"
            role_name = "用户" if msg['role'] == 'user' else "AI助手"
            print(f"\n{i}. {role_icon} {role_name} ({msg['created_at']})")
            print(f"   {msg['content']}")
    else:
        print(f"❌ 获取对话历史失败: {response.status_code}")
        return
    
    # 步骤6: 文件上传演示
    print_step(6, "文件上传功能演示")
    
    # 创建演示文件
    demo_content = """这是一个演示文件
用于测试AI聊天应用的文件上传功能

文件内容包括：
- 文本内容分析
- 文件格式支持
- 上传状态反馈
- 文件信息存储

AI助手可以分析此文件并提供相关建议。"""
    
    demo_file_path = "/tmp/demo_file.txt"
    with open(demo_file_path, "w", encoding="utf-8") as f:
        f.write(demo_content)
    
    # 上传文件
    with open(demo_file_path, "rb") as f:
        files = {"file": ("demo_file.txt", f, "text/plain")}
        data = {"conversation_id": conv_id}
        response = requests.post(f"{base_url}/upload", files=files, data=data)
    
    if response.status_code == 200:
        file_info = response.json()
        print(f"✅ 文件上传成功")
        print(f"   原始文件名: {file_info['original_filename']}")
        print(f"   存储文件名: {file_info['filename']}")
        print(f"   文件大小: {file_info['file_size']} 字节")
    else:
        print(f"❌ 文件上传失败: {response.status_code}")
    
    # 步骤7: 获取所有对话列表
    print_step(7, "查看所有对话")
    response = requests.get(f"{base_url}/conversations")
    
    if response.status_code == 200:
        conversations = response.json()
        print(f"✅ 成功获取对话列表 ({len(conversations)} 个对话)")
        print("\n📋 对话列表:")
        print("-" * 50)
        
        for conv in conversations[:5]:  # 显示前5个对话
            print(f"🗨️  ID: {conv['id']} | 标题: {conv['title']}")
            print(f"    创建时间: {conv['created_at']}")
            print(f"    更新时间: {conv['updated_at']}")
            print()
    else:
        print(f"❌ 获取对话列表失败: {response.status_code}")
    
    # 演示总结
    print_header("演示完成")
    print("🎉 AI聊天应用功能演示成功完成！")
    print("\n✨ 演示的功能包括:")
    print("   ✅ 创建新对话")
    print("   ✅ 发送用户消息")
    print("   ✅ 接收AI回复")
    print("   ✅ 多轮对话交互")
    print("   ✅ 查看对话历史")
    print("   ✅ 文件上传功能")
    print("   ✅ 对话列表管理")
    
    print(f"\n🌐 访问地址:")
    print(f"   前端应用: http://localhost:12000")
    print(f"   API文档: http://localhost:8000/docs")
    
    print(f"\n📊 当前数据统计:")
    print(f"   总对话数: {len(conversations)}")
    print(f"   本次演示消息数: {len(messages)}")
    print(f"   上传文件数: 1")

if __name__ == "__main__":
    try:
        demo_chat_application()
    except KeyboardInterrupt:
        print("\n\n⏹️  演示被用户中断")
    except Exception as e:
        print(f"\n❌ 演示过程中出现错误: {e}")