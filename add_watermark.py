import os
import re
from PIL import Image, ImageDraw, ImageFont

def parse_description(text):
    """
    解析描述文本,提取时间、日期、星期、天气、温度、地点
    例如: "2023年5月5日   星期五  10:28     晴   28°   西安市长安区王莽街办二里村"
    """
    # 提取日期 (YYYY年MM月DD日)
    date_match = re.search(r'(\d{4}年\d{1,2}月\d{1,2}日)', text)
    date = date_match.group(1) if date_match else ""

    # 提取星期
    week_match = re.search(r'(星期[一二三四五六日天])', text)
    week = week_match.group(1) if week_match else ""

    # 提取时间 (HH:MM 或 上午HH点MM分 等格式)
    time_match = re.search(r'(\d{1,2}:\d{2})', text)
    if time_match:
        time = time_match.group(1)
    else:
        # 尝试匹配 "上午11点27分" 这种格式
        time_match2 = re.search(r'(上午|下午)(\d{1,2})点(\d{1,2})分', text)
        if time_match2:
            period, hour, minute = time_match2.groups()
            time = f"{hour}:{minute}"
        else:
            time = ""

    # 提取天气
    weather_match = re.search(r'(晴|阴|雨|雪|多云|阴天)', text)
    weather = weather_match.group(1) if weather_match else ""

    # 提取温度
    temp_match = re.search(r'(\d{1,2})°', text)
    temp = temp_match.group(0) if temp_match else ""
    if temp and not temp.endswith('℃'):
        temp = temp.replace('°', '℃')

    # 提取地点 (通常在最后,包含"地点为:"或直接是地址)
    location = ""
    # 先移除已匹配的部分
    remaining = text
    if date:
        remaining = remaining.replace(date, '')
    if week:
        remaining = remaining.replace(week, '')
    if time_match:
        remaining = remaining.replace(time_match.group(0), '')
    if weather:
        remaining = remaining.replace(weather, '')
    if temp_match:
        remaining = remaining.replace(temp_match.group(0), '')

    # 清理地点文本
    location = remaining.strip()
    location = re.sub(r'地点为[::]', '', location)
    location = re.sub(r'\s+', '', location)  # 移除多余空格

    return {
        'time': time,
        'date': date,
        'week': week,
        'weather': weather,
        'temp': temp,
        'location': location
    }

def add_watermark():
    work_dir = r"c:\Users\Administrator\Desktop\照片"
    desc_file = os.path.join(work_dir, "描述.txt")

    # Read descriptions
    descriptions = {}
    try:
        with open(desc_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        with open(desc_file, 'r', encoding='gbk') as f:
            lines = f.readlines()

    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Parse line like "1. 2023..."
        parts = line.split('.', 1)
        if len(parts) == 2:
            try:
                idx = int(parts[0].strip())
                text = parts[1].strip()
                descriptions[idx] = text
            except ValueError:
                continue

    print(f"Found descriptions for images: {list(descriptions.keys())}")

    # Font settings
    font_path = "C:/Windows/Fonts/msyhbd.ttc"  # 微软雅黑粗体
    if not os.path.exists(font_path):
        font_path = "C:/Windows/Fonts/msyh.ttc"
    if not os.path.exists(font_path):
        font_path = "C:/Windows/Fonts/simhei.ttf"

    for idx, text in descriptions.items():
        img_name = f"{idx}.jpg"
        img_path = os.path.join(work_dir, img_name)

        if not os.path.exists(img_path):
            print(f"Image {img_name} not found.")
            continue

        try:
            # 解析描述信息
            info = parse_description(text)
            print(f"\n处理图片 {idx}: {info}")

            # 打开原图
            img = Image.open(img_path).convert('RGBA')
            width, height = img.size

            # 创建一个透明层用于绘制
            overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(overlay)

            # 根据图片高度自适应字体大小
            font_size_large = int(height * 0.05)   # 大字:时间和日期
            font_size_medium = int(height * 0.03)  # 中字:星期天气温度
            font_size_small = int(height * 0.025)  # 小字:地点

            try:
                font_large = ImageFont.truetype(font_path, font_size_large)
                font_medium = ImageFont.truetype(font_path, font_size_medium)
                font_small = ImageFont.truetype(font_path, font_size_small)
            except Exception as e:
                print(f"字体加载失败 {font_path}: {e}")
                font_large = font_medium = font_small = ImageFont.load_default()

            # 构建三行文本
            line1 = f"{info['time']} | {info['date']}"  # 第一行:时间 | 日期
            line2 = f"{info['week']} {info['weather']} {info['temp']}"  # 第二行:星期 天气 温度
            line3 = info['location']  # 第三行:地点

            # 计算每行文本的尺寸
            bbox1 = draw.textbbox((0, 0), line1, font=font_large)
            bbox2 = draw.textbbox((0, 0), line2, font=font_medium)
            bbox3 = draw.textbbox((0, 0), line3, font=font_small)

            text_width1 = bbox1[2] - bbox1[0]
            text_height1 = bbox1[3] - bbox1[1]
            text_width2 = bbox2[2] - bbox2[0]
            text_height2 = bbox2[3] - bbox2[1]
            text_width3 = bbox3[2] - bbox3[0]
            text_height3 = bbox3[3] - bbox3[1]

            # 计算最大文本宽度
            max_text_width = max(text_width1, text_width2, text_width3)

            # 内边距
            padding = int(width * 0.015)
            line_spacing = int(height * 0.008)

            # 计算背景框的尺寸和位置
            bg_width = max_text_width + padding * 2
            bg_height = text_height1 + text_height2 + text_height3 + line_spacing * 2 + padding * 2

            # 背景框位置(左下角)
            bg_x = int(width * 0.02)
            bg_y = height - bg_height - int(height * 0.02)

            # 绘制半透明深色背景框 (颜色参考样本图: RGB(19,19,20), 透明度约180)
            draw.rectangle(
                [(bg_x, bg_y), (bg_x + bg_width, bg_y + bg_height)],
                fill=(19, 19, 20, 180)
            )

            # 绘制文本(白色)
            text_color = (255, 255, 255, 255)

            # 第一行:时间和日期(大字)
            y_pos = bg_y + padding
            draw.text((bg_x + padding, y_pos), line1, font=font_large, fill=text_color)

            # 第二行:星期 天气 温度(中字)
            y_pos += text_height1 + line_spacing
            draw.text((bg_x + padding, y_pos), line2, font=font_medium, fill=text_color)

            # 第三行:地点(小字)
            y_pos += text_height2 + line_spacing
            draw.text((bg_x + padding, y_pos), line3, font=font_small, fill=text_color)

            # 合并图层
            img = Image.alpha_composite(img, overlay)

            # 转换回RGB保存
            img = img.convert('RGB')

            # 保存为新文件
            output_path = os.path.join(work_dir, f"{idx}_marked.jpg")
            img.save(output_path, quality=95)
            print(f"Processed {img_name} -> {os.path.basename(output_path)}")

        except Exception as e:
            print(f"Failed to process {img_name}: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    add_watermark()
