from zlapi.models import Message
import requests
import os
from PIL import Image
from io import BytesIO

des = {
    'version': "1.0.2",
    'credits': "Minh Vũ",
    'description': "Check Đồ Ff "
}

def handle_doff_command(message, message_object, thread_id, thread_type, author_id, client):
    parts = message.strip().split()

    if len(parts) < 2:
        client.sendMessage(
            Message(text="❌ Thiếu UID!\n\n📌 **Cách dùng:**\n`-doff <uid>`\n\nVí dụ: `-doff 12345678`"),
            thread_id, thread_type
        )
        return

    uid = parts[1]
    region = "SG"

    try:
        outfit_url = f"https://aditya-outfit-v11op.onrender.com/outfit-image?uid={uid}&region={region.lower()}"

        # Tải ảnh từ URL
        res = requests.get(outfit_url, stream=True)
        if res.status_code != 200:
            client.sendMessage(
                Message(text="❌ Không thể lấy ảnh outfit. UID sai hoặc server lỗi."),
                thread_id, thread_type
            )
            return

        # Mở ảnh từ bytes
        image = Image.open(BytesIO(res.content)).convert("RGB")
        temp_path = f"modules/cache/outfit_{uid}.jpg"
        image.save(temp_path, format='JPEG')

        # Gửi ảnh qua Zalo
        client.sendLocalImage(temp_path, thread_id=thread_id, thread_type=thread_type, width=image.width, height=image.height)

        # Xoá file tạm
        if os.path.exists(temp_path):
            os.remove(temp_path)

    except Exception as e:
        client.sendMessage(
            Message(text=f"⚠️ Có lỗi xảy ra khi xử lý: {e}"),
            thread_id, thread_type
        )

def get_szl():
    return {
        'doff': handle_doff_command  # Lenh gui anh outfit rieng
    }