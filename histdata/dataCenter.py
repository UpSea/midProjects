# -*- coding: utf-8 -*-
import os,sys
import pandas as pd
import numpy as np
from tusharedb.tushareDataManager import tushareDataCenter
        
class dataCenter():
    def __init__(self):
        dataPath = os.path.abspath(os.path.join(os.path.dirname(__file__),'data','csv','tusharedb'))                
        self.tsCenter = tushareDataCenter(dataPath)
    def retriveCandleData(self,params = None):
        '''mid
        return data used to draw candle
        
        '''
        dataProvider = params['dataProvider']
        storageFormat = params['storageFormat']
        
        symbol = params['symbol']
        strStart = params['dateStart']
        strEnd = params['dateEnd']
        frequency = params['frequency']        

        if(dataProvider == "tushare"):
            return self.tsCenter.retriveCandleData(storageType = storageFormat,symbol = symbol,period = frequency)

        elif(dataProvider == 'yahoo'):
            pass
        elif(dataProvider == 'sina'):
            pass
    '''
    def retriveCandleData(self,datasource = 'tushare',storageType = 'mongodb',symbol = '',period = 'D'):
        if (datasource == 'tushare'):
            return self.tsCenter.retriveCandleData(storageType = storageType,symbol = symbol,period = period)
        elif (datasource == 'yahoo'):
            pass
        elif (datasource == 'sina'):
            pass    
    '''
    def retriveHistData(self,symbol = ''):
        return self.tsCenter.retriveHistData(storageType = 'mongodb',symbol = symbol)
    def getLocalAvailableDataSymbols(self,dataType = 'tushare',storageType = 'mongodb',periodType = "D"):
        if(dataType == 'tushare'):
            return self.tsCenter.retriveAvailableSymbols(storageType=storageType,periodType = periodType)
        elif(dataType == 'yahoo'):
            pass        
        elif(dataType == 'sina'):
            pass
        else:
            pass
    def getCodes(self,codesType,sourceType):
        if(codesType == 'tushare'):
            return self.tsCenter.getCodes(sourceType)
        elif(codesType == 'yahoo'):
            if(sourceType == 'remote'):
                pass
            elif(sourceType == 'mongodb'):
                pass
            elif(sourceType == 'csv'):
                pass 
        elif(codesType == 'sina'):
            if(sourceType == 'remote'):
                pass
            elif(sourceType == 'mongodb'):
                pass
            elif(sourceType == 'csv'):
                pass             
        elif(codesType == 'datayes'):
            if(sourceType == 'remote'):
                pass
            elif(sourceType == 'mongodb'):
                pass
            elif(sourceType == 'csv'):
                pass    
        return None
    def downloadHistData(self,providerType='tushare',storageType = 'mongodb',periodType='D',codeList=None,timeStart='',timeEnd=''):
        if(providerType == 'tushare'):
            return self.tsCenter.downloadHistData(storageType=storageType,timeStart=timeStart,timeEnd=timeEnd,
                                                  codeList = codeList,periodType = periodType)
        elif(providerType == 'yahoo'):
            pass
        elif(providerType == 'datayes'):
            pass
        elif(providerType == 'sina'):
            pass
    def __DataFrameToZipline__(self,history):
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
    def getFeedsForZipline(self,params):
        '''mid
        提供回测数据给zipline的唯一接口
        '''
        dataProvider = params['dataProvider']
        storageFormat = params['storageFormat']
        
        symbol = params['symbol']
        strStart = params['dateStart']
        strEnd = params['dateEnd']
        frequency = params['frequency']        

        if(dataProvider == "tushare"):
            if(storageFormat == 'mongodb'):
                dfHistory = self.retriveHistData(symbol)
                return self.__DataFrameToZipline__(dfHistory)
            elif(storageFormat == 'csv'):
                pass
        elif(dataProvider == 'yahoo'):
            pass
        elif(dataProvider == 'sina'):
            pass
    def getFeedsForPAT(self,feedFormat = "tushareCsv",instrument = ""):
        '''mid
        提供回测数据给PAT调用的唯一接口
        '''
        if(feedFormat == "yahoo"):
            feed = self.__getFeedFromYahoo(instrument)
        elif(feedFormat == "yahooCsv"):
            feed = self.__getFeedFromYahooCsv(instrument)
        elif(feedFormat == "tushareCsv"):
            feed = self.__getFeedFromTushareCsv(instrument)
        elif(feedFormat == "tushare"):
            import sys,os
            dataPath = os.path.abspath(os.path.join(os.path.dirname(__file__),'data','csv','tusharedb'))                
            feed = self.tsCenter.buildFeedForPAT([instrument], 2015, 2015, dataPath)
        elif(feedFormat == "generic"):
            feed = self.__getFeedFromGenericCsv(instrument)
        return feed           
    def __getFeedFromGenericCsv(self,instrument):
        '''mid
        使用系统自定义的与数据提供者的数据格式相互独立的csv格式储存的文件
        可以作为用户管理各种数据源的统一格式使用
        '''
        from pyalgotrade.barfeed.csvfeed import GenericBarFeed
        from pyalgotrade import bar
        frequency = bar.Frequency.DAY
        barfeed = GenericBarFeed(frequency)
        barfeed.setDateTimeFormat('%Y-%m-%d %H:%M:%S')
        
        dataRoot = os.path.abspath(os.path.join(os.path.dirname(__file__),'data','generic','csv'))        
        filename = dataRoot+os.sep+'day'+os.sep+('%s.csv'%instrument)          
        barfeed.addBarsFromCSV(instrument, filename) 
        return barfeed
    def __getFeedFromTushareCsv(self,instrument):
        '''mid
        直接读取某个tushare格式的csv文件到pandas，再解析为feed格式返回
        '''
        import tusharedb.feedsForPAT as feedsForPAT        
        dataRoot = os.path.abspath(os.path.join(os.path.dirname(__file__),'data','tusharedb','csv'))        
        filename = dataRoot+os.sep+'day'+os.sep+('%s.csv'%instrument)          
    
        dat = pd.read_csv(filename,index_col=0,encoding='gbk')
        feed = feedsForPAT.Feed()
        feed.addBarsFromDataFrame(instrument, dat)   
        return feed
    def __getFeedFromYahooCsv(self,instrument,fromYear = 2014,toYear = 2016):   
        from pyalgotrade.barfeed import yahoofeed        
        feed = yahoofeed.Feed()
        import sys,os
        dataPath = os.path.abspath(os.path.join(os.path.dirname(__file__),'data','yahoodb','csv'))    
        
        for year in range(fromYear, toYear+1):
            fileName = os.path.join(dataPath, "%s-%d-yahoofinance.csv" % (instrument, year))
            if os.path.exists(fileName):              
                feed.addBarsFromCSV(instrument, fileName)  
        return feed
    def __getFeedFromYahoo(self,instrument):
        from pyalgotrade.tools import yahoofinance        
        import sys,os
        dataPath = os.path.abspath(os.path.join(os.path.dirname(__file__),'data','yahoodb','csv'))          
        feed = yahoofinance.build_feed([instrument], 2015, 2015, dataPath)    
        return feed    