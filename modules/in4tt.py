from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import random
from datetime import datetime
import requests
from zlapi.models import Message
import io

des = {
    'version': "1.0.2",
    'credits': "Nguyễn Đức Tài",
    'description': "Xem toàn bộ lệnh hiện có của bot"
}

# Đường dẫn font
FONT_TEXT_PATH = "font/arial.ttf"  # Font chữ chính
FONT_ICON_PATH = "font/NotoEmoji-Bold.ttf"  # Font chứa icon

BACKGROUND_DIR = "background/"

def get_random_background():
    """Chọn ngẫu nhiên một ảnh nền từ thư mục background."""
    if not os.path.exists(BACKGROUND_DIR):
        return None
    images = [f for f in os.listdir(BACKGROUND_DIR) if f.endswith((".png", ".jpg", ".jpeg"))]
    return os.path.join(BACKGROUND_DIR, random.choice(images)) if images else None

def create_image():
    """Tạo ảnh menu bot với icon nằm cả trước và sau chữ"""
    image_path = get_random_background()
    if not image_path:
        print("❌ Không tìm thấy ảnh nền!")
        return None

    try:
        size = (1124, 450)
        box_color = (255, 255, 255, 180)  # Trắng trong suốt
        text_color = (255, 105, 180)  # Hồng

        # Mở ảnh nền, resize và làm mờ
        bg_image = Image.open(image_path).convert("RGBA").resize(size).filter(ImageFilter.GaussianBlur(8))

        # Tạo overlay hộp trong suốt
        overlay = Image.new("RGBA", size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        draw.rounded_rectangle([(150, 80), (size[0] - 150, size[1] - 100)], radius=35, fill=box_color)
        bg_image = Image.alpha_composite(bg_image, overlay)

        # Load font chữ chính và font icon
        try:
            font_text = ImageFont.truetype(FONT_TEXT_PATH, 40)
            font_icon = ImageFont.truetype(FONT_ICON_PATH, 40)
            date_font = ImageFont.truetype(FONT_TEXT_PATH, 35)
        except Exception as e:
            print(f"❌ Lỗi tải font: {e}")
            return None

        # Danh sách text (icon trước và sau chữ)
        text_lines = [
            ("💡", "Xin chào, tôi là Minh Vũ", "💡"),
            ("📜", "Đây là lệnh i4tt của bot", "📜"),
            ("🤖", "Bot: Music | M.Vũ Yêu M.Anh", "🤖"),
            ("🎧", "Hãy fl _m.vu210_", "🎧")  # Dòng thêm mới
        ]

        # Tính toán vị trí chữ trong hộp
        text_height = len(text_lines) * 50
        start_y = (80 + size[1] - 100 - text_height) // 2
        draw = ImageDraw.Draw(bg_image)

        for icon_start, text, icon_end in text_lines:
            icon_width_start = draw.textlength(icon_start, font=font_icon)
            text_width = draw.textlength(text, font=font_text)
            icon_width_end = draw.textlength(icon_end, font=font_icon)
            
            total_width = icon_width_start + text_width + icon_width_end + 20
            x_pos = (size[0] - total_width) // 2

            # Vẽ icon trước
            draw.text((x_pos, start_y), icon_start, font=font_icon, fill=text_color)

            # Vẽ chữ giữa hai icon
            draw.text((x_pos + icon_width_start + 10, start_y), text, font=font_text, fill=text_color)

            # Vẽ icon sau
            draw.text((x_pos + icon_width_start + text_width + 20, start_y), icon_end, font=font_icon, fill=text_color)

            start_y += 50  # Dãn dòng

        # Hiển thị ngày giờ (góc phải, bên ngoài hộp)
        now = datetime.now().strftime("%d/%m/%Y - %H:%M")
        date_width = draw.textlength(now, font=date_font)
        draw.text((size[0] - date_width - 30, size[1] - 60), now, font=date_font, fill=text_color)

        # Lưu ảnh vào bộ nhớ
        img_bytes = io.BytesIO()
        bg_image.convert("RGB").save(img_bytes, format='PNG')
        img_bytes.seek(0)

        return img_bytes

    except Exception as e:
        print(f"❌ Lỗi tạo ảnh: {e}")
        return None

def i4tt(message, message_object, thread_id, thread_type, author_id, client):
    content = message.strip().split()

    if len(content) < 2:
        client.replyMessage(Message(text="❌ Vui lòng nhập tên người dùng TikTok hợp lệ."), message_object, thread_id, thread_type)
        return

    tiktok_username = content[1].strip()
    api_url = f"https://api.sumiproject.net/tiktok?info={tiktok_username}"

    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if 'data' not in data or 'user' not in data['data']:
            client.replyMessage(Message(text="⚠ Không tìm thấy thông tin tài khoản TikTok."), message_object, thread_id, thread_type)
            return

        user_data = data['data']['user']
        stats_data = data['data']['stats']

        nickname = user_data.get('nickname', 'Không có')
        followers = f"{stats_data.get('followerCount', 0):,}"
        following = f"{stats_data.get('followingCount', 0):,}"
        video_count = f"{stats_data.get('videoCount', 0):,}"
        heart_count = f"{stats_data.get('heartCount', 0):,}"
        bio = user_data.get('signature', 'Không có')

        # Gửi tin nhắn văn bản riêng về follow TikTok
        client.replyMessage(Message(text="🎶 Hãy fl _m.vu210_ 🎶 ❤️ Cảm ơn bạn đã ủng hộ!"), message_object, thread_id, thread_type)

        # Tạo ảnh menu bot
        img_bytes = create_image()

        # Tin nhắn chi tiết thông tin TikTok
        msg = (
            f"📌 Thông tin TikTok của @{tiktok_username}\n"
            f"👤 Tên TikTok: {nickname}\n"
            f"📊 Followers: {followers}\n"
            f"👥 Đang Follow: {following}\n"
            f"🎥 Số video: {video_count}\n"
            f"❤️ Lượt thích: {heart_count}\n"
            f"📝 Tiểu sử: {bio}\n"
            f"👑 Creator: Minh Vũ"
        )

        client.replyMessage(Message(text=msg), message_object, thread_id, thread_type)

        # Gửi ảnh
        if img_bytes:
            client.sendImage(img_bytes, thread_id, thread_type)

    except Exception as e:
        client.replyMessage(Message(text=f"💢 Đã xảy ra lỗi: {str(e)}"), message_object, thread_id, thread_type)

def get_szl():
    return {
        'i4tt': i4tt
    }