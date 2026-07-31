"""聊天历史记录查看窗口模块"""

import tkinter as tk

from ai_client import AIClient
from emotion_parser import EmotionParser
from chat_history import ChatHistory


class ChatWindow:
    """桌面宠物聊天历史记录查看窗口"""

    def __init__(self, pet):
        self.pet = pet
        self.ai_client = AIClient()
        self.history = ChatHistory()
        self.window = None
        self.text_area = None
        self.status_label = None

        self.history.cleanup_old(keep_days=7)

    def toggle(self):
        if self.window and self.window.winfo_exists():
            self.close()
        else:
            self.open()

    def open(self):
        if self.window and self.window.winfo_exists():
            self.window.lift()
            return

        # 关键：临时恢复主窗口为正常窗口，让子窗口能获得焦点
        self.pet.root.overrideredirect(False)
        self.pet.root.attributes('-topmost', False)
        self.pet.root.update_idletasks()
        self.pet.root.withdraw()

        self.window = tk.Toplevel(self.pet.root)
        self.window.title("聊天记录")
        self.window.resizable(False, False)
        self.window.configure(bg='#ffffff')

        # 窗口位置：在宠物右侧
        pet_x = self.pet._last_x if hasattr(self.pet, '_last_x') else 400
        pet_y = self.pet._last_y if hasattr(self.pet, '_last_y') else 300
        self.window.geometry(f"380x520+{pet_x + 220}+{pet_y}")

        self.window.protocol("WM_DELETE_WINDOW", self.close)

        self._build_ui()
        self._load_history_display()

        if not self.ai_client.is_configured:
            self._append_system_message(
                "API Key 未配置！\n"
                "请在程序目录下的 config.json 文件中填写你的通义千问 API Key。\n"
                "获取地址：https://dashscope.console.aliyun.com/"
            )

    def close(self):
        if self.window and self.window.winfo_exists():
            self.window.destroy()
        self.window = None
        # 恢复主窗口
        self.pet.root.overrideredirect(True)
        self.pet.root.attributes('-topmost', self.pet.is_top)
        self.pet.root.deiconify()
        # 恢复内嵌输入框焦点
        if self.pet.chat_input and self.pet.chat_input.is_visible:
            self.pet.chat_input.focus_entry()

    @property
    def is_open(self):
        return self.window is not None and self.window.winfo_exists()

    def _build_ui(self):
        """构建历史记录查看窗口 UI（无输入区域）"""
        # ===== 顶部标题栏 =====
        header = tk.Frame(self.window, bg='#db2777', height=36)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        tk.Label(
            header, text="沈不渝", font=('Microsoft YaHei', 11, 'bold'),
            bg='#db2777', fg='white'
        ).pack(side=tk.LEFT, padx=12, pady=6)

        tk.Label(
            header, text="聊天记录", font=('Microsoft YaHei', 8),
            bg='#db2777', fg='#fbcfe8'
        ).pack(side=tk.LEFT, padx=(0, 12), pady=6)

        # ===== 对话历史区域 =====
        chat_frame = tk.Frame(self.window, bg='#f3f4f6')
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

        self.text_area = tk.Text(
            chat_frame,
            wrap=tk.WORD,
            font=('Microsoft YaHei', 10),
            state=tk.DISABLED,
            bg='#f3f4f6',
            fg='#1f2937',
            padx=12,
            pady=10,
            spacing1=2,
            spacing3=2,
            relief=tk.FLAT,
            highlightthickness=0,
            bd=0,
            insertwidth=0,
        )
        scrollbar = tk.Scrollbar(chat_frame, command=self.text_area.yview, width=6)
        self.text_area.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 文本标签样式
        self.text_area.tag_config('user_name', foreground='#2563eb', font=('Microsoft YaHei', 9, 'bold'), spacing1=8)
        self.text_area.tag_config('user_text', foreground='#1e40af', lmargin1=16, lmargin2=16)
        self.text_area.tag_config('pet_name', foreground='#db2777', font=('Microsoft YaHei', 9, 'bold'), spacing1=8)
        self.text_area.tag_config('pet_text', foreground='#831843', lmargin1=16, lmargin2=16)
        self.text_area.tag_config('system', foreground='#9ca3af', font=('Microsoft YaHei', 8), justify='center', spacing1=6)
        self.text_area.tag_config('time', foreground='#d1d5db', font=('Microsoft YaHei', 7), justify='right')

        # ===== 底部提示 =====
        self.status_label = tk.Label(
            self.window, text="在桌宠下方输入框直接聊天，这里查看历史记录",
            font=('Microsoft YaHei', 8),
            fg='#9ca3af', bg='#ffffff', anchor='w'
        )
        self.status_label.pack(fill=tk.X, padx=12, pady=8)

    def _load_history_display(self):
        messages = self.history.get_display_messages()
        if not messages:
            self._append_system_message("还没有聊天记录，在桌宠下方输入框开始聊天吧~")
            return
        for msg in messages:
            role = msg.get('role', '')
            content = msg.get('content', '')
            time_str = msg.get('time', '')
            if role == 'user':
                self._append_message("你", content, 'user', time_str)
            elif role == 'assistant':
                self._append_message("沈不渝", content, 'pet', time_str)

    def _append_message(self, sender, text, tag, time_str=""):
        if not self.text_area:
            return
        self.text_area.config(state=tk.NORMAL)
        if time_str:
            self.text_area.insert(tk.END, f"{time_str}\n", 'time')
        name_tag = f'{tag}_name'
        text_tag = f'{tag}_text'
        self.text_area.insert(tk.END, f"{sender}\n", name_tag)
        self.text_area.insert(tk.END, f"{text}\n", text_tag)
        self.text_area.see(tk.END)
        self.text_area.config(state=tk.DISABLED)

    def _append_system_message(self, text):
        if not self.text_area:
            return
        self.text_area.config(state=tk.NORMAL)
        self.text_area.insert(tk.END, f"── {text} ──\n", 'system')
        self.text_area.see(tk.END)
        self.text_area.config(state=tk.DISABLED)

    def refresh_history(self):
        """刷新历史记录显示（供外部调用）"""
        if not self.window or not self.window.winfo_exists():
            return
        # 清空当前显示
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete('1.0', tk.END)
        self.text_area.config(state=tk.DISABLED)
        # 重新加载
        self._load_history_display()
