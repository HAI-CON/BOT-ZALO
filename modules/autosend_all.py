import time
import random
import json
import pytz
from datetime import datetime, timedelta
from zlapi.models import Message, ThreadType
import threading

# Danh sách Admin
ADMIN = ["5463805573960055565"]  # Thay bằng ID admin thực tế

# Thông tin mô tả
des = {
    'version': "1.0.1",
    'credits': "Thịnh đz",
    'description': "Hệ thống tự động gửi tin nhắn MITAIZL BOT By Thanh Huy make."
}

# Múi giờ Việt Nam
vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')

# Danh sách nhóm bị chặn
BLOCKED_THREAD_IDS = [
    "8355013351973217472", 
    "1831014859302638939", 
    "6630238838561847857", 
    "7633288257347347164", 
    "8039178332043549346"
]

# Trạng thái autosend
autosend_status = False

# Danh sách thông điệp theo giờ
time_messages = {
    "01:00": ["🌙 Đã 1 giờ sáng rồi! Ngủ đi kẻo mai không dậy nổi đấy."],
    "02:00": ["🌌 2 giờ sáng! Thức khuya quá không tốt đâu nha."],
    "03:00": ["💻 3 giờ sáng! Có phải đang cày phim hay làm việc không? Nghỉ ngơi đi!"],
    "04:00": ["🌅 4 giờ sáng rồi, một ngày mới sắp bắt đầu."],
    "05:00": ["☀️ Chào buổi sáng! Hãy bắt đầu một ngày mới tràn đầy năng lượng."],
    "06:00": ["⏰ 6h sáng rồi! Một ngày vui vẻ nhé."],
    "07:30": ["🎒 Đi học thôi nào :3"],
    "08:00": ["☕ Chào buổi sáng! Đã đến giờ làm việc hoặc học tập rồi."],
    "09:00": ["💡 Chúc bạn một buổi sáng hiệu quả! Đừng quên nghỉ ngơi."],
    "09:30": ["⏳ Chỉ còn một giờ nữa là đến giờ nghỉ trưa. Hãy chuẩn bị nhé!"],
    "10:30": ["🍴 Sắp đến giờ nghỉ trưa, giữ vững tinh thần nhé!"],
    "11:00": ["🥗 Chuẩn bị ăn trưa thôi nào!"],
    "12:00": ["🕛 Đã 12 giờ trưa, nghỉ ngơi chút nhé!"],
    "13:00": ["💼 1 giờ chiều rồi! Làm việc hiệu quả nhé."],
    "14:00": ["😊 Chúc bạn buổi chiều vui vẻ! Đừng quên thư giãn một chút."],
    "15:00": ["🏃 Một buổi chiều vui vẻ! Hãy đứng dậy và vận động một chút."],
    "16:00": ["📋 Sắp hết ngày rồi! Hãy hoàn thành công việc của bạn."],
    "17:00": ["🌇 5 giờ chiều! Chuẩn bị kết thúc một ngày làm việc nhé."],
    "18:00": ["🌆 Chào buổi tối! Thời gian để thư giãn sau một ngày dài."],
    "19:30": ["🍽️ Thời gian cho bữa tối! Hãy thưởng thức bữa ăn ngon miệng."],
    "20:00": ["📖 Đã 8 giờ tối rồi, nghỉ ngơi và thư giãn thôi!"],
    "21:00": ["🏡 Một buổi tối tuyệt vời! Hãy tận hưởng thời gian bên gia đình."],
    "22:00": ["🛌 Sắp đến giờ đi ngủ! Chuẩn bị nghỉ ngơi nhé."],
    "23:00": ["📴 Đã 11 giờ tối, cất điện thoại và đi ngủ thôi!"],
    "00:00": ["🌟 Chúc các bạn ngủ ngon! Hãy mơ những giấc mơ đẹp nhé."],
}

# Lưu trữ video đã gửi
sent_videos = []
last_sent_video = None

def get_random_video(urls):
    global sent_videos, last_sent_video

    # Lọc các video chưa được gửi
    available_videos = [url for url in urls if url not in sent_videos]

    # Nếu tất cả các video đã được gửi, reset danh sách
    if not available_videos:
        sent_videos = []
        available_videos = urls

    # Chọn video ngẫu nhiên từ danh sách còn lại
    video = random.choice(available_videos)

    # Đảm bảo video không trùng lặp ngay sau khi reset
    while video == last_sent_video and len(available_videos) > 1:
        video = random.choice(available_videos)

    sent_videos.append(video)
    last_sent_video = video
    return video

