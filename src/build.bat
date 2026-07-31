@echo off
chcp 65001 >nul
echo 正在打包桌宠程序，请稍候...
python -m PyInstaller --onefile --windowed --name "沈不渝桌宠" --icon=icon.ico --distpath "..\dist" --hidden-import=tkinter --hidden-import=PIL --hidden-import=PIL.Image --hidden-import=PIL.ImageTk --hidden-import=requests --hidden-import=chat_window --hidden-import=chat_input --hidden-import=ai_client --hidden-import=emotion_parser --hidden-import=chat_history main_tk.py
if errorlevel 1 (
    echo 打包失败！
    pause
    exit /b 1
)
echo.
echo 正在复制资源文件到 dist 目录...
copy /Y "assets\character*.png" "..\dist\" >nul
copy /Y "config.json" "..\dist\" >nul
echo.
echo 正在清理构建缓存...
rmdir /S /Q "build" 2>nul
rmdir /S /Q "__pycache__" 2>nul
del /Q "*.spec" 2>nul
echo.
echo 打包完成！请查看项目根目录的 dist 文件夹
echo 提示：dist 目录中的 沈不渝桌宠.exe、config.json 和所有 character*.png 文件需一起分发
pause
