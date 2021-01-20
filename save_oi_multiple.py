import requests
import pandas as pd
import json
from pandas import json_normalize 
import random
from itertools import count
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time
import os.path
from os import path

plt.style.use('fivethirtyeight')
session = requests.Session()

directory = r"C:\\codes\\"

url = "https://www.nseindia.com/api/option-chain-equities?symbol="
#url = "https://www.nseindia.com/api/option-chain-indices?symbol="
headers = {'Host': 'www.nseindia.com', 'Connection': 'keep-alive', 'sec-ch-ua-mobile': '?0', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36', 'Accept': '*/*', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Dest': 'empty', 'Referer': 'https://www.nseindia.com/option-chain', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-US,en;q=0.9'}
homeheaders = {'Host': 'www.nseindia.com', 'Connection': 'keep-alive', 'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"', 'sec-ch-ua-mobile': '?0', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Sec-Fetch-Site': 'none', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-User': '?1', 'Sec-Fetch-Dest': 'document', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-US,en;q=0.9'}
index = count()
x_vals = []
y_vals = []
y1_vals = []

def animate(stkcode):
    #response = requests.get(url, headers=headers)
    response = session.get(url+stkcode, headers=headers)
    #print(response.json())
    if response.status_code == 200:
        data = response.json()
        with open(directory+stkcode+".txt", "w") as outfile:
            json.dump(data, outfile)
        df = json_normalize(data['records'])
        timestamp = df['timestamp']
        stockprice = df['underlyingValue']
        # df1 = pd.DataFrame(df.iloc[:, 1])
        # df2 = pd.DataFrame(df1.iloc[0][0])
        # print(df2)
        ce_data = json_normalize(data=data['records'], record_path='data')
        timelist = [timestamp[0]] * len(ce_data)
        stockpricelist = [stockprice[0]] * len(ce_data)

        df123 = ce_data
        df123['timestamp'] = timelist
        df123['stockprice'] = stockpricelist
        df123 = df123.set_index(['timestamp'])
        #ce_data.insert(0, 'TimeStamp', pd.to_datetime(timestamp))
        #print(df123)
        print(path.exists(directory+stkcode+".csv"))
        if not path.exists(directory+stkcode+".csv"):
            ce_data.to_csv(directory+stkcode+".csv", index=True)
        else:
            ce_data.to_csv(directory+stkcode+".csv", index=True, mode='a', header=False)
        #print(ce_data['CE.openInterest'][(ce_data['expiryDate']=='28-Jan-2021')&(ce_data['strikePrice']==5200)])
    else:
        print("error...")
session.get('https://www.nseindia.com/option-chain', headers=homeheaders)

i = 0
stocks = ['BAJFINANCE','RELIANCE','HINDUNILVR']

while 1==1:
    for stock in stocks:
        animate(stock);
    time.sleep(60)

#print(session.cookies.get_dict())




