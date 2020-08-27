from time import sleep
import pandas as pd 
import os
import json

#self defined Moodules
from Modules import ChromeBot
from Modules.Screener import Screener
from GUtils.GSheet import GSheet
from GUtils.Database.CouchDB import CouchDB
from selenium.webdriver.common.keys import Keys

from flask import Flask, render_template,url_for,jsonify

app = Flask('Backend')

'''Back End'''
@app.route('/syncDB')
def SyncDatabase():
    Result = GSheet('1EIQacULCn6vC7dc4q9KVX71E2eB-Obasfq6N4mVcyQo').Get()
    Result["_id"] = "2020-08-20"
    CouchDB(HTTP="http", USERNAME = "admin", PASSWORD="password" , URL='localhost:5984').Insert(dbName="jlaw",doc =Result)
    print('OK')





@app.route('/graph')
def TradingView():
    List = GSheet('1EIQacULCn6vC7dc4q9KVX71E2eB-Obasfq6N4mVcyQo').Get()
    TraVwBot = ChromeBot('https://tw.tradingview.com/chart')
    TraVwBot.BaseActions.Click('/html/body/div[2]/div[2]/div/div/div[1]/div/div/div/div/div/div[13]/div/div/div[1]')
    TraVwBot.BaseActions.Click('/html/body/div[8]/div/div[2]/div/div/div/div/div/div[1]/div[2]/span[2]')

    for stock in List['Stock']:
        print(stock)
        TraVwBot.BaseActions.Wait('/html/body/div[2]/div[2]/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div/input')
        TraVwBot.BaseActions.Click('/html/body/div[2]/div[2]/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div/input')
        TraVwBot.BaseActions.Send('/html/body/div[2]/div[2]/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div/input', stock.replace('.HK',''))
        TraVwBot.BaseActions.Select('/html/body/div[2]/div[2]/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div/input').send_keys(Keys.ENTER)
        input('Press enter for next')
    TraVwBot.Quit()

@app.route('/analyse')
def RunAnalysis():
    try:
        #Investing.com Filter
        bot= ChromeBot()
        res = bot.InvestCom.Extract()
        bot.Quit()

        GSheet('1EIQacULCn6vC7dc4q9KVX71E2eB-Obasfq6N4mVcyQo').Save(res,sheet='Investing.com') 

        Result = Screener().Analyze(res)

        GSheet('1EIQacULCn6vC7dc4q9KVX71E2eB-Obasfq6N4mVcyQo').Save(Result)
        return Result 
        
    except Exception as e:
        print(e)

@app.route('/result')
def Result():
    res = GSheet('1EIQacULCn6vC7dc4q9KVX71E2eB-Obasfq6N4mVcyQo').Get()
    return jsonify(res)


