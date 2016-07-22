# -*- coding: utf-8 -*-
import sys,os
from PyQt4 import QtGui,QtCore
import pandas as pd
import datetime as dt        
import logbook  
logbook.StderrHandler().push_application()
"""mid
不同数据源在本地有统一的csv和mongodb储存，特将本地储存安排在此类统一提供本地数据处理
"""
class localStorage():
    def __init__(self,dataRoot,db,collection):
        self.periods = None #mid should be redefined when used in dataManager
        self.dataRoot = dataRoot      
        self.codefile = self.dataRoot +os.sep + "code.csv"   
        self.codeinusefile = self.dataRoot + os.sep + "code_inuse.csv"
        self.codenewinusefile = self.dataRoot + os.sep + "code_new_inuse.csv"
    
        from data.mongodb.DataSourceMongodb import Mongodb
        connect = Mongodb()
        connect.use(db)    #database
        connect.setCollection(collection)    #table
        self.mongodb = connect
        self.logger = logbook.Logger('localStorage')    
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

    def retriveHistData(self,storageType = 'mongodb',period = '',symbol = '', timeFrom=None, timeTo=None):
        '''mid
        返回dataframe格式的历史数据,用于pat回测,
        historyDf.index is str as "%Y-%m-%d %H:%M:%S",this index will be parsed when building feed in build feed function.
        '''
        if(storageType == 'mongodb'):
            ret = self.mongodb.retrive(symbol = symbol,period=period,timeFrom=timeFrom, timeTo=timeTo)
            
            '''mid below codes only for py2
            try:#mid here should be exception process in case server is not responsable
                ret = self.mongodb.retrive(symbol = symbol,period=period,timeFrom=timeFrom, timeTo=timeTo)
            except Exception, e:
                print str(e)
                raise e            
            '''
        elif(storageType == 'csv'):
            fileName = os.path.join(self.dataRoot,period,('%s.csv'%symbol))
            historyDf = pd.DataFrame.from_csv(fileName)
            #historyDf = pd.DataFrame.from_csv(fileName).tz_localize('UTC')
            historyDf.sort_index(inplace=True,ascending=True)                
            
            datetimeStr = [str(timestamp).decode() for timestamp in historyDf.index]
            
            historyDf.index = datetimeStr
            
            if(isinstance(timeFrom,dt.datetime) and isinstance(timeTo,dt.datetime)):
                strFrom = timeFrom.strftime("%Y-%m-%d %H:%M:%S").decode()
                strTo = timeTo.strftime("%Y-%m-%d %H:%M:%S").decode()
                '''mid
                以下以时间为标准对historyDf做切片操作
                在py2 linux 下，strFrom和strTo不必必须包含在historyDf的index中
                在py2 window下，strFrom和strTo必须要在historyDf的index中存在时才能通过，
                不知何意，此处index为uncode类型字符串
                '''
                ret = historyDf[strFrom:strTo]
            else:
                ret = historyDf            
        return ret    
    def retriveCandleData(self,storageType = 'mongodb',period = '',symbol = '',timeFrom = None,timeTo = None):
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
        import platform;

        #mid 这个转换是将dataframe格式的数据转化为np.array格式，转换时排列的顺序重要
        #mid 必须确保是按时间index的升序排列
        history = self.retriveHistData(storageType=storageType, period=period,symbol=symbol,timeFrom=timeFrom, timeTo=timeTo)
        history.sort_index(inplace=True,ascending=True)
        
        if sys.version > '3':
            PY3 = True
        else:
            PY3 = False   
            
        sysstr = platform.system()
        '''mid
            tushare有两个获取历史数据的函数
            get_h_data，他返回的数据index为pd.core.index.Index，item类型为str
            get_hist_data，他返回的数据index为pd.tseries.index.DatetimeIndex，item类型为Timestamp
            需要区别对待转换为num
        '''        
        if(sysstr =="Windows"):
            if(type(history.index) is pd.core.index.Index):
                #date = np.array([mpd.date2num(pd.to_datetime(dateStr+' 09:30:00+08','%Y-%m-%d %H:%M:%S').tz_localize('utc')) for dateStr in history.index])
                
                history = history[history.index != 'NaT'] #mid eastmoney 有时候会出现此值，特过滤
                
                date = np.array([mpd.date2num( pd.to_datetime(dateStr,'%Y-%m-%d %H:%M:%S').tz_localize('utc')) for dateStr in history.index]) 
            elif(type(history.index) is pd.tseries.index.DatetimeIndex):
                date = np.array([mpd.date2num(Timestamp) for Timestamp in history.index])            
        elif(sysstr == "Linux"):  
            if(type(history.index) is pd.core.index.Index):
                #date = np.array([mpd.date2num(pd.to_datetime(dateStr+' 09:30:00+08','%Y-%m-%d %H:%M:%S').tz_localize('utc')) for dateStr in history.index]) 
                
                history = history[history.index != 'NaT'] #mid eastmoney 有时候会出现此值，特过滤
                
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
    def retriveCodes(self,storageType = ""):
        if(storageType == 'mongodb'):
            self.mongodb.setCollection('codes')
            codes = self.mongodb.retriveCodes()
            return codes
        elif(storageType == 'csv'):
            dfCodes = pd.read_csv(self.codefile,index_col=False,encoding='gbk',dtype={0:np.str,1:np.str})
            dfCodes.index = dfCodes['code']
            return dfCodes        
        else:
            raise Exception("localStorage,invalid storageType")
    def exists(self,instrument,frequency):
        if (frequency in self.periods.keys()):
            fileName = os.path.join(self.dataRoot,frequency,('%s.csv'%instrument))
            if os.path.exists(fileName):
                return True
            else:
                return False               
        else:
            raise Exception("Invalid frequency")
    def storeHistDataOneToCsv(self,code = '',period = 'D',histDataOne = None):
        fileName = os.path.join(self.dataRoot,period,('%s.csv'%code))
        fileDir = os.path.dirname(fileName)   
        
        #mid 判断是否存在文件夹，如不存在，则创建
        if not os.path.exists(fileDir):
            self.logger.info("Creating %s directory" % (fileDir))
            os.mkdir(fileDir)        
        
        #mid 判断是否存在已有同名文件，如有追加，如无，创建
        if histDataOne is not None and len(histDataOne) != 0:
            if os.path.exists(fileName):
                histDataOne.to_csv(fileName, mode='a', header=None,encoding='gbk')
            else:
                histDataOne.to_csv(fileName,encoding='gbk')
            return True
        else:
            return False         
    