import os
import random
import importlib
import requests
from datetime import datetime
from io import BytesIO
from zlapi.models import *
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from config import PREFIX

des = {
    'version': "1.0.2",
    'credits': "Minh Vũ ",
    'description': "Menu Ảnh Loại Fake A Sìn 90% Đời Đầu"
}

# Định nghĩa thư mục và font
BACKGROUND_DIR = "background/"
MODULES_DIR = "modules/"
FONT_PATH_ICON = "font/NotoEmoji-Bold.ttf"
FONT_PATH_TEXT = "font/arial.ttf"
COMMANDS_PER_PAGE = 10

# Hàm lấy ảnh nền ngẫu nhiên
def get_random_background():
    if not os.path.exists(BACKGROUND_DIR):
        return None
    images = [f for f in os.listdir(BACKGROUND_DIR) if f.endswith((".png", ".jpg", ".jpeg"))]
    return os.path.join(BACKGROUND_DIR, random.choice(images)) if images else None

# Hàm tạo màu nhạt ngẫu nhiên (loại trừ màu đen)
def random_light_color_exclude_black():
    colors = [(255, 182, 193), (173, 216, 230), (144, 238, 144), (255, 255, 224), (255, 250, 250)]
    return random.choice(colors)

# Hàm vẽ icon ngẫu nhiên trong chữ
def draw_random_icon(draw, position, font_size=50):
    icons = ["🎵", "💖", "🎧", "🔥", "🌟", "🎼", "🎶", "💡", "🔊", "🤖"]
    icon = random.choice(icons)
    font_icon = ImageFont.truetype(FONT_PATH_ICON, font_size)
    draw.text(position, icon, font=font_icon, fill=(255, 20, 147))

# Hàm vẽ icon to phía ngoài hộp (bên phải hộp)
def draw_large_random_icon(draw, box_x2, box_y1, box_y2, font_size=100):
    icons = ["🎵", "💖", "🎧", "🔥", "📄", "🇻🇳", "🤖"]
    icon = random.choice(icons)
    font_icon = ImageFont.truetype(FONT_PATH_ICON, font_size)

    # Vị trí icon: bên phải hộp, giữa chiều cao của hộp
    icon_x = box_x2 + 20  # Cách hộp 20px
    icon_y = (box_y1 + box_y2 - font_size) // 2  # Canh giữa theo chiều dọc

    draw.text((icon_x, icon_y), icon, font=font_icon, fill=(255, 255, 255))

