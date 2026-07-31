import sys
import os
import random
import math
import time
import datetime
import tkinter as tk
from tkinter import Menu, Label, font as tkfont
from PIL import Image, ImageTk

# AI 聊天模块（可选，导入失败不影响基础功能）
try:
    from chat_window import ChatWindow
    from chat_input import ChatInputWindow
    CHAT_AVAILABLE = True
except ImportError:
    CHAT_AVAILABLE = False


def get_resource_path(relative_path):
    """获取资源文件路径，兼容打包后运行和开发模式"""
    candidates = []
    if getattr(sys, 'frozen', False):
        candidates.append(os.path.join(os.path.dirname(sys.executable), relative_path))
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        candidates.append(os.path.join(script_dir, 'assets', relative_path))
        candidates.append(os.path.join(script_dir, relative_path))
    for path in candidates:
        if os.path.exists(path):
            return path
    return candidates[0]


# ============ 对话气泡内容 ============
DIALOGUES_IDLE = ["宝宝~","好爱你啊~","你好呀~", "在干嘛呢？", "摸摸头~", "嘻嘻~", "陪我玩嘛！", "嘿嘿~", "你最好了！", "加油哦~", "今天也要开心！"]
DIALOGUES_HAPPY = ["好开心呀！", "太棒了！", "最喜欢你了！", "嘿嘿嘿~"]
DIALOGUES_SAD = ["呜呜...", "有点难过...", "抱抱我...", "心情不好..."]
DIALOGUES_BORED = ["好无聊啊...", "没人陪我玩...", "发呆中...", "嗯...干嘛呢..."]
DIALOGUES_ANGRY = ["哼！", "不理你了！", "生气气了！", "别碰我！"]
DIALOGUES_EAT = ["好好吃！", "啊呜啊呜~", "谢谢投喂！", "还要还要！"]
DIALOGUES_DRINK = ["咕嘟咕嘟~", "解渴了！", "谢谢~", "好喝！"]
DIALOGUES_SLEEP = ["Zzz...", "晚安...", "好困...", "呼...呼..."]
DIALOGUES_MORNING = ["早上好呀！", "新的一天开始了！", "早安~", "今天也要加油！"]
DIALOGUES_NIGHT = ["晚上好~", "该休息了...", "夜深了...", "晚安哦~"]
DIALOGUES_LOVE = ["最喜欢你了！", "比心~", "爱你哦！", "嘿嘿，害羞..."]
DIALOGUES_TICKLE = ["哈哈哈！", "好痒啊！", "别挠了！", "嘻嘻嘻~"]
DIALOGUES_POKE = ["戳我干嘛~", "嗯？", "有事吗？", "怎么啦？"]
DIALOGUES_TSUNDERE = ["才、才不是特意陪你的！", "哼，只是顺便而已！", "别误会了！", "才不喜欢你呢...大概"]
DIALOGUES_THINK = ["让我想想...", "嗯...", "思考中...", "这个问题好难..."]
DIALOGUES_SHOCKED = ["什么？！", "不会吧！", "真的假的！", "吓我一跳！"]
DIALOGUES_SMUG = ["嘿嘿，我厉害吧！", "就是这样！", "不愧是我！", "怎么样，佩服吧！"]
DIALOGUES_GIGGLE = ["咯咯咯~", "嘻嘻嘻~", "嘿嘿嘿~", "太好笑了！"]
DIALOGUES_LECTURE = ["听好了！", "要认真一点！", "这样不对！", "让我来教你！"]
DIALOGUES_BIRTHDAY = ["生日快乐！", "祝你生日快乐！", "许个愿吧！", "今天你最特别！"]
DIALOGUES_FESTIVAL = ["新年快乐！", "恭喜发财！", "万事如意！", "新年新气象！"]
DIALOGUES_HALLOWEEN = ["不给糖就捣蛋！", "Trick or treat!", "万圣节快乐！", "嗷呜~"]
DIALOGUES_CHRISTMAS = ["圣诞快乐！", "Merry Christmas!", "铃儿响叮当~", "圣诞老人来了！"]
DIALOGUES_HAPPY_2 = ["超级开心！", "今天真幸运！", "太幸福了！", "快乐满满！"]

# ============ 特效气泡映射 ============
BUBBLE_EFFECTS = {
    'question': 'character_bubble_question.png',
    'exclaim': 'character_bubble_exclaim.png',
    'music': 'character_bubble_music.png',
    'silence': 'character_bubble_silence.png',
    'idea': 'character_bubble_idea.png',
}

# ============ 表情状态常量 ============
class PetState:
    IDLE = "idle"
    BREATH_UP = "breath_up"
    BREATH_DOWN = "breath_down"
    HAPPY = "happy"
    HAPPY_2 = "happy_2"
    SAD = "sad"
    SURPRISED = "surprised"
    SHY = "shy"
    ANGRY = "angry"
    ANNOYED = "annoyed"
    FURIOUS = "furious"
    SMUG = "smug"
    BORED = "bored"
    SERIOUS = "serious"
    SHOCKED = "shocked"
    THINK = "think"
    BLUSH_LIGHT = "blush_light"
    BLUSH_HEAVY = "blush_heavy"
    TEARING = "tearing"
    BAWL = "bawl"
    LOOKBACK = "lookback"
    HEAD_DOWN = "head_down"
    TILT = "tilt"
    YAWN = "yawn"
    SLEEP = "sleep"
    SLUMP = "slump"
    STRETCH = "stretch"
    CHIN = "chin"
    CROSS = "cross"
    CROUCH = "crouch"
    POKED = "poked"
    LOVE = "love"
    BLUSH = "blush"
    PEEK = "peek"
    GIGGLE = "giggle"
    TSUNDERE = "tsundere"
    LECTURE = "lecture"
    INTRO = "intro"
    CROPPED = "cropped"
    WAKE = "wake"
    BYE = "bye"
    CRY = "cry"
    DIZZY = "dizzy"
    ZOOM = "zoom"
    TINY = "tiny"
    EAT = "eat"
    DRINK = "drink"
    MORNING = "morning"
    NIGHT = "night"
    BIRTHDAY = "birthday"
    FESTIVAL = "festival"
    HALLOWEEN = "halloween"
    CHRISTMAS = "christmas"


