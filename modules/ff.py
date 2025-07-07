from zlapi.models import *
from zlapi import Message, ThreadType
import requests
from io import BytesIO

des = {
    'version': "1.0.2",
    'credits': "Vũ Xuân Kiên",
    'description': "Xoá tin nhắn người dùng"
}

def get_info(uid):
    url = f"https://ff-community-api.vercel.app/ff.Info?uid={uid}"
    try:
        res = requests.get(url, timeout=10)
        if res.status_code == 200:
            return res.json()
    except:
        pass
    return None

def get_mitaizl(message, message_object, thread_id, thread_type, author_id, client):
    args = message.strip().split()

    if len(args) < 2:
        return client.replyMessage(
            Message(text="❌ Vui lòng nhập UID Free Fire.\nVí dụ: ff 123456789"),
            message_object, thread_id, thread_type
        )

    uid = args[1]

    client.replyMessage(
        Message(text="🔍 Đang lấy thông tin tài khoản..."),
        message_object, thread_id, thread_type
    )

    data = get_info(uid)
    if not data or data.get("status") != 200:
        return client.replyMessage(
            Message(text="❌ Không tìm thấy thông tin UID này hoặc API lỗi."),
            message_object, thread_id, thread_type
        )

    result = data.get("result", {})

    # Gửi avatar nếu có
    avatar_url = result.get("avatar")
    if avatar_url:
        try:
            response = requests.get(avatar_url)
            image_bytes = BytesIO(response.content).getvalue()
            client.sendMessageImage(image_bytes, message_object, thread_id, thread_type)
        except:
            pass  # Không gửi avatar nếu lỗi tải

    # Lấy thông tin chính
    nickname = result.get("nickname", "Không rõ")
    level = result.get("level", "N/A")
    region = result.get("region", "N/A")
    survival_rank = result.get("rankedSurvival", "N/A")
    stars = result.get("totalStars", "N/A")
    like = result.get("likes", "0")
    last_login = result.get("lastLogin", "Không rõ")
    language = result.get("language", "Không rõ")
    about = result.get("about", "Không có")

    # Quân đoàn
    guild = result.get("guild", {})
    guild_name = guild.get("name", "Không có")
    guild_level = guild.get("level", "N/A")
    guild_capacity = guild.get("capacity", "N/A")
    guild_member = guild.get("currentMembers", "N/A")
    guild_owner = guild.get("ownerName", "N/A")
    guild_owner_level = guild.get("ownerLevel", "N/A")

    # Pet và kỹ năng
    pet = result.get("pet", {})
    pet_name = pet.get("name", "Không có")
    pet_level = pet.get("level", "N/A")
    skill = result.get("characterSkill", "Không rõ")

    # Soạn tin nhắn trả về
    text = f"""📄 Thông tin Free Fire:

👤 Nickname: {nickname}
⭐ Cấp độ: {level}
🌍 Khu vực: {region}
🏆 Rank Sinh tồn: {survival_rank}
🌟 Tổng sao Tử chiến: {stars}
❤️ Like: {like}
🕒 Đăng nhập gần nhất: {last_login}
🗣️ Ngôn ngữ: {language}
📜 Tiểu sử: {about}

🔰 Quân đoàn:
🏘️ Tên: {guild_name}
🎖️ Cấp: {guild_level}
👥 Sức chứa: {guild_capacity}
👤 Thành viên: {guild_member}
👑 Chủ: {guild_owner} (Lv {guild_owner_level})

🐾 Khác:
🧠 Kỹ năng: {skill}
🐶 Pet: {pet_name} (Lv {pet_level})
"""

    client.replyMessage(Message(text=text), message_object, thread_id, thread_type)

def get_szl():
    return {
        'ff2': get_mitaizl
    }