import requests
from zlapi.models import *
from datetime import datetime, timedelta
import pytz
import time

apikey = "d7e795ae6a0d44aaa8abb1a0a7ac19e4"

vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')

def fetch_weather(area, retries=3):
    try:
        response = requests.get(f"https://api.accuweather.com/locations/v1/cities/search.json?q={requests.utils.quote(area)}&apikey={apikey}&language=vi-vn")
        response.raise_for_status()

        if response.json():
            data = response.json()[0]
            areaKey = data['Key']
        else:
            return "Không tìm thấy địa điểm này!"
    except Exception as err:
        if retries > 0:
            time.sleep(1)
            return fetch_weather(area, retries - 1)
        return "Đã có lỗi xảy ra khi tìm địa điểm!"

    try:
        dataWeather = requests.get(f"http://api.accuweather.com/forecasts/v1/daily/10day/{areaKey}?apikey={apikey}&details=true&language=vi").json()
    except Exception as err:
        if retries > 0:
            time.sleep(1)
            return fetch_weather(area, retries - 1)
        return "Đã có lỗi xảy ra khi lấy dữ liệu thời tiết!"

    def convert_F_to_C(F):
        return round((F - 32) / 1.8)

    def format_hours(hours, label):
        try:
            if hours[-3] == ":" and hours[-2] == "0":
                hours = hours[:-2] + "00"
            return datetime.fromisoformat(hours[:-1]).astimezone(vn_tz).strftime("%H[h]%M[p]")
        except (ValueError, TypeError):
            return f"{label} không có thông tin"

    dataWeatherDaily = dataWeather.get('DailyForecasts', [])
    
    if not dataWeatherDaily:
        return "Không có dữ liệu dự báo thời tiết!"

    dataWeatherToday = dataWeatherDaily[0]

    rainfall_amount = dataWeatherToday.get('Day', {}).get('Rain', {}).get('Value', 'Không có thông tin')
    rain_chance = dataWeatherToday.get('Day', {}).get('PrecipitationProbability', 'Không có thông tin')

    msg = (
        f"Thời tiết hôm nay:\n{dataWeather.get('Headline', {}).get('Text', 'Không có thông tin tiêu đề')}"
        f"\n🌡 Nhiệt độ thấp nhất - cao nhất: {convert_F_to_C(dataWeatherToday.get('Temperature', {}).get('Minimum', {}).get('Value', 0))}°C - {convert_F_to_C(dataWeatherToday.get('Temperature', {}).get('Maximum', {}).get('Value', 0))}°C"
        f"\n🌡 Nhiệt độ cảm nhận được: {convert_F_to_C(dataWeatherToday.get('RealFeelTemperature', {}).get('Minimum', {}).get('Value', 0))}°C - {convert_F_to_C(dataWeatherToday.get('RealFeelTemperature', {}).get('Maximum', {}).get('Value', 0))}°C"
        f"\n🌧 Lượng mưa: {rainfall_amount} mm"
        f"\n☔ Xác suất mưa: {rain_chance}%"
        f"\n🌞 Ban ngày: {dataWeatherToday.get('Day', {}).get('LongPhrase', 'Không có thông tin')}"
        f"\n🌙 Ban đêm: {dataWeatherToday.get('Night', {}).get('LongPhrase', 'Không có thông tin')}"
    )

    return msg

def start_auto(client):
    all_group = client.fetchAllGroups()
    allowed_thread_ids = [gid for gid in all_group.gridVerMap.keys() if gid != '9034032228046851908']

    last_sent_time = None

    send_times = ["07:30", "16:30", "19:05", "11:30"]

    while True:
        now = datetime.now(vn_tz)
        current_time_str = now.strftime("%H:%M")
        
        if current_time_str in send_times and (last_sent_time is None or now - last_sent_time >= timedelta(minutes=1)):
            area = "Lào Cai"
            weather_info = fetch_weather(area)
            for thread_id in allowed_thread_ids:
                client.send(Message(text=f"[ THÔNG BÁO THỜI TIẾT ]\n{weather_info}"), thread_id, ThreadType.GROUP)
                time.sleep(0.3)
            last_sent_time = now
        
        time.sleep(30)
