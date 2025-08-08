#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库管理器
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from contextlib import contextmanager
from config.config import Config

class DatabaseManager:
    """数据库管理器类"""
    
    def __init__(self):
        self.db_path = Config.DATABASE_PATH
        self._ensure_data_dir()
    
    def _ensure_data_dir(self):
        """确保数据目录存在"""
        data_dir = os.path.dirname(self.db_path)
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    @contextmanager
    def get_connection(self):
        """获取数据库连接的上下文管理器"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # 使查询结果可以通过列名访问
        try:
            yield conn
        finally:
            conn.close()
    
    def init_database(self):
        """初始化数据库表"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # 创建对话表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 创建消息表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id INTEGER NOT NULL,
                    role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
                    content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (conversation_id) REFERENCES conversations (id) ON DELETE CASCADE
                )
            ''')
            
            # 创建文件表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS uploaded_files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL,
                    original_filename TEXT NOT NULL,
                    file_size INTEGER NOT NULL,
                    file_path TEXT NOT NULL,
                    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
    
    def create_conversation(self, title: str = None) -> int:
        """创建新对话"""
        if not title:
            title = f"新对话 {datetime.now().strftime('%m-%d %H:%M')}"
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO conversations (title) VALUES (?)',
                (title,)
            )
            conn.commit()
            return cursor.lastrowid
    
    def get_conversations(self) -> List[Dict]:
        """获取所有对话列表"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, title, created_at, updated_at 
                FROM conversations 
                ORDER BY updated_at DESC
            ''')
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def get_conversation(self, conversation_id: int) -> Optional[Dict]:
        """获取单个对话信息"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT id, title, created_at, updated_at FROM conversations WHERE id = ?',
                (conversation_id,)
            )
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def update_conversation_title(self, conversation_id: int, title: str) -> bool:
        """更新对话标题"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE conversations SET title = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
                (title, conversation_id)
            )
            conn.commit()
            return cursor.rowcount > 0
    
    def delete_conversation(self, conversation_id: int) -> bool:
        """删除对话"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM conversations WHERE id = ?', (conversation_id,))
            conn.commit()
            return cursor.rowcount > 0
    
    def add_message(self, conversation_id: int, role: str, content: str) -> int:
        """添加消息"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)',
                (conversation_id, role, content)
            )
            # 更新对话的更新时间
            cursor.execute(
                'UPDATE conversations SET updated_at = CURRENT_TIMESTAMP WHERE id = ?',
                (conversation_id,)
            )
            conn.commit()
            return cursor.lastrowid
    
    def get_messages(self, conversation_id: int) -> List[Dict]:
        """获取对话的所有消息"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, conversation_id, role, content, created_at 
                FROM messages 
                WHERE conversation_id = ? 
                ORDER BY created_at ASC
            ''', (conversation_id,))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def save_uploaded_file(self, filename: str, original_filename: str, file_size: int, file_path: str) -> int:
        """保存上传文件信息"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO uploaded_files (filename, original_filename, file_size, file_path) 
                VALUES (?, ?, ?, ?)
            ''', (filename, original_filename, file_size, file_path))
            conn.commit()
            return cursor.lastrowid
    
    def get_uploaded_files(self) -> List[Dict]:
        """获取所有上传文件信息"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, filename, original_filename, file_size, file_path, uploaded_at 
                FROM uploaded_files 
                ORDER BY uploaded_at DESC
            ''')
            rows = cursor.fetchall()
            return [dict(row) for row in rows]