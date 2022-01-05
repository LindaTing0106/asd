from IPython.display import display, clear_output
from urllib.request import urlopen
import pandas as pd
import datetime
import requests
import sched
import time
import json

s = sched.scheduler(time.time, time.sleep)
def tableColor(val):
    if val > 0:
        color = 'red'
    elif val < 0:
        color = 'green'
    else:
        color = 'white'
    return 'color: %s' % color
def stock_crawler(targets):
    
    clear_output(wait=True)
    
    # 組成stock_list
    stock_list = '|'.join('tse_{}.tw'.format(target) for target in targets) 
    
    #　query data
    query_url = "http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch="+ stock_list
    data = json.loads(urlopen(query_url).read())

    # 過濾出有用到的欄位
    columns = ['c','n','z','tv','v','o','h','l','y']
    df = pd.DataFrame(data['msgArray'], columns=columns)
    df.columns = ['股票代號','公司簡稱','當盤成交價','當盤成交量','累積成交量','開盤價','最高價','最低價','昨收價']
    df.insert(9, "漲跌百分比", 0.0) 
    
    # 新增漲跌百分比
    for x in range(len(df.index)):
        if df['當盤成交價'].iloc[x] != '-':
            df.iloc[x, [2,3,4,5,6,7,8]] = df.iloc[x, [2,3,4,5,6,7,8]].astype(float)
            df['漲跌百分比'].iloc[x] = (df['當盤成交價'].iloc[x] - df['昨收價'].iloc[x])/df['昨收價'].iloc[x] * 100
    
    # 紀錄更新時間
    time = datetime.datetime.now()  
    print("更新時間:" + str(time.hour)+":"+str(time.minute))
    
    # show table
    df = df.style.applymap(tableColor, subset=['漲跌百分比'])
    display(df)
    
    start_time = datetime.datetime.strptime(str(time.date())+'9:30', '%Y-%m-%d%H:%M')
    end_time =  datetime.datetime.strptime(str(time.date())+'13:30', '%Y-%m-%d%H:%M')
    
    # 判斷爬蟲終止條件
    if time >= start_time and time <= end_time:
        s.enter(1, 0, stock_crawler, argument=(targets,))
  
# 欲爬取的股票代碼
stock_list = ['1101','1102','1103','2330']

# 每秒定時器
s.enter(1, 0, stock_crawler, argument=(stock_list,))
s.run()
更新時間:20:36
股票代號	公司簡稱	當盤成交價	當盤成交量	累積成交量	開盤價	最高價	最低價	昨收價	漲跌百分比
0	1101	台泥	37.85	1193	10351	38	38.15	37.85	38	-0.394737
1	1102	亞泥	37.95	611	6233	38	38.2	37.55	38	-0.131579
2	1103	嘉泥	13.85	21	306	13.8	13.85	13.8	13.8	0.362319
3	2330	台積電	230.5	3210	23158	228	230.5	227.5	230	0.217391
 
