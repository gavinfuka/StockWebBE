
import pandas as pd
import requests
import time
import os
import matplotlib.pyplot as plt
from tqdm import tqdm

from .YFinance import YFinance
from _config import config


from ...Database import CouchDB
class SMA:
    def __init__(self):
        self.CouchDB = CouchDB(config=config["CouchDB"])

    @staticmethod
    def PadZero(List):
        return str(List).zfill(4) + '.HK' 


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
            print('[X] RS_Rating Not caculated:' + str(len(df)))
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
        

        for obj in Data["Symbols"]:
            name = obj['Name']['TC']
            symbol = self.PadZero(obj['Symbol'])

            if symbol in config['Exceptions']:
                continue

            # yahoo_df = YFinance.Fetch1Year(symbol)

            # yahoo_df_clone = yahoo_df
            # yahoo_df_clone.index = yahoo_df_clone.index.astype(str)

            yahoo_dict = self.CouchDB.getDocQ(dbName='yfinance',  _id=symbol)
            yahoo_df = pd.DataFrame(yahoo_dict)


            if len(yahoo_df) <= 0:
                continue

            result = self.EvaluateCondition(yahoo_df,name=name, symbol=symbol)
            if (result):
                exportList = exportList.append(result,ignore_index=True)

        exportList = exportList.sort_values(by=['RS_Rating'],ascending=False)
        return exportList.to_dict('list')

