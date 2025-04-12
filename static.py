import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_holidays(start_year, end_year):
    base_url = "https://www.officeholidays.com/countries/taiwan/"
    all_holidays = []  # 儲存所有假期資料的列表

    # 遍歷指定年份範圍
    for year in range(start_year, end_year + 1):
        url = f"{base_url}{year}"  # 組合完整 URL
        response = requests.get(url)  # 發送 HTTP 請求
        
        # 檢查 HTTP 回應狀態碼
        if response.status_code == 200:
            # 使用 BeautifulSoup 解析 HTML 內容
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 尋找包含假期資料的表格
            table = soup.find('table', {'class': 'country-table'})
            
            if table:
                # 跳過表格標題行，取得所有資料行
                rows = table.find_all('tr')[1:]
                
                # 處理每一行資料
                for row in rows:
                    cols = row.find_all('td')  # 取得所有列資料
                    
                    # 確保有足夠的列數（至少 4 列）
                    if len(cols) >= 4:
                        # 提取並清理各列資料
                        day = cols[0].text.strip()          # 星期幾
                        date = cols[1].text.strip()         # 日期
                        holiday_name = cols[2].text.strip() # 假期名稱
                        holiday_type = cols[3].text.strip() # 假期類型
                        
                        # 將資料存入字典
                        all_holidays.append({
                            'Year': year,
                            'Day': day,
                            'Date': date,
                            'Holiday Name': holiday_name,
                            'Type': holiday_type
                        })
        else:
            print(f"無法取得 {year} 年資料，HTTP 狀態碼: {response.status_code}")

    return pd.DataFrame(all_holidays)  # 將列表轉換為 DataFrame

# 執行爬蟲程式 (2015-2026)
holidays_df = fetch_holidays(2015, 2026)

# 將結果儲存為 CSV 檔案
holidays_df.to_csv('static.csv', index=False)
print("台灣假期資料已儲存至 static.csv")
