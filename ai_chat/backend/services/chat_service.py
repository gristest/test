#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
聊天服务
"""

import random
import time
from typing import List, Dict, Optional
from database.db_manager import DatabaseManager

class ChatService:
    """聊天服务类"""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
    
    def create_conversation(self, title: str = None) -> Dict:
        """创建新对话"""
        conversation_id = self.db_manager.create_conversation(title)
        return self.db_manager.get_conversation(conversation_id)
    
    def get_conversations(self) -> List[Dict]:
        """获取对话列表"""
        return self.db_manager.get_conversations()
    
    def get_conversation(self, conversation_id: int) -> Optional[Dict]:
        """获取对话信息"""
        return self.db_manager.get_conversation(conversation_id)
    
    def update_conversation_title(self, conversation_id: int, title: str) -> bool:
        """更新对话标题"""
        return self.db_manager.update_conversation_title(conversation_id, title)
    
    def delete_conversation(self, conversation_id: int) -> bool:
        """删除对话"""
        return self.db_manager.delete_conversation(conversation_id)
    
    def get_messages(self, conversation_id: int) -> List[Dict]:
        """获取对话消息"""
        return self.db_manager.get_messages(conversation_id)
    
    def send_message(self, conversation_id: int, content: str) -> Dict:
        """发送消息并获取AI回复"""
        # 保存用户消息
        user_message_id = self.db_manager.add_message(conversation_id, 'user', content)
        
        # 模拟AI回复（实际项目中这里会调用LLM API）
        ai_response = self._generate_ai_response(content)
        
        # 保存AI回复
        ai_message_id = self.db_manager.add_message(conversation_id, 'assistant', ai_response)
        
        return {
            'user_message': {
                'id': user_message_id,
                'role': 'user',
                'content': content
            },
            'ai_message': {
                'id': ai_message_id,
                'role': 'assistant',
                'content': ai_response
            }
        }
    
    def _generate_ai_response(self, user_message: str) -> str:
        """生成AI回复（模拟）"""
        # 这里是模拟的AI回复，实际项目中应该调用真实的LLM API
        responses = [
            f"我理解您说的是：{user_message}。这是一个很有趣的话题。",
            f"关于您提到的「{user_message}」，我认为这需要更深入的思考。",
            f"您的问题很好：{user_message}。让我为您详细解答一下。",
            f"感谢您的提问：{user_message}。这确实是一个值得探讨的问题。",
            f"针对您说的「{user_message}」，我有以下几点看法...",
        ]
        
        # 模拟思考时间
        time.sleep(0.5)
        
        return random.choice(responses)
    
    def add_message(self, conversation_id: int, role: str, content: str) -> int:
        """直接添加消息"""
        return self.db_manager.add_message(conversation_id, role, content)