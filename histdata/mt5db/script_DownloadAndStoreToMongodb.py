# -*- coding: utf-8 -*-
import os,sys
from PyQt4 import QtGui,QtCore

dataRoot = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,os.pardir,'histdata'))        
sys.path.append(dataRoot)        
import dataCenter as dataCenter    
from data.mongodb.DataSourceMongodb import Mongodb
import datetime as dt
def getSymbols():
    #mid 1)从excel赋值粘贴获得如下数据
    codesStr = """
               XAGUSD 
               """
    #mid 2)将字符串使用split()分割为list，默认会去除\n和所有空格。
    #codeList = ['000021.SZ','000022.SZ']
    codeList = [code.split('.')[0] for code in codesStr.split()]     
    return codeList
def subMain():
    DC = dataCenter.dataCenter()
    remoteDataSourceType = 'mt5'
    localStorageType = 'mongodb' 
    periodType = 'D'
    
    timeStart = dt.datetime(2000,10,20)
    timeEnd = dt.datetime.now()    
    
    # 1)get codes form eastmoney
    codeList =  getSymbols()
    # 2)download history data
    dataDict = DC.downloadHistData(providerType=remoteDataSourceType,storageType=localStorageType,periodType=periodType,
                                                codeList=codeList,timeFrom = timeStart,timeTo = timeEnd)
        
if __name__ == '__main__':
    #app = QtGui.QApplication(sys.argv)
    #mid-----------------------------------------------------------------------------------------------------------------------------

    subMain()
    
    #mid-----------------------------------------------------------------------------------------------------------------------------
    #sys.exit(app.exec_())       