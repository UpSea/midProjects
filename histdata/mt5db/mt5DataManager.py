# -*- coding: utf-8 -*-
import socket
import struct
import sys,os

dataRoot = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir))        
sys.path.append(dataRoot) 
from data.localStorage import localStorage
from mt5Remote import remoteStorage

class mt5DataCenter():
    def __init__(self,dataRoot):
        self.localStorage = localStorage(dataRoot,'Mt5','D')
        self.remoteStorage = remoteStorage('192.168.0.212',5050)     
    
    def getCodes(self,sourceType):
        if(sourceType == 'remote'):
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
        else:
            return self.localStorage.retriveCodes(sourceType)
    def downloadHistData(self,codeList = None,periodType = 'D',timeStart ='2000-01-01',timeEnd = '2016-05-20',storageType =  'mongodb'):
        dic = {}
        for code in codeList:   
            data = self.remoteStorage.downloadKData(code)  
            print 'begin to download:',code
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
                fileName = os.path.join(self.dataRoot,periodType,('%s.csv'%code))
                fileDir = os.path.dirname(fileName)     
                if not os.path.exists(fileDir):
                    self.logger.info("Creating %s directory" % (fileDir))
                    os.mkdir(fileDir)                   
                dic[code].to_csv(fileName,encoding='gbk')
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
    def retriveCandleData(self,storageType = 'mongodb',symbol = '',period = 'D'):
        '''mid
        将dataframe格式历史数据转化为用于绘制canlde 的数据
        '''
        return self.localStorage.retriveCandleData(storageType = storageType,period = period,symbol = symbol)
if __name__ == "__main__":
    dataRoot = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir))        
    sys.path.append(dataRoot)  
    
    dataPath = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,'data','csv','mt5db'))                    
    mt5Center = mt5DataCenter(dataPath)   
    
    if(True):
        data = mt5Center.downloadHistData(['XAUUSD'])
        
        
        if(data is not None):
            quotesDict = data.to_dict()           
        
        
        for i,code in enumerate(data):
            print i,'----',code
    if(True):
        dfCodes = mt5Center.reqCodes()
        for code in dfCodes.values:
            print '----',code          