# -*- coding: utf-8 -*-
import socket
import struct
import sys,os

dataRoot = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir))        
sys.path.append(dataRoot) 

dataRoot = os.path.abspath(os.path.dirname(__file__))        
sys.path.append(dataRoot) 

from data.localStorage import localStorage
from mt5Remote import remoteStorage
import mt5Interface as mt5Interface
import logbook  
logbook.StderrHandler().push_application()

class mt5DataCenter():
    def __init__(self,dataRoot):
        self.localStorage = localStorage(dataRoot,'Mt5','D')
        
        #mid periods 用于将本地使用的周期符号转换为远端系统使用的周期符号，在从远端下载数据时用
        #mid mt5在远端以0x09表示日线周期
        #mid tushare在远端以'D'表示日线周期，需要分别定义
        self.localStorage.periods = mt5Interface.periods  
        
        self.remoteStorage = remoteStorage('192.168.0.212',5050)     
        #self.logger =  pyalgotrade.logger.getLogger("mt5")
        self.logger = logbook.Logger('mt5')    
        
    def getCodes(self,storageType = ""):
        if(storageType == 'remote'):
            codes = self.remoteStorage.downloadCodes()
            #codes.index = codes['code']
            
            storage = self.localStorage.getCodesStorage()
            if(storage == 'mongodb'):
                self.localStorage.mongodb.removeItem(collection='codes')          
                codesDict = codes.T.to_dict()
                dictList = list()
                for code in codesDict:
                    dictList.append(codesDict[code])          
                self.localStorage.mongodb.insert(dictList)  
            elif(storage == 'csv'):
                codes.to_csv(self.localStorage.codefile,encoding='gbk',index=False)    
            return codes
        elif(storageType == 'mongodb' or storageType == 'csv'):
            return self.localStorage.retriveCodes(storageType = storageType)
        else:
            raise Exception("mt5 datacenter,Invalid frequency.");
    def downloadAndStoreKDataByCode(self,code = '',period="D",timeFrom = None,timeTo = None):
        #ktype 数据类型，D=日k线 W=周 M=月 5=5分钟 15=15分钟 30=30分钟 60=60分钟，默认为D
        
        histDataOne = self.remoteStorage.downloadKData(symbol = code,periodType = self.localStorage.periods[period],timeFrom =timeFrom,timeTo =timeTo)
        self.localStorage.storeHistDataOneToCsv(code = code,period = period,histDataOne = histDataOne)

    def downloadHistData(self,codeList = None,periodType = 'D',timeFrom = None,timeTo = None,storageType =  'mongodb'):
        dic = {}
        for code in codeList:   
            data = self.remoteStorage.downloadKData(symbol = code,periodType = self.localStorage.periods[periodType],timeFrom =timeFrom,timeTo =timeTo)  
            #print 'begin to download:',code
            if data is not None:
                dic[code] = data
                #print i,code,type(code)

        #mid ---------------------------------------------------------------------
        if(storageType == 'mongodb'):
            self.localStorage.mongodb.setCollection(periodType)
            
            if(False):
                for code in dic:
                    quotesDict = dic[code].to_dict()
                    quotesDict['symbol'] = code
                    self.mongodb.insert(quotesDict)      
            else:
                for code in dic:
                    quotesDf = dic[code]
                    index = [str(ds) for ds in dic[code].index]
                    quotesDf.index = index
                    quotesDict = quotesDf.to_dict()
                    quotesDict['symbol'] = code
                    self.localStorage.mongodb.insert(quotesDict)                         
        elif(storageType == 'csv'):
            for code in dic:
                #mid 判断是否存在文件夹，如不存在，则创建
                self.localStorage.storeHistDataOneToCsv(code = code,period = periodType,histDataOne = dic[code])
        #mid ----------------------------------------------------------------------
        return dic    
    def retriveAvailableSymbols(self,storageType = 'mongodb' , periodType = 'D'):
        if(storageType == 'mongodb'):
            if(periodType in self.localStorage.periods.keys()):
                codes = self.localStorage.mongodb.retriveSymbolsAll(period =periodType)             
                return codes    
            else:
                pass
        elif(storageType == 'csv'):
            pass   
    def retriveCandleData(self,storageType = 'mongodb',symbol = '',period = 'D',timeFrom = None,timeTo = None):
        '''mid
        将dataframe格式历史数据转化为用于绘制canlde 的数据
        '''
        return self.localStorage.retriveCandleData(storageType = storageType,period = period,symbol = symbol,timeFrom=timeFrom, timeTo=timeTo)
    def buildFeedForPAT(self,instruments = [], timeFrom=None,timeTo=None, storageType = 'csv', period='D', timezone=None, skipErrors=False):
        '''mid
        创建用于PAT的feeds，返回格式为单个feed(将所有数据都填入一个feed)
        '''
        import feedsForPAT as feedsForPAT 
        feed = feedsForPAT.Feed(dataCenter=self,frequency=period)
        ret = feed.build_feed(instruments=instruments, timeFrom = timeFrom, timeTo = timeTo, storageType=storageType,period=period)           
        return ret   
    def buildFeedForPAT_old(self,instruments = [], timeFrom = None, timeTo = None, storageType = 'csv', period='D', timezone=None, skipErrors=False):
        '''mid
        创建用于PAT的feeds，返回格式为字典，这个或许需要修改为单个feed(将所有数据都填入一个feed)
        '''
        import feedsForPAT as feedsForPAT 
        feeds = {}
        for instrument in instruments:
            feed = feedsForPAT.Feed(dataCenter=self,frequency=period)
            feeds[instrument] = feed.build_feed(instrument=instrument, timeFrom=timeFrom, timeTo=timeTo, storageType=storageType,period=period)           
        return feeds    
if __name__ == "__main__":
    dataRoot = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir))        
    sys.path.append(dataRoot)  
    
    dataPath = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,'data','csv','mt5db'))                    
    mt5Center = mt5DataCenter(dataPath)   
    
    logbook.StderrHandler().push_application()
    log = logbook.Logger('Algorithm')    
    if(True):
        data = mt5Center.downloadHistData(['XAUUSD'])
                    
        for i,code in enumerate(data):
            df = data[code]
            for i,row in enumerate(df.itertuples()):
                log.info( '%05d---%s' % (i,str(row)))
    if(True):
        dfCodes = mt5Center.getCodes('mongodb')
        for i,code in enumerate(dfCodes.itertuples()):
            log.info('%05d---%s'%(i,str(code)))          