# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.dates as mpd
import datetime as dt

def DataFrameToZipline(history):
    """
    输入：
    pandas.DataFrame。
            Index=Str
    输出：
            pandas.DataFrame
    Index=Datatime
    """
    #date = pd.to_datetime(history.index+' 09:30:00+08',format='%Y-%m-%d %H:%M:%S')
    date = pd.to_datetime(history.index+' 00:00:00+00',format='%Y-%m-%d %H:%M:%S')
    date.name='Date'
    close = pd.Series(np.array(history['close']),index=date,name='AAPL')

    data = pd.DataFrame(close)
    #data.set_index(date,inplace=True)   
    return data
from mongodb.DataSourceMongodb import Mongodb
import datetime as dt
# %% 01类定义
#----------------------------------------------------------------------
def GetFeedsFromMongodb(params):
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
      
    return DataFrameToZipline(history)
    