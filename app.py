from time import sleep
import pandas as pd 
import os
import json
from datetime import date

#self defined Moodules

#Main Algorithms
from Modules.Algorithms import SMA

from Modules.Database.CouchDB import CouchDB


from flask import Flask, render_template,url_for,jsonify

from _config import config
app = Flask('Backend')

'''Back End'''

@app.route('/Result/<algorithm>/<date>')
def GetResult(algorithm,date):
    res = CouchDB(config =config["CouchDB"]).getDocQ(dbName=algorithm.lower(), _id=date)
    return jsonify(res)


@app.route('/Analyse/<algorithm>/<date>')
def RunAnalysis(algorithm,date):
    try:
        #Get List of symbols to anaylze
        res = CouchDB( config=config["CouchDB"]).getDocQ(dbName='scnr_res', _id=date)

        Result = SMA().Analyze(res)
        CouchDB( config=config["CouchDB"]).Insert(dbName='sma',doc=Result,_id=date)

        return Result 
        
    except Exception as e:
        print(e)




