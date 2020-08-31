from time import sleep
import pandas as pd 
import os
import jsonfrom datetime import date

#self defined Moodules

#Main Algorithms
from Modules.Algorithms import SMA

from Modules.Database.CouchDB import CouchDB


from flask import Flask, render_template,url_for,jsonify

from _config import config
app = Flask('Backend')

'''Back End'''

@app.route('/GetResult/<algorithm>')
def GetResult(algorithm):
    res = CouchDB(HTTP="http", USERNAME = "Fexpert", PASSWORD="Fexpert" , URL=config["CouchDB"]["URL"]).getDocQ(dbName=algorithm.lower(), _id="2020-08-20")
    return jsonify(res)


@app.route('/Analyse/<algorithm>')
def RunAnalysis(algorithm):
    try:
        #Get List of symbols to anaylze
        res = CouchDB(HTTP="http", USERNAME = "Fexpert", PASSWORD="Fexpert" , URL=config["CouchDB"]["URL"]).getDocQ(dbName='symbol', _id="2020-08-31")

        Result = SMA().Analyze(res)

        return Result 
        
    except Exception as e:
        print(e)




