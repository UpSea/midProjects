import pandas as pd
import tushare as ts
import numpy as np
import time,os
from pandas import DataFrame
from PyQt4 import QtGui,QtCore
import os,sys
upsea = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,os.pardir,'histdata')) 
sys.path.append(upsea) 
from dataCenter import dataCenter
windowsRoot = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,os.pardir,'histdataUI'))
sys.path.append(windowsRoot)
from Widgets.pgCandleWidgetCross import pgCandleWidgetCross 

def getCandleData(code):
    #mid 1)获取历史数据
    #df = ts.get_stock_basics()
    #date = df.ix['600848']['timeToMarket'] #上市日期YYYYMMDD
    
    #本接口还提供大盘指数的全部历史数据，调用时，请务必设定index参数为True,
    #由于大盘指数不存在复权的问题，故可以忽略autype参数。

    df = ts.get_h_data(code,start='2013-06-03', end='2016-05-31') #前复权ts.get_h_data('002337', autype='hfq') #后复权
    #ts.get_h_data('002337', autype=None) #不复权
    #ts.get_h_data('002337', start='2015-01-01', end='2015-03-16') #两个日期之间的前复权数据
    
    #ts.get_h_data('399106', index=True) #深圳综合指数
    
    #mid 2)调用tushareDataManager将历史数据转换为candle数据

    
    
    dc = dataCenter()
    
    dataForCandle = dc.tsCenter.__DataFrameToCandle__(df)
    return dataForCandle

if __name__ == '__main__':
    #----------------------------------------------------------------------
    class MainWindow(QtGui.QMainWindow):
        def __init__(self):
            super(MainWindow, self).__init__()
            dataForCandle = getCandleData('600028')
            cw = pgCandleWidgetCross(dataForCandle=dataForCandle)
            self.setCentralWidget(cw) 
    app = QtGui.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.showMaximized()
    sys.exit(app.exec_())