# ============ 状态到图片文件的映射（原角度） ============
SIDE_EXPRESSIONS = {
    PetState.IDLE: "character.png",
    PetState.BREATH_UP: "character_breath_up.png",
    PetState.BREATH_DOWN: "character_breath_down.png",
    PetState.HAPPY: "character_happy_1.png",
    PetState.HAPPY_2: "character_happy_2.png",
    PetState.SAD: "character_sad.png",
    PetState.SURPRISED: "character_surprised.png",
    PetState.SHY: "character_shy.png",
    PetState.ANGRY: "character_angry.png",
    PetState.ANNOYED: "character_annoyed.png",
    PetState.FURIOUS: "character_furious.png",
    PetState.SMUG: "character_smug.png",
    PetState.BORED: "character_bored.png",
    PetState.SERIOUS: "character_serious.png",
    PetState.SHOCKED: "character_shocked.png",
    PetState.THINK: "character_think.png",
    PetState.BLUSH_LIGHT: "character_blush_light.png",
    PetState.BLUSH_HEAVY: "character_blush_heavy.png",
    PetState.TEARING: "character_tearing.png",
    PetState.BAWL: "character_bawl.png",
    PetState.LOOKBACK: "character_lookback.png",
    PetState.HEAD_DOWN: "character_head_down.png",
    PetState.TILT: "character_tilt.png",
    PetState.YAWN: "character_yawn.png",
    PetState.SLEEP: "character_sleep.png",
    PetState.SLUMP: "character_slump.png",
    PetState.STRETCH: "character_stretch.png",
    PetState.CHIN: "character_chin.png",
    PetState.CROSS: "character_cross.png",
    PetState.CROUCH: "character_crouch.png",
    PetState.POKED: "character_poked.png",
    PetState.LOVE: "character_love.png",
    PetState.BLUSH: "character_blush.png",
    PetState.PEEK: "character_peek.png",
    PetState.GIGGLE: "character_giggle.png",
    PetState.TSUNDERE: "character_tsundere.png",
    PetState.LECTURE: "character_lecture.png",
    PetState.INTRO: "character_intro.png",
    PetState.CROPPED: "character_cropped.png",
    PetState.WAKE: "character_wake.png",
    PetState.BYE: "character_bye.png",
    PetState.CRY: "character_cry.png",
    PetState.DIZZY: "character_dizzy.png",
    PetState.ZOOM: "character_zoom.png",
    PetState.TINY: "character_tiny.png",
    PetState.EAT: "character_eat.png",
    PetState.DRINK: "character_drink.png",
    PetState.MORNING: "character_morning.png",
    PetState.NIGHT: "character_night.png",
    PetState.BIRTHDAY: "character_birthday.png",
    PetState.FESTIVAL: "character_festival.png",
    PetState.HALLOWEEN: "character_halloween.png",
    PetState.CHRISTMAS: "character_christmas.png",
}

# ============ 状态到图片文件的映射（正脸） ============
FRONT_EXPRESSIONS = {
    PetState.IDLE: "character_front.png",
    PetState.BREATH_UP: "character_front_breath_up.png",
    PetState.BREATH_DOWN: "character_front_breath_down.png",
    PetState.HAPPY: "character_front_happy.png",
    PetState.SAD: "character_front_sad.png",
    PetState.SURPRISED: "character_front_surprised.png",
    PetState.SHY: "character_front_shy.png",
    PetState.ANGRY: "character_front_angry.png",
    PetState.SMUG: "character_front_smug.png",
    PetState.BORED: "character_front_bored.png",
    PetState.SERIOUS: "character_front_serious.png",
    PetState.SLEEP: "character_front_sleep.png",
    PetState.YAWN: "character_front_yawn.png",
    PetState.POKED: "character_front_poked.png",
    PetState.TSUNDERE: "character_front_tsundere.png",
    PetState.GIGGLE: "character_front_giggle.png",
    PetState.BLUSH: "character_front_blush.png",
    PetState.CHIN: "character_front_chin.png",
    PetState.DIZZY: "character_front_dizzy.png",
}

