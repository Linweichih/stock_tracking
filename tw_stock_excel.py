import numpy as np
import requests
import pandas as pd
import datetime


#   http://www.twse.com.tw/exchangeReport/STOCK_DAY?date=20180817&stockNo=2330  取一個月的股價與成交量
def get_stock_history(date, stock_no):
    quotes = []
    url = 'http://www.twse.com.tw/exchangeReport/STOCK_DAY?date=%s&stockNo=%s' % (date, stock_no)
    r = requests.get(url)
    data = r.json()
    return transform(data['data'])  # 進行資料格式轉換


def transform_date(date):
    y, m, d = date.split('/')
    return str(int(y) + 1911) + '/' + m + '/' + d  # 民國轉西元


def transform_data(data):
    data[0] = datetime.datetime.strptime(transform_date(data[0]), '%Y/%m/%d')
    data[1] = int(data[1].replace(',', ''))  # 把千進位的逗點去除
    data[2] = int(data[2].replace(',', ''))
    data[3] = float(data[3].replace(',', ''))
    data[4] = float(data[4].replace(',', ''))
    data[5] = float(data[5].replace(',', ''))
    data[6] = float(data[6].replace(',', ''))
    data[7] = float(0.0 if data[7].replace(',', '') == 'X0.00' else data[7].replace(',', ''))  # +/-/X表示漲/跌/不比價
    data[8] = int(data[8].replace(',', ''))
    return data


def transform(data):
    return [transform_data(d) for d in data]


def create_df(date, stock_no):
    s = pd.DataFrame(get_stock_history(date, stock_no))
    s.columns = ['date', 'shares', 'amount', 'open', 'high', 'low', 'close', 'change', 'turnover']
    # "日期","成交股數","成交金額","開盤價","最高價","最低價","收盤價","漲跌價差","成交筆數"
    stock = []
    for i in range(len(s)):
        stock.append(stock_no)
    s['stock_no'] = pd.Series(stock, index=s.index)  # 新增股票代碼欄，之後所有股票進入資料表才能知道是哪一張股票
    datelist = []
    for i in range(len(s)):
        datelist.append(s['date'][i])
    s.index = datelist  # 索引值改成日期
    s2 = s.drop(['date'], axis=1)  # 刪除日期欄位
    mlist = []
    for item in s2.index:
        mlist.append(item.month)
    s2['month'] = mlist  # 新增月份欄位
    return s2


listDji = ['2330']
for stock_num in listDji:
    result = create_df('20200701', stock_num)
    print(result)

print("count of close price ", result.groupby('month').close.count())
print("Sum of shares", result.groupby('month').shares.sum())
