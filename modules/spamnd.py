from zlapi.models import Message
import json
import os
import requests
import time
from config import ADMIN  # Import danh sách admin từ config.py

des = {
    'version': "1.0.2",
    'credits': "Dzi x Mode",
    'description': "Chuyển đổi văn bản thành voice"
}

def handle_spamnd_command(message, message_object, thread_id, thread_type, author_id, client):
    # Kiểm tra xem người gửi có phải là admin không
    if author_id not in ADMIN:
        send_error_message(thread_id, thread_type, client, "Đây là lệnh sử dụng tag Admin.")
        return

    content = message_object.content.strip()
    command_parts = content.split(maxsplit=1)

    if len(command_parts) < 2:
        send_error_message(thread_id, thread_type, client, "⚠️💡 Hướng Dẫn: Vui lòng nhập nội dung và số lần spam.\nVí dụ: `spamnd Con mẹ mày,10`")
        return

    try:
        text, times = command_parts[1].rsplit(",", 1)
        text = text.strip()
        times = int(times.strip())
    except (ValueError, IndexError):
        send_error_message(thread_id, thread_type, client, "❗❓ Lỗi Cú Pháp: Ví dụ đúng: `spamnd Con mẹ mày,10`")
        return

    if not text:
        send_error_message(thread_id, thread_type, client, "⚠️📝 Lỗi: Nội dung không được để trống.")
        return

    if times <= 0 or times > 10000000000:
        send_error_message(thread_id, thread_type, client, "🚧🔢 Giới Hạn: Số lần spam phải từ 1 đến 10000000000000.")
        return

    # Thực hiện spam ngay lập tức
    for _ in range(times):
        client.send(Message(text=text), thread_id=thread_id, thread_type=thread_type)
        time.sleep(0.1)  # Thêm thời gian delay giữa mỗi lần gửi tin nhắn (2 giây)

    success_message = f" "
    client.send(Message(text=success_message), thread_id=thread_id, thread_type=thread_type)

def send_error_message(thread_id, thread_type, client, error_message="❌💥 Lỗi Hệ Thống!"):
    client.send(Message(text=error_message), thread_id=thread_id, thread_type=thread_type)

def process_message(message_object, thread_id, thread_type, author_id, client):
    content = message_object.content.strip()
    command_parts = content.split(maxsplit=1)
    command = command_parts[0].lower()
    commands = get_mitaizl()
    
    if command in commands:
        commands[command](message_object, thread_id, thread_type, author_id, client)
    else:
        send_error_message(thread_id, thread_type, client, "❓🔍 Lệnh Không Hợp Lệ!")

def get_szl():
    return {
        'spamnd': handle_spamnd_command  # Thay đổi từ 'spvc' sang 'spamnd'
    }