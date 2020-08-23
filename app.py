from time import sleep
import pandas as pd 
import os
import json

#self defined Moodules
from .Modules import ChromeBot,GUtils
from .Modules.Screener import Screener
from .Modules.GUtils.FileUtils import FileUtils 
from .Modules.GUtils.GSheet import GSheet
from selenium.webdriver.common.keys import Keys

from flask import Flask, render_template,url_for,jsonify

app = Flask('Backend')

'''Back End'''
@app.route('/graph')
def TradingView():
    List = GSheet('1EIQacULCn6vC7dc4q9KVX71E2eB-Obasfq6N4mVcyQo').Get()
    TradingView = ChromeBot('https://tw.tradingview.com/chart')
    TradingView.Symbol.Click('/html/body/div[2]/div[2]/div/div/div[1]/div/div/div/div/div/div[13]/div/div/div[1]')
    TradingView.Symbol.Click('/html/body/div[8]/div/div[2]/div/div/div/div/div/div[1]/div[2]/span[2]')

    for stock in List['Stock']:
        print(stock)
        TradingView.Symbol.Wait('/html/body/div[2]/div[2]/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div/input')
        TradingView.Symbol.Click('/html/body/div[2]/div[2]/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div/input')
        TradingView.Symbol.Send('/html/body/div[2]/div[2]/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div/input', stock.replace('.HK',''))
        TradingView.Symbol.Select('/html/body/div[2]/div[2]/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div/input').send_keys(Keys.ENTER)
        input('Press enter for next')
    TradingView.Quit()

@app.route('/analyse')
def RunAnalysis():
    try:
        #Investing.com Filter
        Investing= ChromeBot()
        res = Investing.Symbol.Extract()
        Investing.Quit()

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


