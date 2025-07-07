from zlapi.models import Message, ThreadType
import requests
from datetime import datetime

des = {
    'version': "1.0.0",
    'credits': "Minh Vũ",
    'description': "Check Id Free Fire ",
    'power': "✅ Ai cung dung đuoc"
}

# ✅ Ham xu ly lenh ff
def handle_ff_command(message, message_object, thread_id, thread_type, author_id, client):
    parts = message.strip().split()

    # ⚠️ Kiem tra cu phap
    if len(parts) < 2:
        client.sendMessage(
            Message(text="❌ Thieu UID!\n\n📌 **Cach dung:**\n`/ff <uid>`\n\nVi du: `/ff 12345678`"),
            thread_id, thread_type
        )
        return

    uid = parts[1]
    region = "SG"  # Hoac tu đong xac đinh neu muon

    try:
        # 🌐 Goi API lay du lieu
        url = f"https://accinfo.vercel.app/player-info?region={region}&uid={uid}"
        res = requests.get(url)

        if res.status_code != 200 or not res.json().get("basicInfo"):
            client.sendMessage(
                Message(text="❌ Khong tim thay tai khoan hoac UID sai."),
                thread_id, thread_type
            )
            return

        data = res.json()
        basic = data["basicInfo"]
        clan = data.get("clanBasicInfo", {})
        pet = data.get("petInfo", {})
        social = data.get("socialInfo", {})

        # 📦 Lay thong tin can
        nickname = basic.get("nickname", "Khong ro")
        level = basic.get("level", 0)
        rank = basic.get("rank", 0)
        cs_rank = basic.get("csRank", 0)
        liked = basic.get("liked", 0)
        clan_name = clan.get("clanName", "Khong co")
        pet_name = pet.get("name", "Khong co")
        pet_lv = pet.get("level", 0)
        signature = social.get("signature", "Chua co")
        created_at = datetime.fromtimestamp(int(basic.get("createAt", 0))).strftime("%d/%m/%Y")

        # 🧾 Format thong tin
        msg = (
    f"📦 [Thong Tin Free Fire]\n"
    f"━━━━━━━━━━━━━━━━━━━\n"
    f"👤 Nickname: *{nickname}*\n"
    f"🆔 UID: `{uid}` ({region})\n"
    f"📈 Cap đo: `{level}`\n"
    f"🏆 Rank BR: `{rank}` | CS: `{cs_rank}`\n"
    f"❤️ Luot thich: `{liked:,}`\n"
    f"👑 Clan: {clan_name}\n"
    f"🐾 Pet chinh: {pet_name} (Lv.{pet_lv})\n"
    f"📅 Ngay tao tai khoan: {created_at}\n"
    f"📝 Tieu su: {signature if signature else 'Khong co'}\n"
    f"━━━━━━━━━━━━━━━━━━━\n"
)

        # ✅ Gui thong tin ve
        client.sendMessage(Message(text=msg), thread_id, thread_type)

    except Exception as e:
        client.sendMessage(
            Message(text=f"⚠️ Co loi xay ra khi xu ly: {e}"),
            thread_id, thread_type
        )


# 📦 Export command
def get_szl():
    return {
        'ff': handle_ff_command,  # Lenh chinh cua ban
    }
