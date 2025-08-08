#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API接口测试脚本
"""

import requests
import json
import os
import time
from datetime import datetime

class APITester:
    def __init__(self, base_url='http://localhost:58726/api'):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
    
    def log_test(self, test_name, success, message, response_data=None):
        """记录测试结果"""
        result = {
            'test_name': test_name,
            'success': success,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'response_data': response_data
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        if response_data and not success:
            print(f"   Response: {response_data}")
    
    def test_health_check(self):
        """测试健康检查接口"""
        try:
            response = self.session.get(f"{self.base_url}/health")
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'ok':
                    self.log_test("健康检查", True, "API服务正常运行")
                    return True
                else:
                    self.log_test("健康检查", False, "API响应状态异常", data)
            else:
                self.log_test("健康检查", False, f"HTTP状态码: {response.status_code}")
        except Exception as e:
            self.log_test("健康检查", False, f"请求失败: {str(e)}")
        return False
    
    def test_create_conversation(self):
        """测试创建对话接口"""
        try:
            # 测试创建默认标题的对话
            response = self.session.post(
                f"{self.base_url}/conversations",
                headers={'Content-Type': 'application/json'},
                json={}
            )

            
            if response.status_code == 201:
                data = response.json()
                if data.get('success') and 'data' in data:
                    conversation_id = data['data']['id']
                    self.log_test("创建对话(默认标题)", True, f"成功创建对话，ID: {conversation_id}")
                    
                    # 测试创建自定义标题的对话
                    custom_title = "测试对话标题"
                    response2 = self.session.post(
                        f"{self.base_url}/conversations",
                        json={'title': custom_title}
                    )
                    if response2.status_code == 201:
                        data2 = response2.json()
                        if data2.get('success') and data2['data']['title'] == custom_title:
                            self.log_test("创建对话(自定义标题)", True, f"成功创建自定义标题对话")
                            return data['data']['id'], data2['data']['id']
                        else:
                            self.log_test("创建对话(自定义标题)", False, "标题设置失败", data2)
                    else:
                        self.log_test("创建对话(自定义标题)", False, f"HTTP状态码: {response2.status_code}")
                else:
                    self.log_test("创建对话(默认标题)", False, "响应格式错误", data)
            else:
                self.log_test("创建对话(默认标题)", False, f"HTTP状态码: {response.status_code}, 响应: {response.text}")
        except Exception as e:
            self.log_test("创建对话", False, f"请求失败: {str(e)}")
        return None, None
    
    def test_get_conversations(self):
        """测试获取对话列表接口"""
        try:
            response = self.session.get(f"{self.base_url}/conversations")
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and isinstance(data.get('data'), list):
                    count = len(data['data'])
                    self.log_test("获取对话列表", True, f"成功获取 {count} 个对话")
                    return True
                else:
                    self.log_test("获取对话列表", False, "响应格式错误", data)
            else:
                self.log_test("获取对话列表", False, f"HTTP状态码: {response.status_code}")
        except Exception as e:
            self.log_test("获取对话列表", False, f"请求失败: {str(e)}")
        return False
    
    def test_conversation_operations(self, conversation_id):
        """测试对话操作接口"""
        if not conversation_id:
            self.log_test("对话操作测试", False, "没有有效的对话ID")
            return False
        
        # 测试获取单个对话
        try:
            response = self.session.get(f"{self.base_url}/conversations/{conversation_id}")
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and data['data']['id'] == conversation_id:
                    self.log_test("获取单个对话", True, f"成功获取对话 {conversation_id}")
                else:
                    self.log_test("获取单个对话", False, "响应数据错误", data)
                    return False
            else:
                self.log_test("获取单个对话", False, f"HTTP状态码: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("获取单个对话", False, f"请求失败: {str(e)}")
            return False
        
        # 测试更新对话标题
        try:
            new_title = f"更新后的标题 {int(time.time())}"
            response = self.session.put(
                f"{self.base_url}/conversations/{conversation_id}",
                json={'title': new_title}
            )
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    self.log_test("更新对话标题", True, f"成功更新标题为: {new_title}")
                else:
                    self.log_test("更新对话标题", False, "更新失败", data)
                    return False
            else:
                self.log_test("更新对话标题", False, f"HTTP状态码: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("更新对话标题", False, f"请求失败: {str(e)}")
            return False
        
        return True
    
    def test_message_operations(self, conversation_id):
        """测试消息操作接口"""
        if not conversation_id:
            self.log_test("消息操作测试", False, "没有有效的对话ID")
            return False
        
        # 测试发送消息
        try:
            test_message = "这是一条测试消息"
            response = self.session.post(
                f"{self.base_url}/conversations/{conversation_id}/messages",
                json={'content': test_message}
            )
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and 'data' in data:
                    user_msg = data['data'].get('user_message')
                    ai_msg = data['data'].get('ai_message')
                    if user_msg and ai_msg:
                        self.log_test("发送消息", True, f"成功发送消息并获得AI回复")
                    else:
                        self.log_test("发送消息", False, "消息格式错误", data)
                        return False
                else:
                    self.log_test("发送消息", False, "响应格式错误", data)
                    return False
            else:
                self.log_test("发送消息", False, f"HTTP状态码: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("发送消息", False, f"请求失败: {str(e)}")
            return False
        
        # 测试获取消息列表
        try:
            response = self.session.get(f"{self.base_url}/conversations/{conversation_id}/messages")
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and isinstance(data.get('data'), list):
                    message_count = len(data['data'])
                    self.log_test("获取消息列表", True, f"成功获取 {message_count} 条消息")
                    return True
                else:
                    self.log_test("获取消息列表", False, "响应格式错误", data)
            else:
                self.log_test("获取消息列表", False, f"HTTP状态码: {response.status_code}")
        except Exception as e:
            self.log_test("获取消息列表", False, f"请求失败: {str(e)}")
        return False
    
    def test_file_upload(self):
        """测试文件上传接口"""
        try:
            # 创建一个测试文件
            test_content = "这是一个测试文件内容\n用于测试文件上传功能"
            test_filename = "test_upload.txt"
            
            # 模拟文件上传
            files = {
                'file': (test_filename, test_content, 'text/plain')
            }
            
            response = self.session.post(f"{self.base_url}/upload", files=files)
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and 'data' in data:
                    file_info = data['data']
                    self.log_test("文件上传", True, f"成功上传文件: {file_info.get('original_filename')}")
                    return True
                else:
                    self.log_test("文件上传", False, "响应格式错误", data)
            else:
                self.log_test("文件上传", False, f"HTTP状态码: {response.status_code}")
        except Exception as e:
            self.log_test("文件上传", False, f"请求失败: {str(e)}")
        return False
    
    def test_get_files(self):
        """测试获取文件列表接口"""
        try:
            response = self.session.get(f"{self.base_url}/files")
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and isinstance(data.get('data'), list):
                    file_count = len(data['data'])
                    self.log_test("获取文件列表", True, f"成功获取 {file_count} 个文件")
                    return True
                else:
                    self.log_test("获取文件列表", False, "响应格式错误", data)
            else:
                self.log_test("获取文件列表", False, f"HTTP状态码: {response.status_code}")
        except Exception as e:
            self.log_test("获取文件列表", False, f"请求失败: {str(e)}")
        return False
    
    def test_delete_conversation(self, conversation_id):
        """测试删除对话接口"""
        if not conversation_id:
            return True  # 没有对话ID，跳过测试
        
        try:
            response = self.session.delete(f"{self.base_url}/conversations/{conversation_id}")
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    self.log_test("删除对话", True, f"成功删除对话 {conversation_id}")
                    return True
                else:
                    self.log_test("删除对话", False, "删除失败", data)
            else:
                self.log_test("删除对话", False, f"HTTP状态码: {response.status_code}")
        except Exception as e:
            self.log_test("删除对话", False, f"请求失败: {str(e)}")
        return False
    
    def run_all_tests(self):
        """运行所有测试"""
        print("=" * 60)
        print("开始API接口测试")
        print("=" * 60)
        
        # 1. 健康检查
        if not self.test_health_check():
            print("❌ API服务未启动，请先启动后端服务")
            return False
        
        # 2. 创建对话
        conv_id1, conv_id2 = self.test_create_conversation()
        
        # 3. 获取对话列表
        self.test_get_conversations()
        
        # 4. 对话操作测试
        self.test_conversation_operations(conv_id1)
        
        # 5. 消息操作测试
        self.test_message_operations(conv_id1)
        
        # 6. 文件上传测试
        self.test_file_upload()
        
        # 7. 获取文件列表
        self.test_get_files()
        
        # 8. 清理测试数据
        self.test_delete_conversation(conv_id1)
        self.test_delete_conversation(conv_id2)
        
        # 输出测试结果统计
        self.print_test_summary()
        
        return True
    
    def print_test_summary(self):
        """打印测试结果摘要"""
        print("\n" + "=" * 60)
        print("测试结果摘要")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"总测试数: {total_tests}")
        print(f"通过: {passed_tests}")
        print(f"失败: {failed_tests}")
        print(f"成功率: {(passed_tests/total_tests*100):.1f}%")
        
        if failed_tests > 0:
            print("\n失败的测试:")
            for result in self.test_results:
                if not result['success']:
                    print(f"  - {result['test_name']}: {result['message']}")
        
        print("=" * 60)

def main():
    """主函数"""
    print("AI Chat API 测试工具")
    print("确保后端服务已启动在 http://localhost:58726")
    print()
    
    tester = APITester()
    tester.run_all_tests()

if __name__ == '__main__':
    main()