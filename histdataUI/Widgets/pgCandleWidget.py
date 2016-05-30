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
    
    import os,sys
    dataRoot = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,os.pardir,'histdata'))        
    sys.path.append(dataRoot)        
    import dataCenter as dataCenter   
    candleData = dataCenter.getCandleData()  
    
    
    mw = pgCandleWidget(dataForCandle=candleData)
    
    mw.showMaximized()
    sys.exit(app.exec_())