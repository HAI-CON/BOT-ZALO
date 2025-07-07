from zlapi.models import Message
import requests
import os
import re
import unicodedata
from datetime import datetime
import random
import string

des = {
    'version': "1.1.1",
    'credits': "HẢI CON x GPT",
    'description': "Tạo bill chuyển tiền bằng API có biến động số dư"
}

# Xóa dấu tiếng Việt
def remove_diacritics(text):
    return ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )

# Random mã giao dịch
def random_mgd(length=15):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

# Lấy thời gian
def get_time():
    now = datetime.now()
    return now.strftime('%H:%M'), now.strftime('%H:%M:%S, Ngày %d/%m/%Y')

# Xử lý bill
def handle_bill_command(message, message_object, thread_id, thread_type, author_id, client):
    try:
        if not message.lower().startswith("!tp"):
            return

        # ✅ Chuẩn hóa cú pháp: bỏ !tp, khoảng trắng và dấu |
        raw = re.sub(r'^!tp\s*\|?', '', message.strip(), flags=re.IGNORECASE)
        fields = [x.strip() for x in raw.split("|")]

        if len(fields) < 8:
            client.sendMessage(
                Message(text=" Sai cú pháp!\nVí dụ:\n!tp |pin5|150000|LE VAN HUAN|0123456789|NGUYEN VAN HAI|0987654321|tpbank|mua tool vip"),
                thread_id, thread_type
            )
            return

        pin_match = re.search(r'\d+', fields[0])
        pin = pin_match.group(0) if pin_match else "3"
        amount = fields[1]
        name_nhan = remove_diacritics(fields[2])
        stk_nhan = fields[3]
        name_gui = remove_diacritics(fields[4])
        stk_gui = fields[5]
        bank_key = fields[6].lower()
        noidung = remove_diacritics(fields[7])

        # Danh sách ngân hàng
        banks = {
            "vietcombank": ("VCB", "VietcomBank", "TMCP Ngoai Thuong Viet Nam"),
            "mbbank": ("MB", "MB Bank", "TMCP Quan Doi"),
            "bidv": ("BIDV", "BIDV", "TMCP Dau tu va Phat trien Viet Nam"),
            "techcombank": ("TCB", "Techcombank", "TMCP Ky Thuong Viet Nam"),
            "vpbank": ("VPB", "VPBank", "TMCP Viet Nam Thinh Vuong"),
            "agribank": ("AGR", "Agribank", "Ngan hang Nong nghiep Viet Nam"),
            "tpbank": ("TPB", "TPBank", "TMCP Tien Phong")
        }

        if bank_key not in banks:
            client.sendMessage(Message(text=" Ngân hàng không hỗ trợ."), thread_id, thread_type)
            return

        code, code1, bank_nhan = banks[bank_key]
        time_dt, time_bill = get_time()
        magiaodich = random_mgd()

        url = 'https://api-lienmom.kesug.com/Api_tp/api.php?type=primary'
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'vi-VN,vi;q=0.9',
            'Connection': 'keep-alive',
            'Origin': 'https://api-lienmom.kesug.com',
            'Referer': 'https://api-lienmom.kesug.com/Api_tp/',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
            'Cookie': '__test=2938c1b1eabdaceb8c8ce44a58bd89c1'
        }

        data = {
            "key": "",
            "theme": "ios",
            "time_dt": time_dt,
            "pin": pin,
            "stk_nhan": stk_nhan,
            "name_nhan": name_nhan,
            "amount": amount,
            "bank_nhan": bank_nhan,
            "code": code,
            "code1": code1,
            "magiaodich": magiaodich,
            "noidung": noidung,
            "bdsd": "1",
            "sdc": amount,
            "stkgui": stk_gui,
            "name_gui": name_gui,
            "time_bill": time_bill
        }

        res = requests.post(url, headers=headers, data=data, timeout=10)

        if res.ok and res.headers.get("Content-Type", "").startswith("application/json"):
            result = res.json()
            if result.get("status") == "success":
                link = result.get("link")
                if link:
                    img = requests.get(link, headers=headers, timeout=10)
                    file_path = f"modules/cache/bill_{magiaodich}.jpg"
                    with open(file_path, 'wb') as f:
                        f.write(img.content)

                    if os.path.exists(file_path):
                        client.sendLocalImage(
                            file_path,
                            message=Message(text=f"Đã tạo bill chuyển {amount} VND từ {name_gui} ➝ {name_nhan}"),
                            thread_id=thread_id,
                            thread_type=thread_type
                        )
                        os.remove(file_path)
                    else:
                        client.sendMessage(Message(text="Không lưu được ảnh bill."), thread_id, thread_type)
                else:
                    client.sendMessage(Message(text="API không trả về link ảnh."), thread_id, thread_type)
            else:
                client.sendMessage(Message(text="Tạo bill thất bại. Vui lòng thử lại sau."), thread_id, thread_type)
        else:
            client.sendMessage(Message(text=" API lỗi hoặc không trả JSON hợp lệ."), thread_id, thread_type)

    except Exception as e:
        client.sendMessage(Message(text=f"Lỗi hệ thống: {str(e)}"), thread_id, thread_type)

# Đăng ký command
def get_szl():
    return {
        'tp': handle_bill_command
    }