# 正脸没有的状态，回退到原角度
FRONT_FALLBACK = {
    PetState.ANNOYED: PetState.ANGRY,
    PetState.FURIOUS: PetState.ANGRY,
    PetState.SHOCKED: PetState.SURPRISED,
    PetState.THINK: PetState.SERIOUS,
    PetState.BLUSH_LIGHT: PetState.BLUSH,
    PetState.BLUSH_HEAVY: PetState.BLUSH,
    PetState.TEARING: PetState.SAD,
    PetState.BAWL: PetState.SAD,
    PetState.LOOKBACK: PetState.IDLE,
    PetState.HEAD_DOWN: PetState.SAD,
    PetState.TILT: PetState.IDLE,
    PetState.SLUMP: PetState.BORED,
    PetState.STRETCH: PetState.IDLE,
    PetState.CROSS: PetState.SERIOUS,
    PetState.CROUCH: PetState.IDLE,
    PetState.LOVE: PetState.HAPPY,
    PetState.PEEK: PetState.IDLE,
    PetState.LECTURE: PetState.SERIOUS,
    PetState.INTRO: PetState.IDLE,
    PetState.WAKE: PetState.IDLE,
    PetState.BYE: PetState.SAD,
    PetState.CRY: PetState.SAD,
    PetState.ZOOM: PetState.SURPRISED,
    PetState.TINY: PetState.SURPRISED,
    PetState.EAT: PetState.HAPPY,
    PetState.DRINK: PetState.HAPPY,
    PetState.MORNING: PetState.HAPPY,
    PetState.NIGHT: PetState.SLEEP,
    PetState.BIRTHDAY: PetState.HAPPY,
    PetState.FESTIVAL: PetState.HAPPY,
    PetState.HALLOWEEN: PetState.SURPRISED,
    PetState.CHRISTMAS: PetState.HAPPY,
}

# ============ 过渡配置 ============
TRANSITION_CONFIG = {
    'default': {'duration': 250, 'steps': 12},
    'emotion': {'duration': 350, 'steps': 16},
    'action': {'duration': 300, 'steps': 14},
    'view': {'duration': 400, 'steps': 18},
    'lifecycle': {'duration': 500, 'steps': 20},
}

EMOTION_STATES = {
    PetState.HAPPY, PetState.HAPPY_2, PetState.SAD, PetState.SURPRISED, PetState.SHY,
    PetState.ANGRY, PetState.ANNOYED, PetState.FURIOUS, PetState.SMUG,
    PetState.BORED, PetState.SERIOUS, PetState.SHOCKED, PetState.THINK,
    PetState.BLUSH_LIGHT, PetState.BLUSH_HEAVY, PetState.TEARING, PetState.BAWL,
    PetState.LOVE, PetState.BLUSH, PetState.TSUNDERE, PetState.GIGGLE,
}

ACTION_STATES = {
    PetState.LOOKBACK, PetState.HEAD_DOWN, PetState.TILT, PetState.YAWN,
    PetState.SLEEP, PetState.SLUMP, PetState.STRETCH, PetState.CHIN,
    PetState.CROSS, PetState.CROUCH, PetState.POKED, PetState.PEEK,
    PetState.LECTURE, PetState.EAT, PetState.DRINK,
}

LIFECYCLE_STATES = {
    PetState.INTRO, PetState.CROPPED, PetState.WAKE, PetState.BYE, PetState.CRY,
    PetState.MORNING, PetState.NIGHT, PetState.BIRTHDAY,
    PetState.FESTIVAL, PetState.HALLOWEEN, PetState.CHRISTMAS,
}

# 自主行为配置
AUTONOMOUS_BEHAVIORS = {
    PetState.YAWN: (45, 120, 3000, DIALOGUES_SLEEP),
    PetState.STRETCH: (60, 150, 2500, DIALOGUES_IDLE),
    PetState.BORED: (40, 100, 4000, DIALOGUES_BORED),
    PetState.SLEEP: (90, 180, 6000, DIALOGUES_SLEEP),
    PetState.PEEK: (50, 110, 2500, DIALOGUES_IDLE),
    PetState.CHIN: (55, 130, 3500, DIALOGUES_THINK),
    PetState.THINK: (60, 140, 4000, DIALOGUES_THINK),
    PetState.GIGGLE: (70, 160, 2500, DIALOGUES_GIGGLE),
    PetState.SMUG: (80, 170, 3000, DIALOGUES_SMUG),
    PetState.LOOKBACK: (45, 100, 2000, DIALOGUES_IDLE),
    PetState.HEAD_DOWN: (70, 150, 3000, DIALOGUES_SAD),
    PetState.TILT: (50, 120, 2500, DIALOGUES_IDLE),
    PetState.SLUMP: (80, 160, 3500, DIALOGUES_BORED),
    PetState.CROSS: (90, 180, 4000, DIALOGUES_TSUNDERE),
    PetState.CROUCH: (100, 200, 3000, DIALOGUES_IDLE),
    PetState.TSUNDERE: (70, 150, 3500, DIALOGUES_TSUNDERE),
    PetState.LECTURE: (90, 180, 4000, DIALOGUES_LECTURE),
}

EMOTION_PROGRESSIONS = {
    'happy': [PetState.HAPPY, PetState.HAPPY_2, PetState.BLUSH_LIGHT, PetState.BLUSH_HEAVY],
    'angry': [PetState.ANNOYED, PetState.ANGRY, PetState.FURIOUS],
    'sad': [PetState.SAD, PetState.TEARING, PetState.BAWL],
}

FESTIVALS = {
    (1, 1): (PetState.FESTIVAL, DIALOGUES_FESTIVAL),
    (10, 31): (PetState.HALLOWEEN, DIALOGUES_HALLOWEEN),
    (12, 25): (PetState.CHRISTMAS, DIALOGUES_CHRISTMAS),
}

