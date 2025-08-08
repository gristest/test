#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对话模型
"""

from datetime import datetime
from typing import List, Dict, Optional

class Conversation:
    """对话模型类"""
    
    def __init__(self, id: int = None, title: str = None, created_at: datetime = None, updated_at: datetime = None):
        self.id = id
        self.title = title or f"新对话 {datetime.now().strftime('%m-%d %H:%M')}"
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> Dict:
        """转换为字典格式"""
        return {
            'id': self.id,
            'title': self.title,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Conversation':
        """从字典创建对象"""
        return cls(
            id=data.get('id'),
            title=data.get('title'),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None,
            updated_at=datetime.fromisoformat(data['updated_at']) if data.get('updated_at') else None
        )

class Message:
    """消息模型类"""
    
    def __init__(self, id: int = None, conversation_id: int = None, role: str = None, 
                 content: str = None, created_at: datetime = None):
        self.id = id
        self.conversation_id = conversation_id
        self.role = role  # 'user' 或 'assistant'
        self.content = content
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> Dict:
        """转换为字典格式"""
        return {
            'id': self.id,
            'conversation_id': self.conversation_id,
            'role': self.role,
            'content': self.content,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Message':
        """从字典创建对象"""
        return cls(
            id=data.get('id'),
            conversation_id=data.get('conversation_id'),
            role=data.get('role'),
            content=data.get('content'),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None
        )