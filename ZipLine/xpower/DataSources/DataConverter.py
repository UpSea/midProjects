# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.dates as mpd
import datetime as dt

class DataConverter():
    """"""
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
    def DataFrameToCandle(self,history):
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
        date = np.array([mpd.date2num(pd.to_datetime(dateStr+' 09:30:00+08', '%Y-%m-%d %H:%M:%S').tz_localize('utc')) for dateStr in history.index])         
        quotes = np.array(history.iloc[:][['open','high','low','close']])
        rows = quotes.shape[0]
        colls = quotes.shape[1]
        quotesWithDate = np.append(date,quotes.reshape(rows*colls,1,order='F')).reshape(colls+1,rows)
        # %%
        if len(quotesWithDate) == 0:
            raise SystemExit    
        return quotesWithDate.T    
    #----------------------------------------------------------------------
    def DataFrameToZipline(self,history):
        """
        输入：
   		pandas.DataFrame。
            	Index=Str
        输出：
            	pandas.DataFrame
		Index=Datatime
        """
        date = pd.to_datetime(history.index+' 09:30:00+08','%Y-%m-%d %H:%M:%S')
        date.name='Date'
        close = pd.Series(np.array(history['close']),index=date,name='AAPL')
    
        data = pd.DataFrame(close)
        #data.set_index(date,inplace=True)   
        return data