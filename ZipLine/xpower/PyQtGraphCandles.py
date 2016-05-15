# -*- coding: utf-8 -*-
"""
Demonstrate creation of a custom graphic (a candlestick plot)
"""
import sys
sys.path.append('/home/mid/PythonProjects/xpower/pyqtgraph-0.9.10')

import pyqtgraph as pg
from pyqtgraph import QtCore, QtGui

## Create a subclass of GraphicsObject.
## The only required methods are paint() and boundingRect() 
## (see QGraphicsItem documentation)
class CandlestickItem(pg.GraphicsObject):
    def __init__(self, data):
        pg.GraphicsObject.__init__(self)
        self.data = data  ## data must have fields: time, open, close, min, max
        self.generatePicture()
    
    def generatePicture(self):
        ## pre-computing a QPicture object allows paint() to run much more quickly, 
        ## rather than re-drawing the shapes every time.
        self.picture = QtGui.QPicture()
        p = QtGui.QPainter(self.picture)
        p.setPen(pg.mkPen('w'))
        barWidth = (self.data[1][0] - self.data[0][0]) / 3.
        for (time, open, high, low, close) in self.data:
            p.drawLine(QtCore.QPointF(time, low), QtCore.QPointF(time, high))
            if open > high:
                p.setBrush(pg.mkBrush('r'))
            else:
                p.setBrush(pg.mkBrush('g'))
            p.drawRect(QtCore.QRectF(time-barWidth, open, barWidth*2, high-open))
        p.end()
    
    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)
    
    def boundingRect(self):
        ## boundingRect _must_ indicate the entire area that will be drawn on
        ## or else we will get artifacts and possibly crashing.
        ## (in this case, QPicture does all the work of computing the bouning rect for us)
        return QtCore.QRectF(self.picture.boundingRect())
import pandas as pd
import matplotlib.dates as mpd
dates = pd.date_range(start='20100101',periods=10)

data = [  ## fields are (time, open, close, min, max).
    (mpd.date2num(dates[0]), 10, 13, 5, 15),
    (mpd.date2num(dates[1]), 13, 17, 9, 20),
    (mpd.date2num(dates[2]), 17, 14, 11, 23),
    (mpd.date2num(dates[3]), 14, 15, 5, 19),
    (mpd.date2num(dates[4]), 15, 9, 8, 22),
    (mpd.date2num(dates[5]), 9, 15, 8, 16),
]
from DataSources.GetDataFromMongodb import GetDataFromMongodb
# %% 01类定义
#----------------------------------------------------------------------
dataSource={}
dataSource['ip']='192.168.1.100'
dataSource['port']=27017
dataSource['database']='Tushare'
dataSource['symbol']='000001'
dataSource['dateStart']='2015-12-19'
dataSource['dateEnd']='2015-12-31'
dataSource['frequency']='D'
dataForZipline,dataForCandle = GetDataFromMongodb(dataSource)

item01 = CandlestickItem(dataForCandle)
item02 = CandlestickItem(data[0:2])

plt = pg.plot()
#plt.addItem(item02)
plt.addItem(item01)
plt.setWindowTitle('pyqtgraph example: customGraphicsItem')

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
