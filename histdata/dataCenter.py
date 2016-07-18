# -*- coding: utf-8 -*-
'''mid
#ktype 数据类型，D=日k线 W=周 M=月 5=5分钟 15=15分钟 30=30分钟 60=60分钟，默认为D
D
W
M
m5
m15
m30
h1
'''
import os,sys
import pandas as pd
import numpy as np
from tusharedb.tushareDataManager import tushareDataCenter
from mt5db.mt5DataManager import mt5DataCenter
from eastmoneydb.eastmoneyDataManager import eastmoneyDataCenter
class dataCenter():
    def __init__(self):
        #mid init tusharedb
        dataPath = os.path.abspath(os.path.join(os.path.dirname(__file__),'data','csv','tusharedb'))                
        self.tsCenter = tushareDataCenter(dataPath)  
        #mid init mt5db
        dataPath = os.path.abspath(os.path.join(os.path.dirname(__file__),'data','csv','mt5db'))                        
        self.mt5Center = mt5DataCenter(dataPath)
        #mid init eastmoneydb
        dataPath = os.path.abspath(os.path.join(os.path.dirname(__file__),'data','csv','eastmoneydb'))                        
        self.eastmoneyCenter = eastmoneyDataCenter(dataPath)        
        
        self.dataProviders = ['mt5','tushare','eastmoney','yahoo','sina','all']
        self.dataStorages = ['mongodb','csv','all']
    def getDataProviders(self):
        return self.dataProviders
    def getDataStorages(self):
        return self.dataStorages
    def getDataPeriods(self,dataProvider):
        if(dataProvider == 'mt5'):
            return self.mt5Center.localStorage.periods
        if(dataProvider == 'tushare'):
            return self.tsCenter.localStorage.periods
        if(dataProvider == 'eastmoney'):
            return self.eastmoneyCenter.localStorage.periods        
        else:
            raise Exception("Invalid dataProvider.") 
    
    
    # mid 以下两个函数只用于某些demo函数获取历史数据，如此安排可方便统一修改，也用于演示datacenter的调用
    def getCandleData(self,dataProvider = 'tushare',dataStorage = 'mongodb',dataPeriod = 'D',symbol = '600028',dateStart=None,dateEnd = None):
        dataSource={}
        dataSource['dataProvider'] = dataProvider
        dataSource['storageFormat']=dataStorage
        dataSource['dataPeriod']=dataPeriod
        dataSource['symbol']=symbol
        dataSource['dateStart']=dateStart
        dataSource['dateEnd']=dateEnd  
        dataSource['alone'] = True
        dataSource['overlay'] = False   
        
        dataForCandle = self.retriveCandleData(params = dataSource)     
        
        return dataForCandle      
    
    def retriveCandleData(self,params = None):
        '''mid
        return data used to draw candle
        
        '''
        dataProvider = params['dataProvider']
        storageFormat = params['storageFormat']
        
        symbol = params['symbol']
        timeFrom = params['dateStart']
        timeTo = params['dateEnd']
        period = params['dataPeriod']        

        if(dataProvider == "tushare"):
            return self.tsCenter.retriveCandleData(storageType = storageFormat,symbol = symbol,period = period,timeFrom=timeFrom, timeTo=timeTo)
        elif(dataProvider == "mt5"):
            return self.mt5Center.retriveCandleData(storageType = storageFormat,symbol = symbol,period = period,timeFrom=timeFrom, timeTo=timeTo)            
        elif(dataProvider == "eastmoney"):
            return self.eastmoneyCenter.retriveCandleData(storageType = storageFormat,symbol = symbol,period = period,timeFrom=timeFrom, timeTo=timeTo)            
        else:
            raise Exception("Invalid dataProvider.") 
    '''
    def retriveCandleData(self,datasource = 'tushare',storageType = 'mongodb',symbol = '',period = 'D'):
        if (datasource == 'tushare'):
            return self.tsCenter.retriveCandleData(storageType = storageType,symbol = symbol,period = period)
        elif (datasource == 'yahoo'):
            pass
        elif (datasource == 'sina'):
            pass    
    '''
    def retriveHistData(self,params):
        dataProvider = params['dataProvider']
        storageFormat = params['storageFormat']
        
        symbol = params['symbol']
        strStart = params['dateStart']
        strEnd = params['dateEnd']
        period = params['dataPeriod']        

        if(dataProvider == "tushare"):
            dfHistory = self.tsCenter.localStorage.retriveHistData(storageType = storageFormat,symbol = symbol,period = period)
            return dfHistory
        else:
            raise Exception("Invalid dataProvider.") 
    def getLocalAvailableDataSymbols(self,dataType = 'tushare',storageType = 'mongodb',periodType = "D"):
        if(dataType == 'tushare'):
            return self.tsCenter.retriveAvailableSymbols(storageType=storageType,periodType = periodType)
        elif(dataType == 'mt5'):
            return self.mt5Center.retriveAvailableSymbols(storageType=storageType,periodType = periodType)
        elif(dataType == 'eastmoney'):
            return self.eastmoneyCenter.retriveAvailableSymbols(storageType=storageType,periodType = periodType)        
        else:
            raise Exception("Invalid dataProvider.") 
    def getCodes(self,codesType,storageType):
        '''mid
        codes 在储存时不存所获取数据的index，只储存values
        values值中必须要有一列名称为'symbol',这是为了检索时准备
        因为检索时是以symbol为关键字建表的
        '''
        if(codesType == 'tushare'):
            return self.tsCenter.getCodes(storageType)
        elif(codesType == 'mt5'):
            return self.mt5Center.getCodes(storageType)
        elif(codesType == 'yahoo'):
            if(storageType == 'remote'):
                pass
            elif(storageType == 'mongodb'):
                pass
            elif(storageType == 'csv'):
                pass 
        elif(codesType == 'sina'):
            if(storageType == 'remote'):
                pass
            elif(storageType == 'mongodb'):
                pass
            elif(storageType == 'csv'):
                pass             
        elif(codesType == 'datayes'):
            if(storageType == 'remote'):
                pass
            elif(storageType == 'mongodb'):
                pass
            elif(storageType == 'csv'):
                pass    
        return None
    def downloadHistData(self,providerType='tushare',storageType = 'mongodb',periodType='D',codeList=None,timeFrom = None,timeTo = None):
        if(providerType == 'tushare'):
            return self.tsCenter.downloadHistData(storageType=storageType,timeFrom = timeFrom,timeTo = timeTo,
                                                  codeList = codeList,periodType = periodType)
        elif(providerType == 'mt5'):
            return self.mt5Center.downloadHistData(storageType=storageType,timeFrom = timeFrom,timeTo = timeTo,
                                                  codeList = codeList,periodType = periodType)
        elif(providerType == 'eastmoney'):
            return self.eastmoneyCenter.downloadHistData(storageType=storageType,timeFrom = timeFrom,timeTo = timeTo,
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
        #date = pd.to_datetime(history.index+' 00:00:00+00',format='%Y-%m-%d %H:%M:%S')
        date = pd.to_datetime(history.index,format='%Y-%m-%d %H:%M:%S')
        date.name='Date'
        close = pd.Series(np.array(history['close']),index=date,name='AAPL')
    
        data = pd.DataFrame(close)
        #data.set_index(date,inplace=True)   
        return data    
    def getFeedsForZipline(self,params):
        '''mid
        提供回测数据给zipline的唯一接口
        '''
        dfHistory = self.retriveHistData(params)
        return self.__DataFrameToZipline__(dfHistory)

    def removeFromStorage(self,dataProvider = "tushare",storageType = 'mongodb',symbols = None,period='D'):
        if(dataProvider == "tushare"):
            return self.tsCenter.removeFromStorage(storageType = storageType,symbols = symbols,period = period)
        elif(dataProvider == 'yahoo'):
            pass
        elif(dataProvider == 'sina'):
            pass
    def getFeedsForPAT(self,dataProvider = "tushare",storageType = 'mongodb',instruments = [],period='D', timeFrom=None,timeTo=None):
        '''mid
        提供回测数据给PAT调用的唯一接口
        '''
        if(dataProvider == "yahoo"):
            feeds = self.__getFeedFromYahoo(instrument)
        elif(dataProvider == "yahooCsv"):
            feeds = self.__getFeedFromYahooCsv(instrument)
        elif(dataProvider == "tushare"):
            feeds = self.tsCenter.buildFeedForPAT_old(instruments = instruments, timeFrom=timeFrom,timeTo=timeTo, period=period,storageType=storageType)
        elif(dataProvider =="mt5"):
            feeds = self.mt5Center.buildFeedForPAT(instruments = instruments, timeFrom=timeFrom,timeTo=timeTo, period=period,storageType=storageType)
        elif(dataProvider == "generic"):
            feeds = self.__getFeedFromGenericCsv(instrument)
        return feeds        
    def getFeedForPAT(self,dataProvider = "tushare",storageType = 'mongodb',instruments = [],period='D', timeFrom=None,timeTo=None):
        '''mid
        提供回测数据给PAT调用的唯一接口
        '''
        if(dataProvider == "yahoo"):
            feeds = self.__getFeedFromYahoo(instrument)
        elif(dataProvider == "yahooCsv"):
            feeds = self.__getFeedFromYahooCsv(instrument)
        elif(dataProvider == "tushare"):
            feeds = self.tsCenter.buildFeedForPAT(instruments = instruments, timeFrom=timeFrom,timeTo=timeTo, period=period,storageType=storageType)
        elif(dataProvider == "eastmoney"):
            feeds = self.eastmoneyCenter.buildFeedForPAT(instruments = instruments, timeFrom=timeFrom,timeTo=timeTo, period=period,storageType=storageType)
        elif(dataProvider =="mt5"):
            feeds = self.mt5Center.buildFeedForPAT(instruments = instruments, timeFrom=timeFrom,timeTo=timeTo, period=period,storageType=storageType)
        elif(dataProvider == "generic"):
            feeds = self.__getFeedFromGenericCsv(instrument)
        return feeds           
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

# mid 以下两个函数只用于某些demo函数获取历史数据，如此安排可方便统一修改，也用于演示datacenter的调用
def getCandleData(dataProvider = 'tushare',dataStorage = 'mongodb',dataPeriod = 'D',symbol = '600028',dateStart=None,dateEnd = None):
    dataSource={}
    dataSource['dataProvider'] = dataProvider
    dataSource['storageFormat']=dataStorage
    dataSource['dataPeriod']=dataPeriod
    dataSource['symbol']=symbol
    dataSource['dateStart']=dateStart
    dataSource['dateEnd']=dateEnd  
    dataSource['alone'] = True
    dataSource['overlay'] = False   
    
    dc = dataCenter()        
    dataForCandle = dc.retriveCandleData(params = dataSource)     
    
    return dataForCandle   
def getRawData():
    import os,sys
    dataRoot = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,os.pardir,'histdata'))        
    sys.path.append(dataRoot)        
    import dataCenter as dataCenter          
    dataSource={}        
    dataSource['dataProvider'] = 'tushare'
    dataSource['storageFormat']='mongodb'
    dataSource['dataPeriod']='D'
    dataSource['symbol']='600028'
    dataSource['dateStart']='2015-03-19'
    dataSource['dateEnd']='2015-12-31'  
    dataSource['alone'] = True
    dataSource['overlay'] = False            
    
    dataCenter = dataCenter.dataCenter()
    
    data = dataCenter.retriveHistData(params = dataSource)   
    
    return data
