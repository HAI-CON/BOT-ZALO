from zlapi.models import Message
import time
import os
import requests

des = {
    'version': "1.0.2",
    'credits': "Quốc Khánh x Nguyễn Đức Tài",
    'description': "Cap trang web yêu cầu"
}

def handle_cap_command(message, message_object, thread_id, thread_type, author_id, client):
    content = message.strip().split()

    if len(content) < 2:
        error_message = Message(text="Vui lòng nhập link cần cap.")
        client.replyMessage(error_message, message_object, thread_id, thread_type)
        return

    url= content[1].strip()

    if not url.startswith("https://") or not validate_url(url):
        error_message = Message(text="Vui lòng nhập link hợp lệ!")
        client.replyMessage(error_message, message_object, thread_id, thread_type)
        return
    
    try:
        url = f"https://apiquockhanh.click/cap?link={url}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }

        image_response = requests.get(url, headers=headers)
        image_response.raise_for_status()
        
        image_path = 'modules/cache/temp_image9.jpeg'
        with open(image_path, 'wb') as f:
            f.write(image_response.content)

        success_message = f"Cap thành công web: {url}"
        message_to_send = Message(text=success_message)
        client.sendLocalImage(
            image_path, 
            message=message_to_send,
            thread_id=thread_id,
            thread_type=thread_type
        )
        
        os.remove(image_path)

    except requests.exceptions.RequestException as e:
        error_message = Message(text=f"Đã xảy ra lỗi khi gọi API: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type)
    except Exception as e:
        error_message = Message(text=f"Đã xảy ra lỗi: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type)

def validate_url(url):
    return requests.utils.urlparse(url).scheme in ('http', 'https')

def get_szl():
    return {
        'cap': handle_cap_command
    }
