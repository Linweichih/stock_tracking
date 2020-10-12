import io
import requests
import pandas as pd
import json
import numpy as np
import datetime
from io import StringIO


datestr = '20201007'

# 下載股價
r = requests.post('https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + datestr + '&type=ALL')

# 整理資料，變成表格
df = pd.read_csv(StringIO(r.text.replace("=", "")),
            header=["證券代號" in l for l in r.text.split("\n")].index(True)-1)
print(df)


# 顯示出來

def crawl_price(stock_id):
    d = datetime.datetime.now()
    url = "https://query1.finance.yahoo.com/v8/finance/chart/"+stock_id+"?period1=0&period2="+str(int(d.timestamp()))+"&interval=1d&events=history&=hP2rOschxO0"

    res = requests.get(url)
    data = json.loads(res.text)
    df = pd.DataFrame(data['chart']['result'][0]['indicators']['quote'][0], index=pd.to_datetime(np.array(data['chart']['result'][0]['timestamp'])*1000*1000*1000))
    return df


url = "https://finance.yahoo.com/world-indices/"
response = requests.get(url)


f = io.StringIO(response.text)
dfs = pd.read_html(f)
world_index = dfs[0]

# print(world_index)



