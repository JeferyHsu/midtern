import requests
import csv

base_url = "https://api.pin-yi.me/taiwan-calendar"
params = {
    "isHoliday": "true",
    "language": "zh-TW"
}

holiday_data = []

for year in range(2015, 2027):
    url = f"{base_url}/{year}"
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        for item in data:
            # 只保留有節日名稱的項目（包含週末節日）
            if item.get('caption'):
                holiday_data.append([
                    item['date_format'],
                    item['week_chinese'],
                    item['caption']
                ])

with open('api.csv', 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(['日期', '星期', '節日名稱'])
    writer.writerows(holiday_data)

print("特別節日資料已輸出至 api.csv")
