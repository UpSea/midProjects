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
    codesStr = """600000.SH
    600010.SH
    600016.SH
    600028.SH
    600029.SH
    600030.SH
    600036.SH
    600048.SH
    600050.SH
    600104.SH
    600109.SH
    600111.SH
    600518.SH
    600519.SH
    600637.SH
    600795.SH
    600837.SH
    600887.SH
    600893.SH
    600958.SH
    600999.SH
    601006.SH
    601088.SH
    601166.SH
    601169.SH
    601186.SH
    601211.SH
    601288.SH
    601318.SH
    601328.SH
    601336.SH
    601377.SH
    601390.SH
    601398.SH
    601601.SH
    601628.SH
    601668.SH
    601669.SH
    601688.SH
    601727.SH
    601766.SH
    601788.SH
    601800.SH
    601818.SH
    601857.SH
    601919.SH
    601985.SH
    601988.SH
    601989.SH
    601998.SH
    """
    #mid 2)将字符串使用split()分割为list，默认会去除\n和所有空格。
    #codeList = ['000021.SZ','000022.SZ']
    codeList = [code.split('.')[0] for code in codesStr.split()]     
    return codeList
def subMain():
    DC = dataCenter.dataCenter()
    remoteDataSourceType = 'tushare'
    localStorageType = 'mongodb' 
    periodType = 'D'
    
    timeStart = dt.datetime(2010,10,20)
    timeEnd = dt.datetime.now()    
    
    # 1)get codes form eastmoney
    codeList =  getSymbols()
    codeList = "510050"
    # 2)download history data
    dataDict = DC.downloadHistData(providerType=remoteDataSourceType,storageType=localStorageType,periodType=periodType,
                                                codeList=codeList,timeFrom = timeStart,timeTo = timeEnd)
        
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    #mid-----------------------------------------------------------------------------------------------------------------------------

    subMain()
    
    #mid-----------------------------------------------------------------------------------------------------------------------------
    sys.exit(app.exec_())       