from zlapi import ZaloAPI
from zlapi.models import *
import os
import random
import json
import requests

des = {
    'version': "1.0.1",
    'credits': "Trung Trí",
    'description': "Gửi video ngẫu nhiên từ danh sách JSON"
}

def handle_chill_command(message, message_object, thread_id, thread_type, author_id, client):
    try:
        with open('Api/chill.json', 'r', encoding='utf-8') as json_file:
            video_data = json.load(json_file)

        if video_data and isinstance(video_data, list):
            video_url = random.choice(video_data)
            thumbnail_url = "https://i.imgur.com/cMxlg82.mp4" 
            duration = 20000  
            width = 1920
            height = 1080
            
           # gửi thông báo khi gửi video
            loading_message = Message(text="🔎đang tìm kiếm video chill để gửi lên..🎶")
            client.sendMessage(loading_message, thread_id, thread_type,ttl=25000)
           # Thông điệp khi gửi video
            success_message = (
                "🎬 Video chill của bạn đây! 🎶\n\n"
                "✨ Chúc bạn một ngày tràn đầy năng lượng và niềm vui! 🌟"
            )
            
            # Gửi video qua API
            client.sendRemoteVideo(
                videoUrl=video_url,
                thumbnailUrl='https://f48-zpg-r.zdn.vn/jpg/7241812760447876073/cbb6fef57865c63b9f74.jpg',
                duration=duration,
                thread_id=thread_id,
                thread_type=thread_type,
                width=width,
                height=height,
                message=Message(text=success_message)  
            )
            
             # Thông báo sau khi video đã được gửi
            found_message = "✅ Đã tìm thấy video chill và gửi thành công!"
            client.send(
                Message(text=found_message),
                thread_id=thread_id,
                thread_type=thread_type
            )

        else:
            client.send(
                Message(text="Danh sách video rỗng hoặc không hợp lệ."),
                thread_id=thread_id,
                thread_type=thread_type
            )
    except Exception as e:
        error_text = f"Lỗi xảy ra: {str(e)}"
        client.send(
            Message(text=error_text),
            thread_id=thread_id,
            thread_type=thread_type
        )

def get_szl():
    return {
        'vdchill': handle_chill_command
    }