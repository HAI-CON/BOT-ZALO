import re
import os
import json
from logging_utils import Logging
logger = Logging()
# Cấu hình cố định
IMEI = "d2328e2a-b268-4871-873e-cdc03b746b46-a0e09f4206cef88dab92b93072e25747"
SESSION_COOKIES = {
    "_ga": "GA1.2.1905749354.1751734702",
    "_gid": "GA1.2.14785691.1751734702",
    "_ga_VM4ZJE1265": "GS2.2.s1751734702$o1$g0$t1751734702$j60$l0$h0",
    "_zlang": "vn",
    "zpsid": "uDZR.426330329.18.ttPzU0P9MmFV0J8Q2abR0tCwAJSqVsWmDdffEgsbOqqnUYLr1w02Qcv9MmC",
    "zpw_sek": "CalJ.426330329.a0.PK_B0bMe2FwCu67dTAW8_YwARPLtaYgqFV0vpGp_NQabdZgrFfjbkpFQFfqKbJNSA0FanXkVEu0ZgUAdFC08_W",
    "__zi": "3000.SSZzejyD6zOgdh2mtnLQWYQN_RAG01ICFjIXe9fEM8Wyd-wdc4jPWd2TwwlLJLs3Tflgh34r.1",
    "__zi-legacy": "3000.SSZzejyD6zOgdh2mtnLQWYQN_RAG01ICFjIXe9fEM8Wyd-wdc4jPWd2TwwlLJLs3Tflgh34r.1",
    "ozi": "2000.SSZzejyD6zOgdh2mtnLQWYQN_RAG01ICFjMXe9fFM8yvd-ghb41QWZ6New-IHHU4DPQbgPD24O0.1",
    "app.event.zalo.me": "7280909900899205763",
    "_ga_RYD7END4JE": "GS2.2.s1751785696$o5$g1$t1751785696$j60$l0$h0"
}
API_KEY = "api_key"
SECRET_KEY = "secret_key"
PREFIX = "!"
import json

SETTING_FILE = "setting.json"

# Đọc cấu hình từ file
def read_settings():
    try:
        with open(SETTING_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Ghi lại cấu hình vào file
def write_settings(settings):
    with open(SETTING_FILE, 'w', encoding='utf-8') as file:
        json.dump(settings, file, ensure_ascii=False, indent=4)

# Kiểm tra xem user đã là admin chưa
def is_admin(author_id):
    settings = read_settings()
    admin_bot = settings.get("admin_bot", [])
    return str(author_id) in admin_bot

# Thêm admin mới nếu chưa có
def add_admin(user_id):
    settings = read_settings()
    admin_bot = settings.get("admin_bot", [])
    if str(user_id) not in admin_bot:
        admin_bot.append(str(user_id))
        settings["admin_bot"] = admin_bot
        write_settings(settings)
        return True
    return False

# Lấy tên người dùng từ bot bằng ID
def get_user_name_by_id(bot, author_id):
    try:
        user = bot.fetchUserInfo(author_id).changed_profiles[author_id].displayName
        return user
    except:
        return "Unknown User"

# Xử lý thêm admin bot và in thông báo
def handle_bot_admin(bot):
    settings = read_settings()
    admin_bot = settings.get("admin_bot", [])
    
    # Kiểm tra xem bot đã có trong danh sách admin chưa
    if str(bot.uid) in admin_bot:
        logger.ok(f"ID đã có trong danh sách Admin: {get_user_name_by_id(bot, bot.uid)} {bot.uid}")
    else:
        # Nếu chưa có, thêm vào danh sách admin và thông báo
        added = add_admin(bot.uid)
        if added:
         logger.added(f"Đã thêm ID:{get_user_name_by_id(bot, bot.uid)}  {bot.uid} cho lần đầu tiên khởi động vào BOT")
        else:
           logger.error(f"Lỗi: Không thể thêm {bot.uid} vào danh sách Admin BOT")

# Đọc danh sách admin lúc khởi động
settings = read_settings()
ADMIN = settings.get("admin_bot", [])
