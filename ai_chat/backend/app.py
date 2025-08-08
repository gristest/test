#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Chat Backend Application
主应用程序入口
"""

from flask import Flask
from flask_cors import CORS
from config.config import Config
from database.db_manager import DatabaseManager
from api.routes import api_bp
import os

def create_app():
    """创建Flask应用实例"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 启用CORS支持
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # 初始化数据库
    db_manager = DatabaseManager()
    db_manager.init_database()
    
    # 注册API蓝图
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # 创建上传目录
    upload_dir = app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )