from zlapi.models import Message
import time
import requests
import os

des = {
    'version': "1.0.2",
    'credits': "Nguyễn Phi Hoàng",
    'description': "Xem thời gian bot Hoạt Động"
}

start_time = time.time()

def handle_uptime_command(message, message_object, thread_id, thread_type, author_id, client):
    current_time = time.time()
    upt_seconds = int(current_time - start_time)

    days = upt_seconds // (24 * 3600)
    upt_seconds %= (24 * 3600)
    hours = upt_seconds // 3600
    upt_seconds %= 3600
    minutes = upt_seconds // 60
    seconds = upt_seconds % 60

    upt_message = f"Thời gian bot Online : {days} Ngày, {hours} Giờ, {minutes}  Phút, {seconds} Giây."
    
    # Gửi thông điệp về thời gian hoạt động
    message_to_send = Message(text=upt_message)
    client.sendMessage(message_to_send, thread_id, thread_type, ttl=60000)

def get_szl():
    return {
        'uptime': handle_uptime_command
    }
