#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件服务
"""

import os
import uuid
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from typing import Dict, List, Optional, Tuple
from config.config import Config
from database.db_manager import DatabaseManager

class FileService:
    """文件服务类"""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.upload_folder = Config.UPLOAD_FOLDER
        self.allowed_extensions = Config.ALLOWED_EXTENSIONS
        self.max_file_size = Config.MAX_CONTENT_LENGTH
    
    def allowed_file(self, filename: str) -> bool:
        """检查文件扩展名是否允许"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.allowed_extensions
    
    def upload_file(self, file: FileStorage) -> Dict:        
        """上传文件"""
        if not file or file.filename == '':
            raise ValueError("没有选择文件")
        
        if not self.allowed_file(file.filename):
            raise ValueError(f"不支持的文件类型。支持的类型：{', '.join(self.allowed_extensions)}")
        
        # 生成唯一文件名
        # by zhb: 
        # #original_filename = secure_filename(file.filename)
        original_filename = file.filename
        file_extension = original_filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{file_extension}"
        
        # 确保上传目录存在
        if not os.path.exists(self.upload_folder):
            os.makedirs(self.upload_folder)
        
        # 保存文件
        file_path = os.path.join(self.upload_folder, unique_filename)
        file.save(file_path)
        
        # 获取文件大小
        file_size = os.path.getsize(file_path)
        
        # 检查文件大小
        if file_size > self.max_file_size:
            os.remove(file_path)  # 删除已保存的文件
            raise ValueError(f"文件大小超过限制（{self.max_file_size // (1024*1024)}MB）")
        
        # 保存文件信息到数据库
        file_id = self.db_manager.save_uploaded_file(
            filename=unique_filename,
            original_filename=original_filename,
            file_size=file_size,
            file_path=file_path
        )
        
        return {
            'id': file_id,
            'filename': unique_filename,
            'original_filename': original_filename,
            'file_size': file_size,
            'file_path': file_path
        }
    
    def get_uploaded_files(self) -> List[Dict]:
        """获取所有上传文件信息"""
        return self.db_manager.get_uploaded_files()
    
    def get_file_path(self, filename: str) -> Optional[str]:
        """获取文件的完整路径"""
        file_path = os.path.join(self.upload_folder, filename)
        if os.path.exists(file_path):
            return file_path
        return None
    
    def delete_file(self, filename: str) -> bool:
        """删除文件"""
        file_path = os.path.join(self.upload_folder, filename)
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
        except Exception:
            pass
        return False
    
    def format_file_size(self, size_bytes: int) -> str:
        """格式化文件大小"""
        if size_bytes == 0:
            return "0B"
        
        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f}{size_names[i]}"