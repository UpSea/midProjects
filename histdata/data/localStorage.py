# -*- coding: utf-8 -*-
import sys,os
from PyQt4 import QtGui,QtCore

"""mid
不同数据源在本地有统一的csv和mongodb储存，特将本地储存安排在此类统一提供本地数据处理
"""
class localStorage():
    def __init__(self,dataRoot,db,collection):
        self.dataRoot = dataRoot      
        self.codefile = self.dataRoot +os.sep + "code.csv"   
        self.codeinusefile = self.dataRoot + os.sep + "code_inuse.csv"
        self.codenewinusefile = self.dataRoot + os.sep + "code_new_inuse.csv"
    
        from data.mongodb.DataSourceMongodb import Mongodb
        connect = Mongodb()
        connect.use(db)    #database
        connect.setCollection(collection)    #table
        self.mongodb = connect
    def getCodesStorage(self):  
        selectorMsgBox=QtGui.QMessageBox()  
        selectorMsgBox.setWindowTitle("select codes storage.")  
        mongodbButton=selectorMsgBox.addButton("mongodb",QtGui.QMessageBox.ActionRole)  
        csvButton=selectorMsgBox.addButton("csv",QtGui.QMessageBox.ActionRole)  
        cancelButton=selectorMsgBox.addButton("do not store",QtGui.QMessageBox.ActionRole)  

        selectorMsgBox.setText("select codes storage!")  
        selectorMsgBox.exec_()  

        button=selectorMsgBox.clickedButton()  
        if button==mongodbButton:  
            return 'mongodb' 
        elif button==csvButton:  
            return 'csv' 
        elif button==cancelButton:  
            return 'cancel'      

    def retriveHistData(self,storageType = 'mongodb',period = '',symbol = ''):
        '''mid
        返回dataframe格式的历史数据,用于pat回测
        '''
        if(storageType == 'mongodb'):
            dfHistData = self.mongodb.retrive(symbol = symbol,period=period)
        elif(storageType == 'csv'):
            dfHistData = self.__retriveDataFrameKData__(symbol = symbol,period=period)
        return dfHistData    
    def retriveCandleData(self,storageType = 'mongodb',period = '',symbol = ''):
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
        import pandas as pd
        import numpy as np
        import matplotlib.dates as mpd
        import datetime as dt        
        #date = np.array([mpd.date2num(dt.datetime.strptime(dateStr, '%Y-%m-%d')) for dateStr in history.index])      
        import sys
        
        #mid 这个转换是将dataframe格式的数据转化为np.array格式，转换时排列的顺序重要
        #mid 必须确保是按时间index的升序排列
        history = self.retriveHistData(storageType=storageType, period=period,symbol=symbol)
        history.sort_index(inplace=True,ascending=True)
        
        if sys.version > '3':
            PY3 = True
        else:
            PY3 = False    
        if (PY3 == True):
            '''mid
            tushare有两个获取历史数据的函数
            get_h_data，他返回的数据index为pd.core.index.Index，item类型为str
            get_hist_data，他返回的数据index为pd.tseries.index.DatetimeIndex，item类型为Timestamp
            需要区别对待转换为num
            '''
            if(type(history.index) is pd.core.index.Index):
                #date = np.array([mpd.date2num(pd.to_datetime(dateStr+' 09:30:00+08',format= '%Y-%m-%d %H:%M:%S').tz_localize('utc')) for dateStr in history.index]) 
                date = np.array([mpd.date2num(pd.to_datetime(dateStr,format= '%Y-%m-%d %H:%M:%S').tz_localize('utc')) for dateStr in history.index]) 
            elif(type(history.index) is pd.tseries.index.DatetimeIndex):
                date = np.array([mpd.date2num(Timestamp) for Timestamp in history.index])                        
        else:
            if(type(history.index) is pd.core.index.Index):
                #date = np.array([mpd.date2num(pd.to_datetime(dateStr+' 09:30:00+08','%Y-%m-%d %H:%M:%S').tz_localize('utc')) for dateStr in history.index]) 
                date = np.array([mpd.date2num(pd.to_datetime(dateStr,format= '%Y-%m-%d %H:%M:%S').tz_localize('utc')) for dateStr in history.index]) 
            elif(type(history.index) is pd.tseries.index.DatetimeIndex):
                date = np.array([mpd.date2num(Timestamp) for Timestamp in history.index])                 
            
        if(len(history) == 0):
            return None
        ohlc = history.iloc[:][['open','high','low','close']]
        quotes = np.array(ohlc)
        rows = quotes.shape[0]
        colls = quotes.shape[1]
        quotesWithDate = np.append(date,quotes.reshape(rows*colls,1,order='F')).reshape(colls+1,rows)
        # %%
        if len(quotesWithDate) == 0:
            raise SystemExit    
        return quotesWithDate.T           
    def retriveCodes(self,sourceType):
        if(sourceType == 'mongodb'):
            self.mongodb.setCollection('codes')
            codes = self.mongodb.retriveCodes()
            return codes
        elif(sourceType == 'csv'):
            dfCodes = pd.read_csv(self.codefile,index_col=False,encoding='gbk',dtype={0:np.str,1:np.str})
            dfCodes.index = dfCodes['code']
            return dfCodes          
        