def start_auto(client):
    global autosend_status
    try:
        # Đọc danh sách video từ file JSON trong thư mục Api
        with open('Api/buon.json', 'r', encoding='utf-8') as json_file:
            urls = json.load(json_file)

        if not urls or not isinstance(urls, list):
            print("Danh sách video rỗng hoặc không hợp lệ.")
            return

    except Exception as e:
        print(f"Lỗi khi đọc danh sách video: {e}")
        return

    # Lấy danh sách tất cả các nhóm
    all_group = client.fetchAllGroups()
    allowed_thread_ids = [
        gid for gid in all_group.gridVerMap.keys() if gid not in BLOCKED_THREAD_IDS
    ]

    if not allowed_thread_ids:
        print("Không có nhóm nào để gửi tin nhắn.")
        return

    last_sent_time = None

    while autosend_status:  # Chỉ chạy khi autosend_status = True
        try:
            now = datetime.now(vn_tz)
            current_time_str = now.strftime("%H:%M")  # Lấy giờ phút hiện tại
            
            # Kiểm tra khung giờ và nội dung tin nhắn
            if current_time_str in time_messages and (last_sent_time is None or now - last_sent_time >= timedelta(minutes=1)):
                # Chọn ngẫu nhiên nội dung tin nhắn
                message = random.choice(time_messages[current_time_str])
                # Lấy video ngẫu nhiên
                video_url = get_random_video(urls)
                thumbnail_url = "https://f48-zpg-r.zdn.vn/jpg/7241812760447876073/cbb6fef57865c63b9f74.jpg"  # Thay đổi nếu cần
                duration = 20000  # Thời lượng video (ms)

                for thread_id in allowed_thread_ids:
                    gui = Message(text=f"> 💬 Send Process <\n➜ 🕐Thời Gian: {current_time_str} \n➜ {message} \n 🚦Autosend")
                    try:
                        # Gửi video
                        client.sendRemoteVideo(
                            videoUrl=video_url, 
                            thumbnailUrl=thumbnail_url,
                            duration=duration,
                            message=gui,
                            thread_id=thread_id,
                            thread_type=ThreadType.GROUP,
                            ttl=1800000,
                            width=1080,
                            height=1920
                        )

                        # Gửi voice (âm thanh của video)
                        client.sendRemoteVoice(
                            video_url,
                            thread_id=thread_id,
                            thread_type=ThreadType.GROUP,
                            fileSize=100000,
                            ttl=1800000
                        )

                        print(f"✅ Gửi thành công đến nhóm {thread_id}: {message} + voice")
                    except Exception as e:
                        print(f"❌ Lỗi gửi tin đến nhóm {thread_id}: {e}")
                # Cập nhật thời gian gửi cuối cùng
                last_sent_time = now
            
            # Chờ 30 giây trước khi kiểm tra lại
            time.sleep(30)
        except Exception as e:
            print(f"Lỗi trong vòng lặp autosend: {e}")

# Lệnh bật autosend
def handle_autosend_start(message, message_object, thread_id, thread_type, author_id, client):
    global autosend_status

    if author_id not in ADMIN:
        response_message = Message(text="⛔ 𝘽ạ𝙣 𝙠𝙝ô𝙣𝙜 𝙘ó 𝙦𝙪𝙮ề𝙣 𝙨ử 𝙙ụ𝙣𝙜 𝙡ệ𝙣𝙝 𝙣à𝙮❗")
        client.replyMessage(response_message, message_object, thread_id, thread_type, ttl=18000)
        return

    if autosend_status:
        response_message = Message(text="⚙️ AUTOSEND đã được bật trước đó❗")
        client.replyMessage(response_message, message_object, thread_id, thread_type, ttl=18000)
        return

    autosend_status = True
    threading.Thread(target=start_auto, args=(client,), daemon=True).start()
    response_message = Message(text="✅ 𝐥𝐨𝐚𝐝𝐢𝐧𝐠 𝐀𝐮𝐭𝐨𝐬𝐞𝐧𝐝 𝐝𝐞𝐯  Music🔥")
    client.replyMessage(response_message, message_object, thread_id, thread_type, ttl=18000)

# Lệnh tắt autosend
def handle_autosend_stop(message, message_object, thread_id, thread_type, author_id, client):
    global autosend_status

    if author_id not in ADMIN:
        response_message = Message(text="⛔ 𝘽ạ𝙣 𝙠𝙝ô𝙣𝙜 𝙘ó 𝙦𝙪𝙮ề𝙣 𝙨ử 𝙙ụ𝙣𝙜 𝙡ệ𝙣𝙝 𝙣à𝙮!")
        client.replyMessage(response_message, message_object, thread_id, thread_type, ttl=18000)
        return

    if not autosend_status:
        response_message = Message(text="❌ AUTOSEND đã được tắt trước đó❗")
        client.replyMessage(response_message, message_object, thread_id, thread_type, ttl=18000)
        return

    autosend_status = False
    response_message = Message(text="❌ 𝐒𝐭𝐨𝐩 𝐀𝐮𝐭𝐨𝐬𝐞𝐧𝐝 𝐝𝐞𝐯 Music🌪️")
    client.replyMessage(response_message, message_object, thread_id, thread_type, ttl=18000)

# Đăng ký các lệnh autosend
def get_szl():
    return {
        'ats_on': handle_autosend_start,
        'ats_off': handle_autosend_stop
    }