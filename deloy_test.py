import asyncio
from web3 import Web3
from ABI import router_abi,pairabi, minabi
from LP_DEX_ADDR import LP_DEX_ADDR
from threading import Thread
from datetime import datetime
import time
import pymongo
from halo import Halo
from colorama import Fore, Back, Style
from fastapi import FastAPI #import class FastAPI() từ thư viện fastapi

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["DataTopGainer"]
mongo_data_price = mydb["data_price"]

# get data from Mongodatabase
find_all_data = mongo_data_price.find()
data_price = {}
for data in find_all_data :
    data.pop('_id')
    data_price[data['pair_addr']] = data
print('length of data from Mongo: ', len(data_price))

def retunr_data_price(data_price):
    return_data = []
    for token_pair in data_price :
        price10s = data_price[token_pair]['price10s']
        price0s = data_price[token_pair]['price0s']
        price30s = data_price[token_pair]['price30s']
        price1m = data_price[token_pair]['price1m']
        price5m = data_price[token_pair]['price5m']
        price10m = data_price[token_pair]['price10m']
        price20m = data_price[token_pair]['price20m']
        price30m = data_price[token_pair]['price30m']
        if price10s != 0:
            price_change_10s = round((((price0s - price10s)/price10s)*100),2)
        else : price_change_10s = -999

        if price30s == 0 :
            price_change_30s = -999
        else :
            price_change_30s = round((((price0s - price30s)/price30s)*100),2)

        if price1m == 0 :
            price_change_1m = -999
        else :
            price_change_1m = round((((price0s - price1m)/price1m)*100),2)
        
        if price5m == 0 :
            price_change_5m = -999
        else :
            price_change_5m = round((((price0s - price5m)/price5m)*100),2)
        
        if price10m == 0 :
            price_change_10m = -999
        else :
            price_change_10m = round((((price0s - price10m)/price10m)*100),2)

        if price20m == 0 :
            price_change_20m = -999
        else :
            price_change_20m = round((((price0s - price20m)/price20m)*100),2)
        
        if price30m == 0 :
            price_change_30m = -999
        else :
            price_change_30m = round((((price0s - price30m)/price30m)*100),2)
        #if ( price_change_10s > 0.1 or price_change_10s < -0.1 ):
        # if  ( price_change_30m > 0.5 or price_change_30m < -0.5) :
        #     if  ( price_change_20m > 0.5 or price_change_20m < - 0.5):
        #         if  ( price_change_10m > 0.5 or price_change_10m < -0.5) :
        if not (price_change_30s == -999 and price_change_1m==-999 and price_change_5m==-999 and price_change_10m==-999 and price_change_20m==-999 and price_change_30m==-999 ):
            if not (price_change_5m==0 and price_change_10m==0 and price_change_20m==0 and price_change_30m==0 and price_change_1m==0 and price_change_10s==0 and price_change_30s==0):
                return_data.append({
                    'name' : data_price[token_pair]['name'],
                    'symbol' : data_price[token_pair]['symbol'],
                    'token_addr' :data_price[token_pair]['token_addr'],
                    'Pair' : data_price[token_pair]['Pair'],
                    'Pool' : data_price[token_pair]['Pool'],
                    'price_change_10s' : price_change_10s,
                    'price_change_30s' : price_change_30s,
                    'price_change_1m' : price_change_1m,
                    'price_change_5m' : price_change_5m,
                    'price_change_10m' : price_change_10m,
                    'price_change_20m' : price_change_20m,
                    'price_change_30m' : price_change_30m

            })
    

    print('Total Token Ready reply for GET method: ',len(return_data))
    return return_data
data_price_ = data_price.copy()
data_for_GET = retunr_data_price(data_price_)
print('Length of data_price : ', len(data_price))
app = FastAPI() # gọi constructor và gán vào biến app

@app.get("/test") # giống flask, khai báo phương thức get và url
async def root(): # do dùng ASGI nên ở đây thêm async, nếu bên thứ 3 không hỗ trợ thì bỏ async đi
    return data_for_GET


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)