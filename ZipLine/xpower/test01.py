# -*- coding: utf-8 -*-
import sys
sys.path.append('/home/mid/PythonProjects/xpower/pyqtgraph-0.9.10')
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph.Point import Point
from Widgets.pgCandleWidget import CandlestickItem
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

########################################################################
class pgGraphicsCandle(pg.GraphicsWindow):
    """"""

    #----------------------------------------------------------------------
    def __init__(self,p1,candleData,vLine,hLine):
        """Constructor"""
        super(pgGraphicsCandle, self).__init__()
        self.setWindowTitle('pyqtgraph example: crosshair')
        label = pg.LabelItem(justify='right')
        self.addItem(label,0,0)      
        item01 = CandlestickItem(candleData)        
        self.p1 = p1
        self.p1.addItem(item01)     
        self.p1.addItem(vLine, ignoreBounds=True)
        self.p1.addItem(hLine, ignoreBounds=True)
        self.addItem(p1,1,0)
        
        
app = QtGui.QApplication(sys.argv)

candleData = getCandleData() 
p1 = pg.PlotItem()
#cross hair
vLine = pg.InfiniteLine(angle=90, movable=False)
hLine = pg.InfiniteLine(angle=0, movable=False)
win = pgGraphicsCandle(p1,candleData,vLine,hLine)




vb = p1.vb

def mouseMoved(evt):
    pos = evt[0]  ## using signal proxy turns original arguments into a tuple
    if p1.sceneBoundingRect().contains(pos):
        mousePoint = vb.mapSceneToView(pos)
        index = int(mousePoint.x())
        xLeft = candleData[0,0]
        xRight = candleData[len(candleData)-1,0]
        if index > xLeft and index < xRight:
            #label.setText("<span style='font-size: 12pt'>x=%0.1f,   <span style='color: red'>y1=%0.1f</span>,   <span style='color: green'>y2=%0.1f</span>" % (mousePoint.x(), index, index))
            #label.setText('asdklfa;sdkfl')
            pass
        vLine.setPos(mousePoint.x())
        hLine.setPos(mousePoint.y())



proxy = pg.SignalProxy(p1.scene().sigMouseMoved, rateLimit=60, slot=mouseMoved)
#p1.scene().sigMouseMoved.connect(mouseMoved)


## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys

    
    mw = QtGui.QMainWindow()

    mw.setCentralWidget(win)    
    mw.show()

    sys.exit(app.exec_())