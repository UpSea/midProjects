# -*- coding: utf-8 -*-
if __name__ == '__main__':
    import sys,os
    from PyQt4 import QtCore, QtGui
    app = QtGui.QApplication(sys.argv) 
    
    xpower = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir))
    sys.path.append(xpower)
    
    params={}
    Globals=[]
    dataSource={}
    algo={}
    
    dataSource['dataProvider']='tushare'
    dataSource['storageFormat']='mongodb'
    dataSource['symbol']='600028'
    dataSource['dateStart']='2015-03-19'
    dataSource['dateEnd']='2015-12-31'
    dataSource['dataPeriod']='D'
    
    algo['instant_fill']=True
    algo['capital_base']=1000
    
    params['dataSource'] = dataSource
    params['algo'] = algo  
    
    from TradingCalendar import shTradingCalendar
    tradingcalendar = shTradingCalendar    
    from zipline.finance.trading import TradingEnvironment
    from loaders.yahooLoader import load_market_data
    algo['env']=TradingEnvironment(load=load_market_data,
                                   #bm_symbol='000001',
                                   exchange_tz="Asia/Shanghai",
                                   max_date=None,
                                   env_trading_calendar = tradingcalendar,
                                   asset_db_path=':memory:')     
import matplotlib.pyplot as plt
from Algorithms.DualEma_talib import DualEmaTalib
import os,sys        
xpower = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,os.pardir,os.pardir,'histdata'))
sys.path.append(xpower)

import dataCenter as dataCenter    
from Analyzers.Analyzer01 import Analyzer01
from Analyzers.Analyzer02 import Analyzer02
from Analyzers.Analyzer03 import Analyzer03
from Analyzers.Analyzer04 import Analyzer04
from Analyzers.Analyzer05 import Analyzer05

dataSource = params['dataSource']
algo = params['algo']


dataCenter = dataCenter.dataCenter()           
dataForZipline = dataCenter.getFeedsForZipline(dataSource)
#dataForZipline = feedsForZipline.GetFeedsFromMongodb(dataSource)
dataForCandle = dataCenter.retriveCandleData(params = dataSource)
#dataForCandle = dataCenter.retriveCandleData(datasource = 'tushare',storageType = 'mongodb',symbol = '600028')     

#dataForCandle = feedsForCandle.GetCandlesFromMongodb(dataSource)

dataUtcTime = dataForZipline.tz_localize('utc')
algo = DualEmaTalib(instant_fill=algo['instant_fill'],
                    capital_base=algo['capital_base'],
                    env=algo['env'])

def dumpDict(dictStr):
    """"""
    import json
    jsonDumpsIndentStr = json.dumps(dictStr, indent=4,skipkeys = False,default=str,sort_keys=True)
    print (jsonDumpsIndentStr) 
algo.dumpDict = dumpDict
result = algo.run(dataUtcTime)

analyzer = Analyzer05(Globals=Globals)
analyzer.analyze(result,dataForCandle,bDrawText=False)




if __name__ == '__main__':
    sys.exit(app.exec_())