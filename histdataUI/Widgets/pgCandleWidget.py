# -*- coding: utf-8 -*-
import sys,os
xpower = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,os.pardir,'thirdParty','pyqtgraph-0.9.10'))
sys.path.append(xpower)
xpower = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir))
sys.path.append(xpower)
from PyQt4 import QtCore, QtGui
from Widgets.pgCandleItem import CandlestickItem
import pyqtgraph as pg

class pgCandleWidget(pg.PlotWidget):
    def __init__(self, dataForCandle=None):
        super(pgCandleWidget, self).__init__()
        item01 = CandlestickItem(dataForCandle)        
        self.addItem(item01) 
        
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    
    def getCandleData():
        import os,sys        
        xpower = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,os.pardir,'histdata'))
        sys.path.append(xpower)
    
        import feedsForCandle as feedsForCandle
    
        dataSource={}
        dataSource['ip']='192.168.0.212'
        dataSource['port']=27017
        dataSource['database']='Tushare'
        dataSource['symbol']='600028'
        dataSource['dateStart']='2013-08-19'
        dataSource['dateEnd']='2015-08-31'
        dataSource['frequency']='D'
        dataForCandle = feedsForCandle.GetCandlesFromMongodb(dataSource)
        return dataForCandle    
    
    candleData = getCandleData()
    
    mw = pgCandleWidget(dataForCandle=candleData)
    
    mw.showMaximized()
    sys.exit(app.exec_())