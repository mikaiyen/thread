import pandas as pd
import requests
from io import StringIO
import time
import concurrent.futures
import xlwings as xw 

def monthly_report(url):
    # 偽瀏覽器
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    
    # 下載該年月的網站，並用pandas轉換成 dataframe
    r = requests.get(url, headers=headers)
    r.encoding = 'big5'

    dfs = pd.read_html(StringIO(r.text))

    df = pd.concat([df for df in dfs if df.shape[1] <= 11 and df.shape[1] > 5])
    
    if 'levels' in dir(df.columns):
        df.columns = df.columns.get_level_values(1)
    else:
        df = df[list(range(0,10))]
        column_index = df.index[(df[0] == '公司代號')][0]
        df.columns = df.iloc[column_index]
    
    df['當月營收'] = pd.to_numeric(df['當月營收'], 'coerce')
    df = df[~df['當月營收'].isnull()]
    df = df[df['公司代號'] != '合計']
    
    # 偽停頓
    time.sleep(5)
    
    #address = r"c:\Users\mikai\OneDrive\Desktop\stock\\" + url + ".csv"
    xw.view(df)


def inputYear():
    while(1==1):
        num =int(input("請輸入西元年份:  "))
        if(num<2010):
            print("查詢日期小於西元2010年，請重新查詢!")
            continue
        else:
            taiwanyear=num-1911
            return str(taiwanyear)

year = inputYear()
monthstart =int(input("請輸入起始月份:  "))
monthend =int(input("請輸入截止月份:  "))

start_time = time.time()  # 開始時間

base_url = "https://mops.twse.com.tw/nas/t21/sii/t21sc03" 
urls = [f"{base_url}_{year}_{month}_0.html" for month in range(monthstart,monthend+1)]  


with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(monthly_report,urls)

#monthly_report(urls)

end_time = time.time()
print(f"{end_time - start_time} 秒爬取 ")

# 西元2011年1月
# xw.view(monthly_report(2011,1))