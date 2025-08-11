#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API路由
"""

from flask import Blueprint, request, jsonify, send_file
from werkzeug.exceptions import RequestEntityTooLarge
from services.chat_service import ChatService
from services.file_service import FileService
import os

api_bp = Blueprint('api', __name__)

# 初始化服务
chat_service = ChatService()
file_service = FileService()

@api_bp.route('/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({'status': 'ok', 'message': 'AI Chat API is running'})

# 对话相关API
@api_bp.route('/conversations', methods=['GET'])
def get_conversations():
    """获取对话列表"""
    try:
        conversations = chat_service.get_conversations()
        return jsonify({
            'success': True,
            'data': conversations
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/conversations', methods=['POST'])
def create_conversation():
    """创建新对话"""
    try:
        data = request.get_json() or {}
        title = data.get('title')
        
        conversation = chat_service.create_conversation(title)
        return jsonify({
            'success': True,
            'data': conversation
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/conversations/<int:conversation_id>', methods=['GET'])
def get_conversation(conversation_id):
    """获取对话信息"""
    try:
        conversation = chat_service.get_conversation(conversation_id)
        if not conversation:
            return jsonify({
                'success': False,
                'error': '对话不存在'
            }), 404
        
        return jsonify({
            'success': True,
            'data': conversation
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/conversations/<int:conversation_id>', methods=['PUT'])
def update_conversation(conversation_id):
    """更新对话标题"""
    try:
        data = request.get_json()
        if not data or 'title' not in data:
            return jsonify({
                'success': False,
                'error': '缺少标题参数'
            }), 400
        
        success = chat_service.update_conversation_title(conversation_id, data['title'])
        if not success:
            return jsonify({
                'success': False,
                'error': '对话不存在'
            }), 404
        
        return jsonify({
            'success': True,
            'message': '标题更新成功'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/conversations/<int:conversation_id>', methods=['DELETE'])
def delete_conversation(conversation_id):
    """删除对话"""
    try:
        success = chat_service.delete_conversation(conversation_id)
        if not success:
            return jsonify({
                'success': False,
                'error': '对话不存在'
            }), 404
        
        return jsonify({
            'success': True,
            'message': '对话删除成功'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# 消息相关API
@api_bp.route('/conversations/<int:conversation_id>/messages', methods=['GET'])
def get_messages(conversation_id):
    """获取对话消息"""
    try:
        messages = chat_service.get_messages(conversation_id)
        return jsonify({
            'success': True,
            'data': messages
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/conversations/<int:conversation_id>/messages', methods=['POST'])
def send_message(conversation_id):
    """发送消息"""
    try:
        data = request.get_json()
        if not data or 'content' not in data:
            return jsonify({
                'success': False,
                'error': '缺少消息内容'
            }), 400
        
        content = data['content'].strip()
        if not content:
            return jsonify({
                'success': False,
                'error': '消息内容不能为空'
            }), 400
        
        # 检查对话是否存在
        conversation = chat_service.get_conversation(conversation_id)
        if not conversation:
            return jsonify({
                'success': False,
                'error': '对话不存在'
            }), 404
        
        result = chat_service.send_message(conversation_id, content)
        return jsonify({
            'success': True,
            'data': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# 文件上传相关API
@api_bp.route('/upload', methods=['POST'])
def upload_file():
    """上传文件"""
    try:        
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': '没有文件'
            }), 400
        
        file = request.files['file']
        result = file_service.upload_file(file)
        
        return jsonify({
            'success': True,
            'data': result,
            'message': '文件上传成功'
        })
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except RequestEntityTooLarge:
        return jsonify({
            'success': False,
            'error': '文件大小超过限制'
        }), 413
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'上传失败：{str(e)}'
        }), 500

@api_bp.route('/files', methods=['GET'])
def get_uploaded_files():
    """获取上传文件列表"""
    try:
        files = file_service.get_uploaded_files()
        # 格式化文件大小
        for file_info in files:
            file_info['formatted_size'] = file_service.format_file_size(file_info['file_size'])
        
        return jsonify({
            'success': True,
            'data': files
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/files/<filename>', methods=['GET'])
def download_file(filename):
    """下载文件"""
    try:
        file_path = file_service.get_file_path(filename)
        if not file_path:
            return jsonify({
                'success': False,
                'error': '文件不存在'
            }), 404
        
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# 错误处理
@api_bp.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': '接口不存在'
    }), 404

@api_bp.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'success': False,
        'error': '请求方法不允许'
    }), 405

@api_bp.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': '服务器内部错误'
    }), 500