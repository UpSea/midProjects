# -*- coding: utf-8 -*-
import os,sys
from PyQt4 import QtGui,QtCore

dataRoot = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,os.pardir,'histdata'))        
sys.path.append(dataRoot)        
import dataCenter as dataCenter    
from data.mongodb.DataSourceMongodb import Mongodb
import datetime as dt
if __name__ == '__main__':
    #app = QtGui.QApplication(sys.argv)
    #mid-----------------------------------------------------------------------------------------------------------------------------
    
    
    dataCenter = dataCenter.dataCenter()

    codeList = ['000021.SZ','000022.SZ']

    remoteDataSourceType = 'eastmoney'
    localStorageType = 'mongodb' 
    periodType = 'D'
    
    
    timeStart = dt.datetime(2010,10,20)
    timeEnd = dt.datetime.now()
                
    # 2)download history data
    dataDict = dataCenter.downloadHistData(providerType=remoteDataSourceType,storageType=localStorageType,periodType=periodType,
                                                codeList=codeList,timeFrom = timeStart,timeTo = timeEnd)
    
    
    
    #mid-----------------------------------------------------------------------------------------------------------------------------
    #sys.exit(app.exec_())       