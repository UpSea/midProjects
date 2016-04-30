# -*- coding: utf-8 -*-
import sys
sys.path.append('/home/mid/PythonProjects/xpower/pyqtgraph-0.9.10')
sys.path.append('/home/mid/PythonProjects/xpower')
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph.Point import Point
from Widgets.pgCandleItem import CandlestickItem
########################################################################
class pgCandleWidgetCross(pg.GraphicsWindow):
    def __init__(self, dataForCandle=None):
        """Constructor"""
        super(pgCandleWidgetCross, self).__init__()
        self.setWindowTitle('pyqtgraph example: crosshair')     
        
        self.candleData = dataForCandle 
        self.CandlePlot = pg.PlotItem()
        #cross hair
        self.vLine = pg.InfiniteLine(angle=90, movable=False)
        self.hLine = pg.InfiniteLine(angle=0, movable=False)

        self.label = pg.LabelItem(justify='right')
        
        self.addItem(self.label,0,0)      
        self.addItem(self.CandlePlot,1,0) 
        
        self.CandlePlot.addItem(CandlestickItem(self.candleData))     
        self.CandlePlot.addItem(self.vLine, ignoreBounds=True)
        self.CandlePlot.addItem(self.hLine, ignoreBounds=True)

        self.proxy = pg.SignalProxy(self.CandlePlot.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)
    def mouseMoved(self,evt):
        pos = evt[0]  ## using signal proxy turns original arguments into a tuple
        if self.CandlePlot.sceneBoundingRect().contains(pos):
            mousePoint = self.CandlePlot.vb.mapSceneToView(pos)
            index = int(mousePoint.x())
            xLeft = self.candleData[0,0]
            xRight = self.candleData[len(self.candleData)-1,0]
            if index > xLeft and index < xRight:
                self.label.setText("<span style='font-size: 12pt'>x=%0.1f,   <span style='color: red'>y1=%0.1f</span>,   <span style='color: green'>y2=%0.1f</span>" % (mousePoint.x(), index, index))
            self.vLine.setPos(mousePoint.x())
            self.hLine.setPos(mousePoint.y())
if __name__ == '__main__':
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
    import sys
    app = QtGui.QApplication(sys.argv)
    mw = QtGui.QMainWindow()
    
    candleData = getCandleData()
        
    win = pgCandleWidgetCross(dataForCandle=candleData)
    mw.setCentralWidget(win)    
    mw.show()
    sys.exit(app.exec_())