from zlapi.models import Message
from config import ADMIN  # Lấy danh sách admin từ config.py

# Mô tả module
des = {
    'version': "1.0.3",
    'credits': "TÂM HOÀNG",
    'description': "Lệnh đóng/mở chat nhóm"
}

# Trạng thái nhóm (lưu trạng thái mở hoặc đóng chat theo thread_id)
group_chat_status = {}

def is_admin(author_id):
    """Kiểm tra xem người dùng có phải là admin không"""
    return str(author_id) in ADMIN  # Kiểm tra nếu ID có trong danh sách ADMIN

def handle_bot_sos_command(message, message_object, thread_id, thread_type, author_id, client):
    try:
        if not is_admin(author_id):
            error_msg = "• Bạn Không Có Quyền! Chỉ có admin mới có thể sử dụng lệnh này."
            client.replyMessage(Message(text=error_msg), message_object, thread_id, thread_type)
            return

        # Lấy trạng thái hiện tại của nhóm (mặc định là mở chat = 0)
        current_status = group_chat_status.get(thread_id, 0)

        # Đảo trạng thái: 0 -> 1 (đóng), 1 -> 0 (mở)
        new_status = 1 if current_status == 0 else 0
        group_chat_status[thread_id] = new_status

        # Cập nhật cài đặt nhóm
        kwargs = {"lockSendMsg": new_status}
        client.changeGroupSetting(thread_id, **kwargs)

        # Phản hồi trạng thái mới
        action = "🔒 Đóng chat thành công!" if new_status == 1 else "🔓 Mở chat thành công!"
        client.replyMessage(Message(text=action), message_object, thread_id, thread_type)

    except Exception as e:
        error_message = f"⚠ Lỗi khi thay đổi cài đặt nhóm: {str(e)}"
        client.replyMessage(Message(text=error_message), message_object, thread_id, thread_type)

def get_szl():
    return {
        'sos': handle_bot_sos_command
    }