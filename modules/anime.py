from zlapi.models import MultiMsgStyle, MessageStyle
import os
import json
import requests
from zlapi.models import Message
import time
import random  
des = {
    'version': "1.0.0",
    'credits': "Xuân Bách",
    'description': "Anh anime"
}


def fetch_image_with_retry(url, retries=3, delay=2):
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_8_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6.6 Mobile/15E148 Safari/604.1'
    }
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response  
        except requests.exceptions.RequestException as e:
            if attempt < retries - 1: 
                time.sleep(delay)
            else: 
                raise e

def handle_anime_command(message, message_object, thread_id, thread_type, author_id, client):
    try:
      
        with open('Api/anime.json', 'r', encoding='utf-8') as json_file:
            image_data = json.load(json_file)

        # Lấy URL ngẫu nhiên từ danh sách
        if image_data and isinstance(image_data, list):
            image_url = random.choice(image_data)  # Random URL từ danh sách

            # Tải ảnh từ URL với retry
            img_response = fetch_image_with_retry(image_url)
            img_filename = 'temp_image.jpg'
            with open(img_filename, 'wb') as img_file:
                img_file.write(img_response.content)

            # Gửi ảnh qua Zalo
            client.sendLocalImage(img_filename, thread_id=thread_id, thread_type=thread_type)

            # Phản hồi thành công
            # success_text = f"Đã gửi ảnh ngẫu nhiên từ danh sách!"
            # style_success = MultiMsgStyle([
            #     MessageStyle(offset=0, length=len(success_text), style="color", color="#00ff00", auto_format=False),
            # ])
            # client.replyMessage(Message(text=success_text, style=style_success), message_object, thread_id=thread_id, thread_type=thread_type)

            # Xóa ảnh tạm
            os.remove(img_filename)
        else:
            raise ValueError("Danh sách URL trong JSON rỗng hoặc không hợp lệ.")
    except Exception as e:
        # Phản hồi lỗi
        error_text = f"Lỗi: {str(e)}"
        style_error = MultiMsgStyle([
            MessageStyle(offset=0, length=len(error_text), style="color", color="#ff5555", auto_format=False),
        ])
        client.replyMessage(Message(text=error_text, style=style_error), message_object, thread_id=thread_id, thread_type=thread_type)

def get_szl():
    return {
        'anime': handle_anime_command
    }
