"""情感标签解析模块：将 AI 返回的情感标签映射到宠物表情状态"""


class EmotionParser:
    """解析 AI 回复中的情感标签，返回对应的表情状态和气泡特效"""

    # 情感标签 -> (主表情状态, 备选表情状态, 气泡特效)
    EMOTION_MAP = {
        'happy':     ('happy', 'happy_2', 'music'),
        'love':      ('love', 'blush_light', None),
        'sad':       ('sad', 'head_down', 'silence'),
        'angry':     ('annoyed', 'angry', 'exclaim'),
        'surprised': ('surprised', 'shocked', 'exclaim'),
        'think':     ('think', 'chin', 'question'),
        'shy':       ('shy', 'blush', None),
        'smug':      ('smug', 'tsundere', None),
        'bored':     ('bored', 'slump', 'silence'),
        'serious':   ('serious', 'lecture', None),
        'neutral':   ('idle', 'idle', None),
    }

    DEFAULT_EMOTION = 'neutral'

    @classmethod
    def parse(cls, raw_text):
        """
        解析 AI 返回的原始文本，提取情感标签和回复内容。

        期望格式：
            [emotion_tag]
            回复内容...

        返回：
            (emotion_tag, reply_text)
        """
        if not raw_text:
            return cls.DEFAULT_EMOTION, "..."

        text = raw_text.strip()

        # 尝试解析 [tag] 格式
        if text.startswith('['):
            end = text.find(']')
            if end > 0:
                tag = text[1:end].strip().lower()
                reply = text[end + 1:].strip()
                if tag in cls.EMOTION_MAP:
                    return tag, reply if reply else "..."
                # 标签不在映射表中，尝试模糊匹配
                for key in cls.EMOTION_MAP:
                    if key in tag:
                        return key, reply if reply else "..."
                return cls.DEFAULT_EMOTION, reply if reply else text

        # 没有标签，尝试从内容推断情感
        return cls._guess_emotion(text), text

    @classmethod
    def get_state_and_effect(cls, emotion_tag, use_alt=False):
        """
        根据情感标签返回 (表情状态字符串, 气泡特效)。
        use_alt=True 时返回备选表情（用于连续相同情感时切换）。
        """
        entry = cls.EMOTION_MAP.get(emotion_tag, cls.EMOTION_MAP[cls.DEFAULT_EMOTION])
        state = entry[1] if use_alt else entry[0]
        effect = entry[2]
        return state, effect

    @classmethod
    def _guess_emotion(cls, text):
        """从文本内容猜测情感（简单关键词匹配）"""
        text_lower = text.lower()

        happy_kw = ['开心', '高兴', '哈哈', '嘻嘻', '嘿嘿', '太好了', '棒', '耶']
        love_kw = ['喜欢', '爱', '比心', '心动', '亲亲']
        sad_kw = ['难过', '伤心', '呜呜', '哭', '委屈', '不开心']
        angry_kw = ['生气', '哼', '讨厌', '烦', '不理', '怒']
        surprised_kw = ['什么', '真的吗', '不会吧', '惊讶', '哇', '?!', '！？']
        think_kw = ['想想', '思考', '嗯...', '让我看', '考虑']
        shy_kw = ['害羞', '脸红', '不好意思', '羞']
        smug_kw = ['得意', '厉害', '不愧', '骄傲', '怎样']
        bored_kw = ['无聊', '发呆', '没事', '闲']

        for kw in happy_kw:
            if kw in text_lower:
                return 'happy'
        for kw in love_kw:
            if kw in text_lower:
                return 'love'
        for kw in sad_kw:
            if kw in text_lower:
                return 'sad'
        for kw in angry_kw:
            if kw in text_lower:
                return 'angry'
        for kw in surprised_kw:
            if kw in text_lower:
                return 'surprised'
        for kw in think_kw:
            if kw in text_lower:
                return 'think'
        for kw in shy_kw:
            if kw in text_lower:
                return 'shy'
        for kw in smug_kw:
            if kw in text_lower:
                return 'smug'
        for kw in bored_kw:
            if kw in text_lower:
                return 'bored'

        return cls.DEFAULT_EMOTION
