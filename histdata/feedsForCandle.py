# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.dates as mpd
import datetime as dt
def DataFrameToCandle(history):
    """
    将日期字符串转化为Datetime，再转化为narray，只用于绘制candle
    输入：
        pandas.DataFrame。
        Index=Str
    输出：
        numpy.narray
        col1=date
        col2=open
        col3=high
        col4=low
        col5=close
    """     
    #date = np.array([mpd.date2num(dt.datetime.strptime(dateStr, '%Y-%m-%d')) for dateStr in history.index])         
    date = np.array([mpd.date2num(pd.to_datetime(dateStr+' 09:30:00+08',format= '%Y-%m-%d %H:%M:%S').tz_localize('utc')) for dateStr in history.index])         
    quotes = np.array(history.iloc[:][['open','high','low','close']])
    rows = quotes.shape[0]
    colls = quotes.shape[1]
    quotesWithDate = np.append(date,quotes.reshape(rows*colls,1,order='F')).reshape(colls+1,rows)
    # %%
    if len(quotesWithDate) == 0:
        raise SystemExit    
    return quotesWithDate.T    

def GetCandlesFromMongodb(params):
    from mongodb.DataSourceMongodb import Mongodb
    import datetime as dt    
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
      
    return DataFrameToCandle(history)