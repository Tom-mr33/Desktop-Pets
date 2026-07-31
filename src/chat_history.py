"""对话历史管理模块：按天存储和加载对话记录"""

import os
import json
import datetime


class ChatHistory:
    """管理对话历史的读写，按天存储 JSON 文件"""

    def __init__(self, history_dir=None):
        if history_dir is None:
            # 历史文件存放在程序同目录下的 chat_history 文件夹
            if getattr(os, '_frozen', False) or getattr(__import__('sys'), 'frozen', False):
                base = os.path.dirname(__import__('sys').executable)
            else:
                base = os.path.dirname(os.path.abspath(__file__))
            history_dir = os.path.join(base, 'chat_history')
        self.history_dir = history_dir
        os.makedirs(self.history_dir, exist_ok=True)
        self.messages = []
        self._load_today()

    def _today_filename(self):
        today = datetime.datetime.now().strftime('%Y%m%d')
        return os.path.join(self.history_dir, f'chat_history_{today}.json')

    def _load_today(self):
        """加载当天的对话历史"""
        path = self._today_filename()
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    self.messages = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.messages = []
        else:
            self.messages = []

    def _save(self):
        """保存到当天的历史文件"""
        path = self._today_filename()
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(self.messages, f, ensure_ascii=False, indent=2)
        except IOError:
            pass

    def add_message(self, role, content):
        """添加一条消息并保存"""
        self.messages.append({
            'role': role,
            'content': content,
            'time': datetime.datetime.now().strftime('%H:%M:%S')
        })
        self._save()

    def get_api_messages(self, max_rounds=10):
        """
        返回发送给 API 的消息列表（只保留最近 max_rounds 轮对话）。
        每轮 = 一条 user + 一条 assistant。
        """
        # 取最近的 max_rounds*2 条消息
        recent = self.messages[-(max_rounds * 2):]
        return [{'role': m['role'], 'content': m['content']} for m in recent]

    def get_display_messages(self):
        """返回用于显示的完整当天消息列表"""
        return list(self.messages)

    def clear(self):
        """清空当天历史"""
        self.messages = []
        self._save()

    def cleanup_old(self, keep_days=7):
        """清理 keep_days 天前的历史文件"""
        cutoff = datetime.datetime.now() - datetime.timedelta(days=keep_days)
        for fname in os.listdir(self.history_dir):
            if not fname.startswith('chat_history_') or not fname.endswith('.json'):
                continue
            try:
                date_str = fname.replace('chat_history_', '').replace('.json', '')
                file_date = datetime.datetime.strptime(date_str, '%Y%m%d')
                if file_date < cutoff:
                    os.remove(os.path.join(self.history_dir, fname))
            except (ValueError, OSError):
                pass
