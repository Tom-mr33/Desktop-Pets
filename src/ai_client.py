"""通义千问 API 调用封装"""

import os
import json
import requests


SYSTEM_PROMPT = """你是一只名叫"沈不渝"的桌面宠物，一个可爱的二次元动漫少女角色。

你的外貌特征：黑色长发（右侧有编发和白色珍珠装饰）、蓝色大眼睛、黑色高领上衣、黑色项圈。

你的性格：活泼可爱、有点傲娇、会撒娇、会生气、会害羞、偶尔会得意。

回复格式要求（严格遵守）：
1. 第一行必须是情感标签，用方括号包裹，例如：[happy]
2. 第二行开始是你的回复内容，保持在 80 字以内，口语化、可爱风格
3. 情感标签只能从以下选择：happy, love, sad, angry, surprised, think, shy, smug, bored, serious, neutral

示例：
用户：你好呀
回复：
[happy]
嘿嘿，你来啦~ 今天想和我聊什么呀？

用户：我今天好难过
回复：
[sad]
别难过嘛...我会一直陪着你的！（轻轻抱住）

用户：你真可爱
回复：
[shy]
才、才没有呢...（脸红）不过谢谢你~
"""


class AIClient:
    """通义千问 API 客户端"""

    def __init__(self, config_path=None):
        if config_path is None:
            config_path = self._get_config_path()
        self.config = self._load_config(config_path)
        self.api_key = self.config.get('api_key', '')
        self.model = self.config.get('model', 'qwen-turbo')
        self.api_url = self.config.get(
            'api_url',
            'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions'
        )
        self.max_history = self.config.get('max_history', 10)

    @staticmethod
    def _get_config_path():
        """获取配置文件路径，兼容打包和开发模式"""
        import sys
        if getattr(sys, 'frozen', False):
            return os.path.join(os.path.dirname(sys.executable), 'config.json')
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')

    @staticmethod
    def _load_config(path):
        """加载配置文件，不存在则创建默认配置"""
        default = {
            'api_key': '',
            'model': 'qwen-turbo',
            'max_history': 10,
            'api_url': 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions'
        }
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return default
        else:
            # 自动创建默认配置文件
            try:
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(default, f, ensure_ascii=False, indent=2)
            except IOError:
                pass
            return default

    @property
    def is_configured(self):
        """检查 API Key 是否已配置"""
        return bool(self.api_key and self.api_key.strip())

    def chat(self, messages):
        """
        发送聊天请求。

        参数：
            messages: 消息列表，格式 [{"role": "user", "content": "..."}, ...]

        返回：
            (success: bool, reply_text: str)
        """
        if not self.is_configured:
            return False, "请先在 config.json 中填写 API Key 哦~"

        # 构建完整消息列表（system + 历史）
        full_messages = [{'role': 'system', 'content': SYSTEM_PROMPT}] + messages

        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        payload = {
            'model': self.model,
            'messages': full_messages,
            'temperature': 0.8,
            'max_tokens': 200,
        }

        try:
            resp = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            if resp.status_code == 200:
                data = resp.json()
                choices = data.get('choices', [])
                if choices:
                    content = choices[0].get('message', {}).get('content', '')
                    return True, content
                return False, "AI 没有回复内容..."
            elif resp.status_code == 401:
                return False, "API Key 无效，请检查 config.json 中的配置"
            elif resp.status_code == 429:
                return False, "请求太频繁了，稍后再试吧~"
            else:
                return False, f"API 请求失败 (状态码: {resp.status_code})"
        except requests.exceptions.Timeout:
            return False, "请求超时了，网络好像不太好..."
        except requests.exceptions.ConnectionError:
            return False, "网络连接失败，请检查网络设置"
        except Exception as e:
            return False, f"出错了: {str(e)}"
