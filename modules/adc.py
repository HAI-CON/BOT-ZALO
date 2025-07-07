import os
import requests
from config import ADMIN
from zlapi.models import Message

ADMIN_ID = ADMIN

des = {
    'version': "1.0.0",
    'credits': "Nguyễn Đức Tài",
    'description': "Áp dụng code all link raw"
}

def is_admin(author_id):
    return author_id == ADMIN_ID

def read_command_content(command_name):
    try:
        file_path = f"modules/{command_name}.py"
        
        if not os.path.exists(file_path):
            return None
        
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        return str(e)

def handle_adc_command(message, message_object, thread_id, thread_type, author_id, client):
    lenhcanlay = message.split()

    if len(lenhcanlay) < 2:
        error_message = Message(text="Vui lòng nhập tên lệnh cần lấy.")
        client.replyMessage(error_message, message_object, thread_id, thread_type)
        return

    command_name = lenhcanlay[1].strip()

    if not is_admin(author_id):
        response_message = "Bạn không đủ quyền hạn để sử dụng lệnh này."
        message_to_send = Message(text=response_message)
        client.replyMessage(message_to_send, message_object, thread_id, thread_type)
        return

    command_content = read_command_content(command_name)
    
    if command_content is None:
        response_message = f"Lệnh '{command_name}' không được tìm thấy trong các module."
        message_to_send = Message(text=response_message)
        client.replyMessage(message_to_send, message_object, thread_id, thread_type)
        return

    try:
        data = {
            "title": command_name,
            "content": command_content
        }

        response = requests.post("https://note.accngonvip.site/api.php", json=data)

        # Kiểm tra phản hồi từ máy chủ
        if response.status_code == 200:
            try:
                response_data = response.json()
                mock_url = response_data.get("link")

                if mock_url:
                    response_message = f"Thành công ✅\nDưới đây là link của lệnh {command_name}\nLink: {mock_url}"
                else:
                    response_message = "Không thể tạo link trên trang web của bạn."
            except ValueError:
                response_message = "Phản hồi từ máy chủ không phải là JSON hợp lệ."
        else:
            response_message = f"Yêu cầu thất bại với mã trạng thái: {response.status_code}"

    except Exception as e:
        response_message = f"Có lỗi xảy ra: {str(e)}"

    message_to_send = Message(text=response_message)
    client.replyMessage(message_to_send, message_object, thread_id, thread_type)

def get_szl():
    return {
        'adc': handle_adc_command
    }
