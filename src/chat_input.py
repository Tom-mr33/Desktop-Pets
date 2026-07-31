"""内嵌聊天输入框模块：在桌宠下方显示一个输入框，无需打开独立窗口即可聊天"""

import threading
import tkinter as tk

from ai_client import AIClient
from emotion_parser import EmotionParser
from chat_history import ChatHistory


# 样式常量（与气泡/聊天窗口统一的粉色系）
COLOR_PRIMARY = '#db2777'
COLOR_PRIMARY_DARK = '#be185d'
COLOR_PRIMARY_LIGHT = '#fbcfe8'
COLOR_BG = '#ffffff'
COLOR_TEXT = '#1f2937'
COLOR_PLACEHOLDER = '#9ca3af'
COLOR_BORDER = '#fbcfe8'

INPUT_HEIGHT = 36
INPUT_MARGIN = 6


class ChatInputWindow:
    """桌宠内嵌输入框窗口：紧贴主窗口下方，跟随移动"""

    def __init__(self, pet):
        self.pet = pet
        self.ai_client = AIClient()
        self.history = ChatHistory()
        self.window = None
        self.entry = None
        self.placeholder_label = None
        self._waiting = False
        self._visible = False

        self.history.cleanup_old(keep_days=7)

    # ------------------------------------------------------------------
    # 窗口生命周期
    # ------------------------------------------------------------------

    def create(self):
        """创建输入框窗口（紧贴主窗口下方）"""
        if self.window and self.window.winfo_exists():
            return

        self.window = tk.Toplevel(self.pet.root)
        self.window.overrideredirect(True)
        self.window.attributes('-topmost', True)
        self.window.attributes('-transparentcolor', 'magenta')
        self.window.configure(bg='magenta')

        self._build_ui()
        self._sync_position()
        self._visible = True

    def destroy(self):
        """销毁输入框窗口"""
        if self.window and self.window.winfo_exists():
            self.window.destroy()
        self.window = None
        self.entry = None
        self.placeholder_label = None
        self._visible = False
        self._waiting = False

    @property
    def is_visible(self):
        return self._visible and self.window is not None and self.window.winfo_exists()

    # ------------------------------------------------------------------
    # UI 构建
    # ------------------------------------------------------------------

    def _build_ui(self):
        """构建圆角粉色边框输入框"""
        # 外层 Frame：magenta 背景（透明），留边距让圆角更自然
        outer = tk.Frame(self.window, bg='magenta')
        outer.pack(fill=tk.BOTH, expand=True, padx=INPUT_MARGIN, pady=INPUT_MARGIN)

        # 边框 Frame：粉色细边框
        border = tk.Frame(outer, bg=COLOR_BORDER, padx=2, pady=2)
        border.pack(fill=tk.BOTH, expand=True)

        # 内层背景 Frame：白色底
        inner = tk.Frame(border, bg=COLOR_BG)
        inner.pack(fill=tk.BOTH, expand=True)

        # 输入框
        self.entry = tk.Entry(
            inner,
            font=('Microsoft YaHei', 10),
            bg=COLOR_BG,
            fg=COLOR_TEXT,
            relief=tk.FLAT,
            bd=0,
            insertwidth=2,
            insertbackground=COLOR_PRIMARY,
            highlightthickness=0,
        )
        self.entry.pack(fill=tk.X, expand=True, padx=10, pady=7, ipady=2)

        # 绑定事件
        self.entry.bind('<Return>', lambda e: self._send_message())
        self.entry.bind('<FocusIn>', self._on_focus_in)
        self.entry.bind('<FocusOut>', self._on_focus_out)
        self.entry.bind('<KeyPress>', self._on_key_press)

        # 占位提示文字（用 Label 叠加方式实现 placeholder）
        self.placeholder_label = tk.Label(
            inner,
            text="...",
            font=('Microsoft YaHei', 10),
            bg=COLOR_BG,
            fg=COLOR_PLACEHOLDER,
            relief=tk.FLAT,
        )
        self._update_placeholder()

    def _update_placeholder(self):
        """更新占位符显示状态"""
        if not self.entry or not self.placeholder_label:
            return
        text = self.entry.get()
        if text:
            self.placeholder_label.place_forget()
        else:
            self.placeholder_label.place(x=12, y=0, relheight=1)

    # ------------------------------------------------------------------
    # 焦点处理
    # ------------------------------------------------------------------

    def _on_focus_in(self, event):
        self.placeholder_label.place_forget()

    def _on_focus_out(self, event):
        self._update_placeholder()

    def _on_key_press(self, event):
        # 任何按键都隐藏占位符
        if self.placeholder_label and self.placeholder_label.winfo_ismapped():
            self.placeholder_label.place_forget()
        # 延迟更新占位符（等输入框内容变化后）
        self.window.after(10, self._update_placeholder)

    def focus_entry(self):
        """聚焦输入框"""
        if self.entry and self.window and self.window.winfo_exists():
            self.window.lift()
            self.entry.focus_force()

    # ------------------------------------------------------------------
    # 位置同步
    # ------------------------------------------------------------------

    def _sync_position(self):
        """同步输入框窗口位置到主窗口正下方"""
        if not (self.window and self.window.winfo_exists()):
            return
        try:
            pet_x = self.pet._last_x
            pet_y = self.pet._last_y
            pet_w = self.pet.root.winfo_width()
            input_w = pet_w
            input_h = INPUT_HEIGHT + INPUT_MARGIN * 2
            x = pet_x
            y = pet_y + self.pet.root.winfo_height()
            self.window.geometry(f"{input_w}x{input_h}+{x}+{y}")
        except Exception:
            pass

    def update_position(self):
        """供主窗口在拖动时调用，同步位置"""
        self._sync_position()

    # ------------------------------------------------------------------
    # 消息发送
    # ------------------------------------------------------------------

    def _send_message(self):
        if self._waiting:
            return

        if not self.entry:
            return

        text = self.entry.get().strip()
        if not text:
            return

        self.entry.delete(0, tk.END)
        self._update_placeholder()

        # 保存用户消息
        self.history.add_message('user', text)

        # 如果历史记录窗口正打开，刷新显示
        if self.pet.chat_window and self.pet.chat_window.is_open:
            self.pet.chat_window.refresh_history()

        # 桌宠进入思考状态
        self.pet.set_state('think', duration=0)
        self.pet.show_bubble("对方正在输入中...", 3000, effect='question')

        # 禁用输入，等待回复
        self._waiting = True
        self.entry.config(state=tk.DISABLED, fg=COLOR_PLACEHOLDER)

        # 异步调用 API
        thread = threading.Thread(target=self._call_api, args=(text,), daemon=True)
        thread.start()

    def _call_api(self, user_text):
        """在子线程中调用 AI API"""
        messages = self.history.get_api_messages(self.ai_client.max_history)
        success, reply = self.ai_client.chat(messages)

        if self.window and self.window.winfo_exists():
            self.window.after(0, lambda: self._on_api_response(success, reply))

    def _on_api_response(self, success, reply):
        """API 响应回调（主线程）"""
        self._waiting = False
        if self.entry:
            self.entry.config(state=tk.NORMAL, fg=COLOR_TEXT)

        if not success:
            self.pet.set_state('sad', duration=2000)
            self.pet.show_bubble("呜呜，出错了...", 2000)
            return

        # 解析情感标签
        emotion, reply_text = EmotionParser.parse(reply)
        self.history.add_message('assistant', reply_text)

        # 如果历史记录窗口正打开，刷新显示
        if self.pet.chat_window and self.pet.chat_window.is_open:
            self.pet.chat_window.refresh_history()

        # 设置桌宠表情和气泡
        state_str, effect = EmotionParser.get_state_and_effect(emotion)
        self.pet.set_state(state_str, duration=3000)

        # 气泡显示回复（截断过长文本）
        display_text = reply_text[:20] + ("..." if len(reply_text) > 20 else "")
        self.pet.show_bubble(display_text, 3000, effect=effect)

        # 恢复输入框焦点
        if self.entry and self.window and self.window.winfo_exists():
            self.entry.focus_set()
