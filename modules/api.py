import json
import os
from zlapi.models import Message
from config import ADMIN

des = {
    'version': "1.0.0",
    'credits': "Xuân Bách",
    'description': "Thêm và Check api"
}

api = "Api/"

if not os.path.exists(api):
    os.makedirs(api)

def handle_api_command(args, message_object, thread_id, thread_type, author_id, client):
    if author_id not in ADMIN:
        client.sendMessage(Message(text="Bạn không có quyền thực hiện hành động này!"), thread_id, thread_type)
        return
    args = args.split()
    if args[0] == '&api':
        args = args[1:]
    
    if len(args) < 2:
        response_message = "Lệnh không hợp lệ. Vui lòng sử dụng: api add <tên_file> <link> hoặc api check <tên_file>"
    else:
        command = args[0]
        file_name = args[1]
        file_path = os.path.join(api, f"{file_name}")

        print(f"DEBUG: command = {command}, file_name = {file_name}, file_path = {file_path}")

        if command == "add" and len(args) == 3:
            link = args[2]
            data = []

            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                except json.JSONDecodeError:
                    response_message = f"Lỗi: Không thể đọc tệp {file_name}.json."
                    client.sendMessage(Message(text=response_message), thread_id, thread_type)
                    return
            data.append(link)
            try:
                with open(file_path, 'w') as file:
                    json.dump(data, file, indent=4)
                response_message = f"Đã thêm link vào {file_name}.json. Tổng cộng: {len(data)} link."
            except IOError:
                response_message = f"Lỗi: Không thể ghi vào tệp {file_name}.json."

        elif command == "check" and len(args) == 2:
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                    response_message = f"{file_name}.json hiện có {len(data)} link."
                except json.JSONDecodeError:
                    response_message = f"Lỗi: Không thể đọc tệp {file_name}.json."
            else:
                response_message = f"Tệp {file_name}.json không tồn tại."
        else:
            response_message = "Lệnh không hợp lệ hoặc thiếu tham số."
    client.sendMessage(Message(text=response_message), thread_id, thread_type)

def get_szl():
    return {
        'api': handle_api_command
    }
