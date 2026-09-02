# 沈不渝桌面宠物

一个用 Python 编写的 Windows 桌面宠物程序，主角是动漫角色"沈不渝"，支持 AI 聊天、表情互动、节日祝福等功能。

## 目录结构

```
c:/pets/
├── src/                     # 源代码（开发用）
│   ├── main_tk.py           # 主程序（Tkinter）
│   ├── ai_client.py         # 通义千问 API 封装
│   ├── chat_window.py       # 聊天窗口 UI
│   ├── chat_history.py      # 对话历史管理
│   ├── emotion_parser.py    # 情感标签解析
│   ├── config.json          # 配置文件（API Key 等）
│   ├── build.bat            # 一键打包脚本
│   └── assets/              # 图片资源（81 张表情素材）
│
├── dist/                    # 发布目录（可直接分发）
│   ├── 沈不渝桌宠.exe       # 可执行程序
│   ├── config.json          # 配置文件
│   └── character*.png       # 81 张表情图片
│
├── character.md             # 角色设定文档
└── README.md                # 本文件
```

## 功能特性

- 55 种表情状态，双视角（侧面/正面）切换
- 呼吸动画 + 眨眼动画
- 点击互动（跳跃/压扁/摇晃/戳/挠痒）
- 双击打开 AI 聊天窗口（通义千问）
- AI 回复自动匹配表情和气泡特效
- 自主行为（打哈欠、伸懒腰、发呆、睡觉等 17 种）
- 时间感知（早晨/深夜问候）
- 节日检测（新年/万圣节/圣诞节/生日）
- 情绪递进系统（连续互动触发不同等级）
- 投喂互动（喂食/喂水）
- 对话历史按天保存

## 快速开始

### 用户使用
1. 进入 `dist/` 目录
2. 在 `config.json` 中填入通义千问 API Key
3. 双击 `沈不渝桌宠.exe` 运行

### 开发运行
```bash
cd src
pip install Pillow requests
python main_tk.py
```

### 打包发布
```bash
cd src
build.bat
```
打包完成后，`dist/` 目录中包含所有发布文件。

## 技术栈

- Python 3.x / Tkinter / Pillow / requests / PyInstaller

## API 配置

在 `config.json` 中填写：
```json
{
  "api_key": "你的API Key",
  "model": "qwen-turbo",
  "max_history": 20
}
```
获取 API Key：https://dashscope.console.aliyun.com/
