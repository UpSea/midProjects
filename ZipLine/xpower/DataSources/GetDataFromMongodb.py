# -*- coding: utf-8 -*-
from .DataConverter import DataConverter
from .DataSourceMongodb import Mongodb
import datetime as dt
# %% 01类定义
#----------------------------------------------------------------------
def GetDataFromMongodb(params):
    ip = params['ip']
    port = params['port']
    database = params['database']

    symbol = params['symbol']
    strStart = params['dateStart']
    strEnd = params['dateEnd']
    frequency = params['frequency']
    
    # 1)connect to Mongodb  
    connect = Mongodb(ip, port)
    connect.use(database)    #database    
    
    # 2)retrive data from specified collection    
    connect.setCollection(frequency)    #table
    history = connect.retrive(symbol,strStart,strEnd,frequency)
      
    dataConverter = DataConverter()
    return dataConverter.DataFrameToZipline(history),dataConverter.DataFrameToCandle(history)