# 状态对应的气泡特效（自动匹配）
STATE_BUBBLE_EFFECTS = {
    PetState.THINK: 'question',
    PetState.SURPRISED: 'exclaim',
    PetState.SHOCKED: 'exclaim',
    PetState.HAPPY: 'music',
    PetState.HAPPY_2: 'music',
    PetState.GIGGLE: 'music',
    PetState.BORED: 'silence',
    PetState.SLUMP: 'silence',
    PetState.HEAD_DOWN: 'silence',
}


class DesktopPet:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("沈不渝桌宠")
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.attributes('-transparentcolor', 'magenta')

        self.scale = 1.0
        self.base_size = 200
        self.is_top = True
        self.bubble_height = 40
        self.view_mode = 'side'

        self.expressions = {'side': {}, 'front': {}}
        self.load_expressions()

        self.current_scaled = {'side': {}, 'front': {}}
        self.tk_image = None

        self.canvas = tk.Canvas(self.root, bg='magenta', highlightthickness=0, bd=0)
        self.canvas.pack(fill='both', expand=True)

        self.character_id = None
        self.bubble_id = None
        self.bubble_text_ids = []
        self.bubble_timer = None
        self.bubble_effect_id = None

        self.state = PetState.IDLE
        self.previous_state = PetState.IDLE
        self.state_timer = None
        self.state_duration = 0
        self.state_queue = []

        # 呼吸动画已移除

        # 眨眼动画已移除

        self.anim_type = None
        self.anim_frame = 0
        self.anim_running = False
        self.base_y = 50

        self.transition_running = False
        self.transition_alpha = 0
        self.transition_from = None
        self.transition_to = None
        self.transition_duration = 150
        self.transition_steps = 8

        self.dragging = False
        self.drag_x = 0
        self.drag_y = 0
        self.press_x = 0
        self.press_y = 0
        self.drag_start_time = 0

        self.emotion_level = {'happy': 0, 'angry': 0, 'sad': 0}
        self.emotion_cooldown = {'happy': 0, 'angry': 0, 'sad': 0}
        self.last_interaction_time = time.time()

        # AI 聊天窗口（历史记录查看）和内嵌输入框
        self.chat_window = None
        self.chat_input = None
        if CHAT_AVAILABLE:
            self.chat_window = ChatWindow(self)
            self.chat_input = ChatInputWindow(self)

        self.behavior_timer = None
        self.schedule_next_behavior()

        self.time_check_timer = None
        self.last_time_state = None
        self.schedule_time_check()

        self.check_festival()
        # 示例：如果用户生日是 6 月 25 日，取消下面注释
        # self.check_birthday(6, 25)

        self.update_size()
        self.setup_events()

        self.root.geometry(f"+{400}+{300}")
        self._last_x = 400
        self._last_y = 300

        # 启动动画序列：cropped -> intro -> idle
        self.state = PetState.CROPPED
        self.update_display()
        self.show_bubble("你好呀！我是沈不渝~", 2500)
        self.root.after(800, lambda: self.set_state(PetState.INTRO, duration=1500))
        self.root.after(2500, lambda: self.set_state(PetState.IDLE))

        self._emotion_decay_loop()

        # 创建内嵌输入框窗口（紧贴主窗口下方）
        if self.chat_input:
            self.root.after(500, self._init_chat_input)

    def _emotion_decay_loop(self):
        """情绪衰减循环：长时间不互动，情绪等级自动降低"""
        current_time = time.time()
        if current_time - self.last_interaction_time > 30:
            for key in self.emotion_level:
                self.emotion_level[key] = max(0, self.emotion_level[key] - 1)
            self.last_interaction_time = current_time
        self.root.after(10000, self._emotion_decay_loop)

    def _init_chat_input(self):
        """初始化内嵌输入框窗口"""
        if self.chat_input:
            self.chat_input.create()
            self.chat_input.focus_entry()

    def load_expressions(self):
        for state, filename in SIDE_EXPRESSIONS.items():
            path = get_resource_path(filename)
            if os.path.exists(path):
                img = Image.open(path).convert('RGBA')
                alpha = img.getchannel('A')
                alpha = alpha.point(lambda a: 255 if a >= 128 else 0)
                img.putalpha(alpha)
                self.expressions['side'][state] = img
            else:
                print(f"警告: 找不到 {filename}")
                self.expressions['side'][state] = self.expressions['side'].get(PetState.IDLE)

        for state, filename in FRONT_EXPRESSIONS.items():
            path = get_resource_path(filename)
            if os.path.exists(path):
                img = Image.open(path).convert('RGBA')
                alpha = img.getchannel('A')
                alpha = alpha.point(lambda a: 255 if a >= 128 else 0)
                img.putalpha(alpha)
                self.expressions['front'][state] = img
            else:
                print(f"警告: 找不到 {filename}")

        if PetState.IDLE not in self.expressions['side']:
            raise FileNotFoundError("找不到 character.png")

    def get_expression(self, state, view_mode=None):
        if view_mode is None:
            view_mode = self.view_mode
        if view_mode == 'front':
            if state in self.expressions['front']:
                return self.expressions['front'][state]
            fallback_state = FRONT_FALLBACK.get(state, PetState.IDLE)
            if fallback_state in self.expressions['front']:
                return self.expressions['front'][fallback_state]
            return self.expressions['side'].get(state, self.expressions['side'][PetState.IDLE])
        return self.expressions['side'].get(state, self.expressions['side'][PetState.IDLE])

    def setup_events(self):
        self.canvas.bind('<ButtonPress-1>', self.on_press)
        self.canvas.bind('<B1-Motion>', self.on_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_release)
        self.canvas.bind('<MouseWheel>', self.on_wheel)
        self.canvas.bind('<Button-3>', self.show_menu)

    def update_size(self):
        size = int(self.base_size * self.scale)
        orig = self.get_expression(PetState.IDLE)
        orig_w = orig.width
        orig_h = orig.height
        ratio = orig_h / orig_w
        img_w = size
        img_h = int(size * ratio)

        win_h = img_h + self.bubble_height + 20
        self.root.geometry(f"{img_w}x{win_h}")
        self.canvas.config(width=img_w, height=win_h)

        self.current_scaled = {'side': {}, 'front': {}}
        for view in ['side', 'front']:
            for state, img in self.expressions[view].items():
                resized = img.resize((img_w, img_h), Image.LANCZOS)
                alpha = resized.getchannel('A')
                alpha = alpha.point(lambda a: 255 if a >= 128 else 0)
                resized.putalpha(alpha)
                self.current_scaled[view][state] = resized

        self.img_w = img_w
        self.img_h = img_h
        self.update_display()

        # 窗口尺寸变化时同步输入框位置
        if self.chat_input and self.chat_input.is_visible:
            self.chat_input.update_position()

    def get_scaled_image(self, state, view_mode=None):
        if view_mode is None:
            view_mode = self.view_mode
        if view_mode == 'front':
            if state in self.current_scaled['front']:
                return self.current_scaled['front'][state]
            fallback_state = FRONT_FALLBACK.get(state, PetState.IDLE)
            if fallback_state in self.current_scaled['front']:
                return self.current_scaled['front'][fallback_state]
            return self.current_scaled['side'].get(state, self.current_scaled['side'][PetState.IDLE])
        return self.current_scaled['side'].get(state, self.current_scaled['side'][PetState.IDLE])

    def update_display(self):
        current_img = self.get_scaled_image(self.state)
        self.tk_image = ImageTk.PhotoImage(current_img)

        if self.character_id:
            self.canvas.delete(self.character_id)

        y = self.base_y + self.img_h // 2

        self.character_id = self.canvas.create_image(
            self.img_w // 2, y, image=self.tk_image
        )

        # 角色重建后，把已有气泡提到最上层，避免被角色图片遮挡
        if self.bubble_id:
            self.canvas.tag_raise(self.bubble_id)
            for tid in self.bubble_text_ids:
                self.canvas.tag_raise(tid)
            if self.bubble_effect_id:
                self.canvas.tag_raise(self.bubble_effect_id)

    def get_transition_config(self, from_state, to_state):
        if to_state in LIFECYCLE_STATES or from_state in LIFECYCLE_STATES:
            return TRANSITION_CONFIG['lifecycle']
        if to_state in EMOTION_STATES or from_state in EMOTION_STATES:
            return TRANSITION_CONFIG['emotion']
        if to_state in ACTION_STATES or from_state in ACTION_STATES:
            return TRANSITION_CONFIG['action']
        return TRANSITION_CONFIG['default']

    def set_state(self, new_state, duration=0, force=False):
        if new_state == self.state and not force:
            return
        if self.transition_running:
            if new_state not in self.state_queue:
                self.state_queue.append(new_state)
            return

        self.previous_state = self.state
        self.transition_from = self.state
        self.transition_to = new_state
        self.transition_running = True
        self.transition_alpha = 0

        config = self.get_transition_config(self.state, new_state)
        self.transition_duration = config['duration']
        self.transition_steps = config['steps']

        self.state_duration = duration
        if self.state_timer:
            self.root.after_cancel(self.state_timer)
            self.state_timer = None

        self.animate_transition()

    def animate_transition(self):
        if not self.transition_running:
            return
        self.transition_alpha += 255 // self.transition_steps
        if self.transition_alpha >= 255:
            self.complete_transition()
            return

        from_img = self.get_scaled_image(self.transition_from)
        to_img = self.get_scaled_image(self.transition_to)
        blended = Image.blend(from_img, to_img, self.transition_alpha / 255.0)
        self.tk_image = ImageTk.PhotoImage(blended)
        self.canvas.itemconfig(self.character_id, image=self.tk_image)

        self.root.after(self.transition_duration // self.transition_steps, self.animate_transition)

    def complete_transition(self):
        self.transition_running = False
        self.state = self.transition_to
        self.update_display()

        if self.state_queue:
            next_state = self.state_queue.pop(0)
            self.set_state(next_state, duration=self.state_duration)
            return

        if self.state_duration > 0:
            self.state_timer = self.root.after(self.state_duration, lambda: self.set_state(PetState.IDLE))

    def on_press(self, event):
        self.dragging = True
        self.drag_x = event.x_root - self.root.winfo_x()
        self.drag_y = event.y_root - self.root.winfo_y()
        self.press_x = event.x
        self.press_y = event.y
        self.drag_start_time = time.time()

    def on_drag(self, event):
        if self.dragging:
            x = event.x_root - self.drag_x
            y = event.y_root - self.drag_y
            self.root.geometry(f"+{x}+{y}")
            self._last_x = x
            self._last_y = y
            # 拖动时直接切换状态，不使用过渡动画避免闪烁
            if self.state != PetState.DIZZY:
                self.state = PetState.DIZZY
                self.update_display()
            # 同步内嵌输入框窗口位置
            if self.chat_input and self.chat_input.is_visible:
                self.chat_input.update_position()

    def on_release(self, event):
        if self.dragging:
            moved = abs(event.x - self.press_x) + abs(event.y - self.press_y)
            drag_duration = time.time() - self.drag_start_time
            if moved < 8 and drag_duration < 0.3:
                self.trigger_interaction()
            elif self.state == PetState.DIZZY:
                self.state = PetState.IDLE
                self.update_display()
        self.dragging = False

    def _trigger_happy_progression(self):
        """情绪递进：连续触发 happy -> happy_2 -> blush_light -> blush_heavy"""
        current_time = time.time()
        if current_time < self.emotion_cooldown.get('happy', 0):
            self.set_state(PetState.LOVE, duration=2000)
            self.show_bubble(random.choice(DIALOGUES_LOVE), 2000)
            return

        level = self.emotion_level.get('happy', 0)
        progression = EMOTION_PROGRESSIONS['happy']
        level = min(level, len(progression) - 1)
        state = progression[level]
        self.emotion_level['happy'] = level + 1
        self.emotion_cooldown['happy'] = current_time + 3.0
        self.last_interaction_time = current_time

        if level == 0:
            dialogue = random.choice(DIALOGUES_HAPPY)
        elif level == 1:
            dialogue = random.choice(DIALOGUES_HAPPY_2)
        else:
            dialogue = random.choice(DIALOGUES_LOVE)

        effect = STATE_BUBBLE_EFFECTS.get(state)
        self.set_state(state, duration=2500)
        self.show_bubble(dialogue, 2500, effect=effect)

    def on_wheel(self, event):
        old_scale = self.scale
        if event.delta > 0:
            self.scale = min(2.5, self.scale + 0.1)
        else:
            self.scale = max(0.3, self.scale - 0.1)
        if self.scale > old_scale:
            self.set_state(PetState.ZOOM, duration=800)
        elif self.scale < old_scale:
            self.set_state(PetState.TINY, duration=800)
        self.update_size()

    def trigger_interaction(self):
        if self.anim_running:
            return

        self.last_interaction_time = time.time()
        anim_list = ['jump', 'squash', 'shake', 'poke', 'tickle']
        self.anim_type = random.choice(anim_list)
        self.anim_frame = 0
        self.anim_running = True

        dialogue = random.choice(DIALOGUES_IDLE)
        if self.anim_type == 'jump':
            self.set_state(PetState.HAPPY, duration=2000)
            dialogue = random.choice(DIALOGUES_HAPPY)
        elif self.anim_type == 'squash':
            self.set_state(PetState.SURPRISED, duration=2000)
            dialogue = random.choice(DIALOGUES_SHOCKED)
        elif self.anim_type == 'shake':
            self.set_state(PetState.SHY, duration=2000)
            dialogue = random.choice(DIALOGUES_LOVE)
        elif self.anim_type == 'poke':
            self.set_state(PetState.POKED, duration=2000)
            dialogue = random.choice(DIALOGUES_POKE)
        elif self.anim_type == 'tickle':
            self.set_state(PetState.GIGGLE, duration=2000)
            dialogue = random.choice(DIALOGUES_TICKLE)

        effect = STATE_BUBBLE_EFFECTS.get(self.state)
        self.show_bubble(dialogue, effect=effect)
        self.animate()

    def animate(self):
        if not self.anim_running:
            return
        if self.anim_type == 'jump':
            self.anim_jump()
        elif self.anim_type == 'squash':
            self.anim_squash()
        elif self.anim_type == 'shake':
            self.anim_shake()
        elif self.anim_type in ('poke', 'tickle'):
            self.anim_poke()

    def anim_jump(self):
        frames = 24
        height = 25
        if self.anim_frame < frames // 2:
            t = self.anim_frame / (frames // 2)
            offset = -height * (2 * t - t * t)
        else:
            t = (self.anim_frame - frames // 2) / (frames // 2)
            offset = -height * (1 - t * t)

        y = self.base_y + self.img_h // 2 + int(offset)
        self.canvas.coords(self.character_id, self.img_w // 2, y)

        self.anim_frame += 1
        if self.anim_frame >= frames:
            self.end_interaction()
            return
        self.root.after(30, self.animate)

    def anim_squash(self):
        frames = 24
        max_squash = 0.75
        if self.anim_frame < frames // 2:
            t = self.anim_frame / (frames // 2)
            factor = 1 - (1 - max_squash) * t
        else:
            t = (self.anim_frame - frames // 2) / (frames // 2)
            factor = max_squash + (1 - max_squash) * t

        new_w = int(self.img_w / factor)
        new_h = int(self.img_h * factor)

        current_img = self.get_scaled_image(self.state)
        squashed = current_img.resize((new_w, new_h), Image.LANCZOS)
        alpha = squashed.getchannel('A')
        alpha = alpha.point(lambda a: 255 if a >= 128 else 0)
        squashed.putalpha(alpha)

        self.tk_image = ImageTk.PhotoImage(squashed)
        self.canvas.itemconfig(self.character_id, image=self.tk_image)

        y = self.base_y + self.img_h - new_h // 2
        self.canvas.coords(self.character_id, self.img_w // 2, y)

        self.anim_frame += 1
        if self.anim_frame >= frames:
            self.end_interaction()
            return
        self.root.after(30, self.animate)

    def anim_shake(self):
        frames = 18
        amplitude = 12
        if self.anim_frame < frames:
            t = self.anim_frame / frames
            current_amp = amplitude * (1 - t)
            offset = current_amp if self.anim_frame % 2 == 0 else -current_amp
            y = self.base_y + self.img_h // 2
            self.canvas.coords(self.character_id, self.img_w // 2 + int(offset), y)
        self.anim_frame += 1
        if self.anim_frame >= frames:
            self.end_interaction()
            return
        self.root.after(30, self.animate)

    def anim_poke(self):
        frames = 12
        if self.anim_frame < frames:
            t = self.anim_frame / frames
            offset = 5 * math.sin(t * math.pi * 2)
            y = self.base_y + self.img_h // 2
            self.canvas.coords(self.character_id, self.img_w // 2 + int(offset), y)
        self.anim_frame += 1
        if self.anim_frame >= frames:
            self.end_interaction()
            return
        self.root.after(30, self.animate)

    def end_interaction(self):
        self.anim_running = False
        self.update_display()

    def show_bubble(self, text, duration=2000, effect=None):
        self.hide_bubble()
        # 如果没有指定特效，根据当前状态自动匹配
        if effect is None:
            effect = STATE_BUBBLE_EFFECTS.get(self.state)

        # 气泡可用高度：从顶部 y=5 到角色顶部 base_y，留 8px 间距
        available_height = max(30, self.base_y - 5 - 8)

        # 字号自适应：从目标字号开始，若气泡高度超过可用空间则缩小
        target_font_size = max(10, int(12 * self.scale))
        font_size = target_font_size
        while font_size >= 9:
            result = self._layout_bubble(text, font_size, effect)
            if result['bubble_height'] <= available_height or font_size <= 9:
                break
            font_size -= 1
        else:
            font_size = 9
            result = self._layout_bubble(text, font_size, effect)

        x1 = result['x1']
        y1 = result['y1']
        x2 = result['x2']
        y2 = result['y2']
        lines = result['lines']
        bubble_height = result['bubble_height']
        line_height = result['line_height']
        padding_y = result['padding_y']

        self.bubble_id = self.canvas.create_rectangle(
            x1, y1, x2, y2, fill='white', outline='#555', width=2
        )
        # 逐行绘制文字，保证垂直居中且行距均匀
        self.bubble_text_ids = []
        text_y = y1 + padding_y + line_height // 2
        for line in lines:
            tid = self.canvas.create_text(
                (x1 + x2) // 2, text_y,
                text=line, fill='#333', font=('Microsoft YaHei', font_size)
            )
            self.bubble_text_ids.append(tid)
            text_y += line_height

        # 动态更新气泡高度，确保窗口预留空间足够
        self.bubble_height = max(40, bubble_height + 10)

        if effect and effect in BUBBLE_EFFECTS:
            effect_path = get_resource_path(BUBBLE_EFFECTS[effect])
            if os.path.exists(effect_path):
                effect_img = Image.open(effect_path).convert('RGBA')
                effect_size = int(30 * self.scale)
                effect_img = effect_img.resize((effect_size, effect_size), Image.LANCZOS)
                self.bubble_effect_img = ImageTk.PhotoImage(effect_img)
                self.bubble_effect_id = self.canvas.create_image(
                    x2 + 15, y1 + 5, image=self.bubble_effect_img
                )

        if self.bubble_timer:
            self.root.after_cancel(self.bubble_timer)
        self.bubble_timer = self.root.after(duration, self.hide_bubble)

        # 确保气泡显示在角色图片之上（后创建的在上，但 update_display 可能重建角色）
        if self.character_id:
            self.canvas.tag_raise(self.bubble_id)
            for tid in self.bubble_text_ids:
                self.canvas.tag_raise(tid)
            if self.bubble_effect_id:
                self.canvas.tag_raise(self.bubble_effect_id)

    def _layout_bubble(self, text, font_size, effect):
        """计算气泡布局：按窗口宽度自动换行，返回坐标和行列表"""
        bubble_font = tkfont.Font(family='Microsoft YaHei', size=font_size)
        effect_space = int(45 * self.scale) if (effect and effect in BUBBLE_EFFECTS) else 0
        max_text_width = max(80, self.img_w - 40 - effect_space)

        lines = []
        current_line = ""
        for ch in text:
            if ch == '\n':
                lines.append(current_line)
                current_line = ""
                continue
            test_line = current_line + ch
            if bubble_font.measure(test_line) > max_text_width and current_line:
                lines.append(current_line)
                current_line = ch
            else:
                current_line = test_line
        if current_line:
            lines.append(current_line)

        line_height = font_size + 6
        padding_x = 15
        padding_y = 8
        text_block_width = max(bubble_font.measure(line) for line in lines)
        text_block_height = len(lines) * line_height

        bubble_width = text_block_width + padding_x * 2
        bubble_height = text_block_height + padding_y * 2

        x1 = max(5, (self.img_w - bubble_width) // 2)
        y1 = 5
        x2 = x1 + bubble_width
        y2 = y1 + bubble_height

        return {
            'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2,
            'lines': lines, 'bubble_height': bubble_height,
            'line_height': line_height, 'padding_y': padding_y,
        }

    def hide_bubble(self):
        if self.bubble_id:
            self.canvas.delete(self.bubble_id)
            self.bubble_id = None
        for tid in self.bubble_text_ids:
            self.canvas.delete(tid)
        self.bubble_text_ids = []
        if self.bubble_effect_id:
            self.canvas.delete(self.bubble_effect_id)
            self.bubble_effect_id = None

    def show_menu(self, event):
        menu = Menu(self.root, tearoff=0)

        size_menu = Menu(menu, tearoff=0)
        size_menu.add_command(label="小", command=lambda: self.set_scale(0.6))
        size_menu.add_command(label="中", command=lambda: self.set_scale(1.0))
        size_menu.add_command(label="大", command=lambda: self.set_scale(1.5))
        menu.add_cascade(label="调整大小", menu=size_menu)

        view_menu = Menu(menu, tearoff=0)
        view_menu.add_command(label="原角度", command=lambda: self.set_view('side'))
        view_menu.add_command(label="正脸", command=lambda: self.set_view('front'))
        menu.add_cascade(label="切换视角", menu=view_menu)

        feed_menu = Menu(menu, tearoff=0)
        feed_menu.add_command(label="喂食", command=self.feed_eat)
        feed_menu.add_command(label="喂水", command=self.feed_drink)
        menu.add_cascade(label="投喂", menu=feed_menu)

        if self.chat_window:
            menu.add_command(label="查看聊天记录", command=self.chat_window.toggle)

        menu.add_command(label="取消置顶" if self.is_top else "置顶", command=self.toggle_top)
        menu.add_separator()
        menu.add_command(label="退出", command=self.quit_app)

        menu.post(event.x_root, event.y_root)

    def set_scale(self, scale):
        self.scale = scale
        self.update_size()

    def set_view(self, view_mode):
        if view_mode != self.view_mode:
            self.view_mode = view_mode
            self.update_size()
            self.show_bubble(f"切换到{'正脸' if view_mode == 'front' else '原角度'}视角~", 1500)

    def toggle_top(self):
        self.is_top = not self.is_top
        self.root.attributes('-topmost', self.is_top)

    def feed_eat(self):
        self.set_state(PetState.EAT, duration=3000)
        self.show_bubble(random.choice(DIALOGUES_EAT), 2500)
        self.last_interaction_time = time.time()

    def feed_drink(self):
        self.set_state(PetState.DRINK, duration=3000)
        self.show_bubble(random.choice(DIALOGUES_DRINK), 2500)
        self.last_interaction_time = time.time()

    def schedule_next_behavior(self):
        delay = random.randint(30000, 90000)
        self.behavior_timer = self.root.after(delay, self.trigger_random_behavior)

    def trigger_random_behavior(self):
        if self.state != PetState.IDLE or self.anim_running or self.transition_running:
            self.schedule_next_behavior()
            return

        available = [s for s in AUTONOMOUS_BEHAVIORS.keys() if s != PetState.SLEEP or self.is_night_time()]
        if not available:
            self.schedule_next_behavior()
            return

        behavior = random.choice(available)
        min_interval, max_interval, duration, dialogues = AUTONOMOUS_BEHAVIORS[behavior]

        self.set_state(behavior, duration=duration)
        if dialogues:
            effect = STATE_BUBBLE_EFFECTS.get(behavior)
            self.show_bubble(random.choice(dialogues), duration - 500, effect=effect)

        self.schedule_next_behavior()

    def is_night_time(self):
        hour = datetime.datetime.now().hour
        return hour >= 23 or hour < 6

    def schedule_time_check(self):
        self.time_check_timer = self.root.after(60000, self.check_time)

    def check_time(self):
        hour = datetime.datetime.now().hour
        current_time_state = None

        if 6 <= hour < 9:
            current_time_state = PetState.MORNING
        elif hour >= 23 or hour < 6:
            current_time_state = PetState.NIGHT

        if current_time_state and current_time_state != self.last_time_state:
            self.last_time_state = current_time_state
            if self.state == PetState.IDLE:
                self.set_state(current_time_state, duration=4000)
                effect = STATE_BUBBLE_EFFECTS.get(current_time_state)
                if current_time_state == PetState.MORNING:
                    self.show_bubble(random.choice(DIALOGUES_MORNING), 3500, effect=effect)
                else:
                    self.show_bubble(random.choice(DIALOGUES_NIGHT), 3500, effect=effect)

        self.schedule_time_check()

    def check_festival(self):
        today = datetime.datetime.now()
        month_day = (today.month, today.day)
        if month_day in FESTIVALS:
            state, dialogues = FESTIVALS[month_day]
            self.root.after(3000, lambda: self.set_state(state, duration=5000))
            self.root.after(3500, lambda: self.show_bubble(random.choice(dialogues), 4500))

    def check_birthday(self, birthday_month, birthday_day):
        """检查今天是否是用户生日，如果是则触发生日祝福"""
        today = datetime.datetime.now()
        if (today.month, today.day) == (birthday_month, birthday_day):
            self.root.after(4000, lambda: self.set_state(PetState.BIRTHDAY, duration=5000))
            self.root.after(4500, lambda: self.show_bubble(random.choice(DIALOGUES_BIRTHDAY), 4500))

    def quit_app(self):
        # 销毁内嵌输入框窗口
        if self.chat_input:
            self.chat_input.destroy()
        # 告别动画序列：bye -> cry -> 退出
        self.set_state(PetState.BYE, duration=1500)
        self.show_bubble("再见啦~宝宝~", 1500)
        self.root.after(1800, lambda: self.set_state(PetState.CRY, duration=1200))
        self.root.after(1800, lambda: self.show_bubble("呜呜，舍不得你...", 1200))
        self.root.after(3200, self.root.quit)

    def run(self):
        self.root.mainloop()


def main():
    pet = DesktopPet()
    pet.run()


if __name__ == "__main__":
    main()
