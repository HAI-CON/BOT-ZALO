from zlapi import ZaloAPI
from zlapi.models import *
import time
from concurrent.futures import ThreadPoolExecutor
import threading
from deep_translator import GoogleTranslator
des = {
    'version': "1.0.0",
    'credits': "Quốc Khánh x Nguyễn Đức Tài",
    'description': "dich ngon ngu"
}
def handle_translate_command(message, message_object, thread_id, thread_type, author_id, client):
        message_text = message_object.get('content', '').strip()
        
        parts = message_text.split(maxsplit=2)

        if len(parts) < 3:
            client.replyMessage(Message(text="Vui lòng nhập ngôn ngữ đích và văn bản cần dịch."), message_object, thread_id, thread_type)
            return

        target_language = parts[1]  
        text_to_translate = parts[2]  

        try:
            
            translated = GoogleTranslator(source='auto', target=target_language).translate(text_to_translate)
            response = f"Dịch từ '{text_to_translate}' sang '{target_language}': {translated}"
            client.replyMessage(Message(text=response), message_object, thread_id, thread_type)
        except Exception as e:
            client.replyMessage(Message(text=f"Lỗi khi dịch: {str(e)}"), message_object, thread_id, thread_type)
def get_szl():
    return {
        'dich': handle_translate_command
    }