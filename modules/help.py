import os
from zlapi.models import Message
import importlib
from config import PREFIX
des = {
    'version': "1.0.2",
    'credits': "Quốc Khánh x Nguyễn Đức Tài",
    'description': "Lệnh này cung cấp thông tin chi tiết về các lệnh khác."
}

def get_all_khanhdzzl_with_info():
    khanhdzzl_info = {}

    for module_name in os.listdir('modules'):
        if module_name.endswith('.py') and module_name != '__init__.py':
            module_path = f'modules.{module_name[:-3]}'
            module = importlib.import_module(module_path)

            if hasattr(module, 'des'):
                des = getattr(module, 'des')
                version = des.get('version', 'Chưa có thông tin')
                credits = des.get('credits', 'Chưa có thông tin')
                description = des.get('description', 'Chưa có thông tin')
                khanhdzzl_info[module_name[:-3]] = (version, credits, description)

    return khanhdzzl_info

def paginate_commands(khanhdzzl_info, page=1, page_size=5):
    total_pages = (len(khanhdzzl_info) + page_size - 1) // page_size
    if page < 1 or page > total_pages:
        return None, total_pages

    start = (page - 1) * page_size
    end = start + page_size

    commands_on_page = list(khanhdzzl_info.items())[start:end]

    return commands_on_page, total_pages

def handle_help_command(message, message_object, thread_id, thread_type, author_id, client):
    command_parts = message.split()
    
    khanhdzzl_info = get_all_khanhdzzl_with_info()

    if len(command_parts) > 1:
        requested_command = command_parts[1].lower()
        
        if requested_command in khanhdzzl_info:
            version, credits, description = khanhdzzl_info[requested_command]
            single_command_help = f"• Tên lệnh: {requested_command}\n• Phiên bản: {version}\n• Credits: {credits}\n• Mô tả: {description}"
            message_to_send = Message(text=single_command_help)
            client.replyMessage(message_to_send, message_object, thread_id, thread_type)
            return
        elif command_parts[1].isdigit():
            page = int(command_parts[1])
        else:
            message_to_send = Message(text=f"Không tìm thấy lệnh '{requested_command}' trong hệ thống.")
            client.replyMessage(message_to_send, message_object, thread_id, thread_type)
            return
    else:
        page = 1

    commands_on_page, total_pages = paginate_commands(khanhdzzl_info, page)

    if commands_on_page is None:
        help_message = f"Trang {page} không hợp lệ. Tổng số trang hiện có: {total_pages}."
    else:
        help_message_lines = [f"Tổng số lệnh bot hiện tại: {len(khanhdzzl_info)} lệnh\n"]
        for i, (name, (version, credits, description)) in enumerate(commands_on_page, (page - 1) * 5 + 1):
            help_message_lines.append(f"{i}:\n• Tên lệnh: {name}\n• Phiên bản: {version}\n• Credits: {credits}\n• Mô tả: {description}\n")
            help_message_lines.append(f"\n> Để xem thông tin các lệnh khác, vui lòng dùng {PREFIX}help + số trang\n> Ví dụ: {PREFIX}help 2\n> Trang số: {page}/{total_pages}")
            help_message = "\n".join(help_message_lines)

    message_to_send = Message(text=help_message)
    client.replyMessage(message_to_send, message_object, thread_id, thread_type)

def get_szl():
    return {
        'help': handle_help_command
    }