if __name__ == '__main__':
    import os,sys        
    from PyQt4 import QtGui,QtCore
    
    app = QtGui.QApplication([])   
    
    dialog = QtGui.QDialog()
    layout = QtGui.QHBoxLayout()
    dialog.setLayout(layout)   
    
    
    table = QtGui.QTableWidget()   
    table.clear()
    header = ['datetime','open','high','low','close']
    table.setHorizontalHeaderLabels(header)     #mid should be after .setColumnCount()
    if(True):#mid 用于演示candledata的获取和使用
        candleData = getCandleData()  
        table.setColumnCount(len(header))
        table.setRowCount(len(candleData))      
        for row in range(len(candleData[:,0])):
            print (row)
            for column in range(len(candleData[0,:])):
                print (column)
                table.setItem(row,column,QtGui.QTableWidgetItem(str(candleData[row, column]))) 
    else:#mid 用于演示histdata的获取和使用
        dfLocalSymbols = getRawData()
        table.setRowCount(len(dfLocalSymbols))
        table.setColumnCount(len(header))
        
        for row in range(len(dfLocalSymbols.index)):
            for column in range(len(dfLocalSymbols.columns)):
                table.setItem(row,column,QtGui.QTableWidgetItem(str(dfLocalSymbols.iget_value(row, column))))   
                
    layout.addWidget(table)
    dialog.showMaximized()    

    
    sys.exit(app.exec_())