# -*- coding: utf-8 -*-
import sys
sys.path.append('/home/mid/PythonProjects/xpower/pyqtgraph-0.9.10')
sys.path.append('/home/mid/PythonProjects/xpower')
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
        import sys
        #mid 0) append relatibe path
        #from pathlib import Path # if you haven't already done so
        #root = Path(__file__).resolve().parents[1].path
        # For older Python:
        from os.path import dirname, realpath
        root = dirname(dirname(realpath(__file__)))
        sys.path.append(root)  
        
        #mid 1)append absolute path
        #sys.path.append('/home/mid/PythonProjects/xpower') 
        
        from DataSources.GetDataFromMongodb import GetDataFromMongodb

        dataSource={}
        dataSource['ip']='192.168.1.100'
        dataSource['port']=27017
        dataSource['database']='Tushare'
        dataSource['symbol']='600311'
        dataSource['dateStart']='2013-08-19'
        dataSource['dateEnd']='2015-08-31'
        dataSource['frequency']='D'
        dataForZipline,dataForCandle = GetDataFromMongodb(dataSource)
        return dataForCandle    
    
    candleData = getCandleData()
    
    mw = pgCandleWidget(dataForCandle=candleData)
    
    mw.show()
    sys.exit(app.exec_())