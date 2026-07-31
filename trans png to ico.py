from PIL import Image
import os

def convert_png_to_ico(png_path, output_path="src/icon.ico"):
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # 打开并转换
    img = Image.open(png_path)

    # 转为 RGBA（支持透明背景）
    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    # 生成多尺寸 ICO（Windows 会自动选择合适尺寸）
    icon_sizes = [(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)]
    img.save(output_path, format='ICO', sizes=icon_sizes)
    print(f"✅ 图标已生成: {output_path}")
    print(f"   包含尺寸: {icon_sizes}")

# 使用示例：把你的 PNG 路径填在这里
convert_png_to_ico("C:\pets\dist\character_blush_light.png")
