import json
from zlapi.models import *
from config import ADMIN
import os
import time

des = {
    'version': "1.0.6",
    'credits': "Nguyễn Đức Tài",
    'description': "Duyệt nhóm, ban nhóm, duyệt all, ban all, duyệt theo id"
}

def is_admin(author_id):
    return str(author_id) in map(str, ADMIN)

def load_duyetbox_data():
    file_path = 'modules/cache/duyetboxdata.json'
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
            return data if isinstance(data, list) else []
        except json.JSONDecodeError:
            return []

def save_duyetbox_data(data):
    with open('modules/cache/duyetboxdata.json', 'w') as f:
        json.dump(data, f, indent=4)

def handle_duyetbox_command(message, message_object, thread_id, thread_type, author_id, client):
    group_info = client.fetchGroupInfo(thread_id)
    group_name = group_info.gridInfoMap.get(thread_id, {}).get('name', 'None')
    current_time = time.strftime("%H:%M:%S - %d/%m/%Y", time.localtime())

    if not is_admin(author_id):
        response_message = "❌ Bạn không đủ quyền để sử dụng lệnh này."
        client.replyMessage(Message(text=response_message), message_object, thread_id, thread_type)
        return

    text = message.split()
    if len(text) < 2:
        error_message = (
            "📌 Lệnh hỗ trợ:\n"
            "- thread duyet\n"
            "- thread ban\n"
            "- thread duyetid <id>\n"
            "- thread banid <id>\n"
            "- thread duyetall\n"
            "- thread banall\n"
            "- thread listduyet\n"
            "- thread list-approved"
        )
        client.sendMessage(Message(text=error_message), thread_id, thread_type)
        return

    action = text[1].lower()
    data = load_duyetbox_data()

    if action == "duyet":
        if thread_id not in data:
            data.append(thread_id)
            save_duyetbox_data(data)
            success_message = f"✅ Đã duyệt nhóm: {group_name}\nID: {thread_id}\n🕐 {current_time}"
        else:
            success_message = "✅ Nhóm đã được duyệt trước đó."

    elif action == "duyetid" and len(text) > 2:
        target_id = text[2]
        if target_id not in data:
            data.append(target_id)
            save_duyetbox_data(data)
            name = client.fetchGroupInfo(target_id).gridInfoMap.get(target_id, {}).get('name', 'None')
            client.sendMessage(Message(text="✅ Nhóm của bạn đã được ADMIN duyệt từ xa"), target_id, ThreadType.GROUP)
            success_message = f"✅ Đã duyệt nhóm từ xa: {name}\nID: {target_id}\n🕐 {current_time}"
        else:
            success_message = "⚠️ Nhóm đã được duyệt từ trước."

    elif action == "ban":
        if thread_id in data:
            data.remove(thread_id)
            save_duyetbox_data(data)
            success_message = f"🚫 Đã ban nhóm: {group_name}\nID: {thread_id}\n🕐 {current_time}"
        else:
            success_message = "⚠️ Nhóm chưa duyệt, không thể ban."

    elif action == "banid" and len(text) > 2:
        target_id = text[2]
        if target_id in data:
            data.remove(target_id)
            save_duyetbox_data(data)
            name = client.fetchGroupInfo(target_id).gridInfoMap.get(target_id, {}).get('name', 'None')
            client.sendMessage(Message(text="❌ Nhóm của bạn đã bị ADMIN ban từ xa"), target_id, ThreadType.GROUP)
            success_message = f"🚫 Đã ban nhóm từ xa: {name}\nID: {target_id}\n🕐 {current_time}"
        else:
            success_message = "⚠️ Nhóm chưa duyệt."

    elif action == "duyetall":
        all_ids = list(client.fetchAllGroups().gridVerMap.keys())
        new_ids = [gid for gid in all_ids if gid not in data]
        data.extend(new_ids)
        save_duyetbox_data(data)
        group_list = "\n".join(
            f"{i+1}. {client.fetchGroupInfo(gid).gridInfoMap.get(gid, {}).get('name', 'None')} ({gid})"
            for i, gid in enumerate(new_ids)
        )
        success_message = "✅ Đã duyệt toàn bộ nhóm:\n" + (group_list if new_ids else "Không có nhóm mới.")

    elif action == "banall":
        banned = list(data)
        data.clear()
        save_duyetbox_data(data)
        group_list = "\n".join(
            f"{i+1}. {client.fetchGroupInfo(gid).gridInfoMap.get(gid, {}).get('name', 'None')} ({gid})"
            for i, gid in enumerate(banned)
        )
        success_message = "🚫 Đã ban toàn bộ nhóm:\n" + (group_list if banned else "Không có nhóm nào.")

    elif action == "listduyet":
        group_list = "\n".join(
            f"{i+1}. {client.fetchGroupInfo(gid).gridInfoMap.get(gid, {}).get('name', 'None')} ({gid})"
            for i, gid in enumerate(data)
        )
        success_message = "✅ Danh sách nhóm đã duyệt:\n" + (group_list if data else "Chưa có nhóm nào được duyệt.")

    elif action == "list-approved":
        all_ids = list(client.fetchAllGroups().gridVerMap.keys())
        not_approved = [gid for gid in all_ids if gid not in data]
        group_list = "\n".join(
            f"{i+1}. {client.fetchGroupInfo(gid).gridInfoMap.get(gid, {}).get('name', 'None')} ({gid})"
            for i, gid in enumerate(not_approved)
        )
        success_message = "📋 Nhóm chưa được duyệt:\n" + (group_list if not_approved else "Tất cả nhóm đã duyệt.")

    else:
        success_message = "⚠️ Lệnh không hợp lệ, vui lòng xem hướng dẫn: `thread help`"

    client.replyMessage(Message(text=success_message), message_object, thread_id, thread_type)

def get_szl():
    return {
        'thread': handle_duyetbox_command
    }