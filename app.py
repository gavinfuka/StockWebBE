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
from flask_cors import CORS


from _config import config
app = Flask('Backend')
CORS(app)


'''Back End'''

@app.route('/Result/<algorithm>/<date>')
def GetResultWithDate(algorithm,date):
    res = CouchDB(config =config["CouchDB"]).getDocQ(dbName=algorithm.lower(), _id=date)
    return jsonify(res)

@app.route('/Result/<algorithm>')
def GetResult(algorithm):
    sma_conf = CouchDB( config=config["CouchDB"]).getDocQ(dbName='config', _id='sma')
    res = CouchDB(config =config["CouchDB"]).getDocQ(dbName=algorithm.lower(), _id=sma_conf['LastUpdate'])
    return jsonify(res)


@app.route('/Analyse/<algorithm>/<date>')
def AnalyseWithDate(algorithm,date):
    try:
        #Get List of symbols to anaylze
        scnr_conf = CouchDB( config=config["CouchDB"]).getDocQ(dbName='config', _id='scnr_res')
        scnr_res = CouchDB( config=config["CouchDB"]).getDocQ(dbName='scnr_res', _id=scnr_conf['LastUpdate'])

        Result = SMA().Analyze(scnr_res)
        CouchDB( config=config["CouchDB"]).Insert(dbName='sma',doc=Result,_id=date)
        doc = {
            "LastUpdate": date
        }
        CouchDB( config=config["CouchDB"]).Update(dbName='config',doc=doc,_id='sma')

        return jsonify(Result) 
        
    except Exception as e:
        print(e)
        return  e


@app.route('/Analyse/<algorithm>')
def Analyse(algorithm):
    try:
        dbDoc = CouchDB( config=config["CouchDB"]).getDocQ(dbName='config', _id='yFinance')
        date = dbDoc['LastUpdate']
        #Get List of symbols to anaylze
        scnr_conf = CouchDB( config=config["CouchDB"]).getDocQ(dbName='config', _id='scnr_res')
        scnr_res = CouchDB( config=config["CouchDB"]).getDocQ(dbName='scnr_res', _id=scnr_conf['LastUpdate'])
        scnr_res = dict(scnr_res)

        Result = SMA().Analyze(scnr_res)
        CouchDB( config=config["CouchDB"]).Update(dbName='sma',doc=Result,_id=date)
        doc = {
            "LastUpdate": date
        }
        CouchDB( config=config["CouchDB"]).Update(dbName='config',doc=doc,_id='sma')

        return jsonify(Result) 
        
    except Exception as e:
        err = {"error":e}
        return  jsonify(err)