# Hàm tạo ảnh menu bot
def draw_menu_image(output_path, avatar_url):
    image_path = get_random_background()
    if not image_path:
        print("❌ Không tìm thấy ảnh nền!")
        return None
    
    try:
        size = (1124, 452)
        box_color = (*random_light_color_exclude_black(), 180)
        text_color = (255, 20, 147)

        # Tạo ảnh nền
        bg_image = Image.open(image_path).convert("RGBA")
        bg_image = bg_image.resize(size)
        bg_image = bg_image.filter(ImageFilter.GaussianBlur(8))

        # Tạo hộp trong suốt
        overlay = Image.new("RGBA", size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        box_x1, box_y1 = 150, 80
        box_x2, box_y2 = size[0] - 150, size[1] - 80
        draw.rounded_rectangle([(box_x1, box_y1), (box_x2, box_y2)], radius=35, fill=box_color)

        bg_image = Image.alpha_composite(bg_image, overlay)
        draw = ImageDraw.Draw(bg_image)

        # Vẽ icon to bên phải hộp
        draw_large_random_icon(draw, box_x2, box_y1, box_y2)

        # Vẽ chữ
        font_text = ImageFont.truetype(FONT_PATH_TEXT, 40)
        date_font = ImageFont.truetype(FONT_PATH_TEXT, 35)

        text_lines = [
            "Xin chào, tôi là Minh Vũ",
            "Tôi có thể giúp gì cho bạn?",
            "Đây là menu lệnh của bot",
            "Bot : Music | Fb Minh Vũ (Music)"
        ]

        text_height = len(text_lines) * 50
        start_y = (box_y1 + box_y2 - text_height) // 2

        # Vẽ icon ngẫu nhiên trên đầu menu
        draw_random_icon(draw, (50, 30), font_size=60)

        for idx, line in enumerate(text_lines):
            x_pos = (size[0] - draw.textlength(line, font=font_text)) // 2
            draw_random_icon(draw, (x_pos - 60, start_y))  # Icon bên trái
            draw.text((x_pos, start_y), line, font=font_text, fill=text_color)
            draw_random_icon(draw, (x_pos + draw.textlength(line, font=font_text) + 10, start_y))  # Icon bên phải
            start_y += 50

        # Vẽ ngày giờ
        now = datetime.now().strftime("%d/%m/%Y - %H:%M")
        date_width = draw.textlength(now, font=date_font)
        date_x = (size[0] - date_width) // 2
        draw.text((date_x, box_y2 - 40), now, font=date_font, fill=text_color)

        # Vẽ avatar lên ảnh menu
        avatar = load_image_from_url(avatar_url).convert("RGBA")
        avatar = avatar.resize((170, 170), Image.LANCZOS)

        mask = Image.new("L", avatar.size, 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.ellipse((0, 0, 170, 170), fill=255)

        avatar = Image.composite(avatar, Image.new("RGBA", avatar.size), mask)
        bg_image.paste(avatar, (50, 50), avatar)

        # Lưu ảnh
        bg_image = bg_image.convert("RGB")
        bg_image.save(output_path)
        return output_path
    except Exception as e:
        print(f"❌ Lỗi tạo ảnh: {e}")
        return None

# Hàm tải ảnh từ URL
def load_image_from_url(url):
    response = requests.get(url)
    return Image.open(BytesIO(response.content))

# Hàm lấy danh sách lệnh từ modules
def get_all_szl():
    szl = {}
    for module_name in os.listdir(MODULES_DIR):
        if module_name.endswith('.py') and module_name != '__init__.py':
            module_path = f'modules.{module_name[:-3]}'
            module = importlib.import_module(module_path)

            if hasattr(module, 'get_szl'):
                module_szl = module.get_szl()
                szl.update(module_szl)
    
    return list(szl.keys())

# Hàm xử lý lệnh menu
def handle_menu_command(message, message_object, thread_id, thread_type, author_id, bot):
    commands = get_all_szl()
    total_pages = (len(commands) + COMMANDS_PER_PAGE - 1) // COMMANDS_PER_PAGE

    parts = message.split()
    page = 1
    if len(parts) > 1 and parts[1].isdigit():
        page = int(parts[1])

    if page < 1 or page > total_pages:
        bot.send(Message(text=f"⚠ Trang không hợp lệ! Chọn từ 1 đến {total_pages}."), thread_id=thread_id, thread_type=thread_type)
        return

    start_index = (page - 1) * COMMANDS_PER_PAGE
    end_index = start_index + COMMANDS_PER_PAGE
    commands_page = commands[start_index:end_index]

    user_avatar_url = bot.fetchUserInfo(author_id).changed_profiles[author_id].avatar
    intro_image_path = "intro_menu.jpg"
    image_path = draw_menu_image(intro_image_path, user_avatar_url)

    command_list_text = "\n".join([f"- {cmd}" for cmd in commands_page])
    message_text = f"📜 **Danh sách lệnh (Trang {page}/{total_pages})**:\n\n{command_list_text}\n\n🔄 Nhập `menu [số trang]` để chuyển"

    if image_path:
        bot.sendLocalImage(
            message=Message(text=message_text),
            imagePath=image_path,
            thread_id=thread_id,
            thread_type=thread_type,
            width=1124,
            height=452,
            ttl=500000
        )
    else:
        bot.send(Message(text="❌ Không thể tạo ảnh menu. Kiểm tra thư mục background hoặc font chữ."), thread_id=thread_id, thread_type=thread_type)

# Hàm trả về dict các lệnh trong module
def get_szl():
    return {'menu': handle_menu_command}