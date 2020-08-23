from pandas_datareader import data as pdr
from yahoo_fin import stock_info as si
from pandas import ExcelWriter
import yfinance as yf
import pandas as pd
import requests
import datetime
import time
import os
import matplotlib.pyplot as plt

from tqdm import tqdm

from GUtils.GSheet import GSheet
from GUtils.CLog import CLog

from ..config import config

yf.pdr_override()

# stocklist = []
# for filename in os.listdir('./csv'):
#     if '.csv' in filename:
#         with open('./csv/'+filename,encoding='utf-8') as f:
#             watchlist = pd.read_csv(f).to_dict()
#             for key,value in watchlist['代號'].items():
#                 stocklist.append(str(value).zfill(4) + '.HK')

class Screener:
    def __init__(self):
        pass

    @staticmethod
    def PadZero(List):
        return [str(item).zfill(4) + '.HK' for item in List]


    @staticmethod
    def CalculateRS(df):
        quarter = -63
        try:
            ThreeMthRS = 2* df['Close'][-1]/ df['Close'][-quarter*1-1] 
            SixMthRS =  df['Close'][-1]/df['Close'][-quarter*2-1] 
            NineMthRS = df['Close'][-1]/df['Close'][-quarter*3-1] 
            TwelveMthRS = df['Close'][-1]/df['Close'][0]

            RS_Rating = ThreeMthRS + SixMthRS + NineMthRS + TwelveMthRS

        except:
            CLog('[X] RS_Rating Not caculated:' + str(len(df)))
            RS_Rating = 0

        return RS_Rating


    @staticmethod
    def Plt(df):
        plt.figure(figsize=(15,10))
        plt.grid(True)
        plt.plot(df['Close'], label ='GLD')
        plt.plot(df['SMA_50'], label='MA 50')
        plt.plot(df['SMA_150'], label='MA 150')
        plt.plot(df['SMA_200'], label='MA 200')
        plt.legend(loc=2)
        plt.show()


    def EvaluateCondition(self,df,name,symbol,sector=None):
        try:
            RS_Rating = self.CalculateRS(df)   
            sma = [50, 150, 200]
            for x in sma:
                # ClosingP = df.iloc[:,4]
                ClosingP = df.Close
                Rolled = ClosingP.rolling(window=x)
                Mean = Rolled.mean()
                df["SMA_"+str(x)] = round(Mean,2)
            # self.Plt(df)

            currentClose = df["Adj Close"][-1]
            moving_average_50 = df["SMA_50"][-1]
            moving_average_150 = df["SMA_150"][-1]
            moving_average_200 = df["SMA_200"][-1]
            low_of_52week = min(df["Adj Close"][-260:])
            high_of_52week = max(df["Adj Close"][-260:])
            
            try:
                moving_average_200_20 = df["SMA_200"][-20]

            except Exception:
                moving_average_200_20 = 0

            Conditions = {
                '1':(currentClose > moving_average_150 > moving_average_200),
                '2': (moving_average_150 > moving_average_200),
                '3': (moving_average_200 > moving_average_200_20),
                '4': (moving_average_50 > moving_average_150 > moving_average_200),
                '5': (currentClose > moving_average_50),
                '6': (currentClose >= (1.3*low_of_52week)),
                '7': (currentClose >= (.75*high_of_52week)),
            }

            selectedConditions = [boolean for i,boolean in Conditions.items() if i in config['Conditions']['include']]

            if( False not in selectedConditions):
                data ={
                        'Stock': symbol, 
                        "Name": name,
                        # "Sector" : sector,
                        "RS_Rating": RS_Rating, 
                        "50 Day MA": moving_average_50, 
                        "150 Day Ma": moving_average_150, 
                        "200 Day MA": moving_average_200, 
                        "52 Week Low": low_of_52week, 
                        "52 week High": high_of_52week,
                    }
                return data

            return False

                                
        except Exception as e:
            print (e)
            return False


    def Analyze(self,Data):
        exportList = pd.DataFrame(columns=['Stock', "Name", "RS_Rating", "50 Day MA", "150 Day Ma", "200 Day MA", "52 Week Low", "52 week High"])
        Data["SymbolList"] = self.PadZero(Data["SymbolList"])

        for name,symbol in zip(Data['NameList'],Data['SymbolList']):
            if symbol in config['Exceptions']:
                continue
            #yahoo finance API
            start_date = datetime.datetime.now() - datetime.timedelta(days=365)
            end_date = datetime.date.today()
            yahoo_df = pdr.get_data_yahoo(symbol, start=start_date, end=end_date)

            if len(yahoo_df) <= 0:
                continue

            result = self.EvaluateCondition(yahoo_df,name=name, symbol=symbol)
            if (result):
                exportList = exportList.append(result,ignore_index=True)

        exportList = exportList.sort_values(by=['RS_Rating'],ascending=False)
        return exportList.to_dict('list')

# res = GSheet('1EIQacULCn6vC7dc4q9KVX71E2eB-Obasfq6N4mVcyQo').Get(sheet='Investing.com')
# Result = Screener().Analyze(res)
# Result = Screener().Analyze({'SymbolList':['1755'],'NameList':[''],'SectorList':['']})
# GSheet('1EIQacULCn6vC7dc4q9KVX71E2eB-Obasfq6N4mVcyQo').Save(Result)