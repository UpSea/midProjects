# -*- coding: utf-8 -*-
import sys
sys.path.append('/home/mid/PythonProjects/xpower/pyqtgraph-0.9.10')
from PyQt4 import QtCore, QtGui
import pyqtgraph as pg
import numpy as np

class CandlestickItem(pg.GraphicsObject):
    sigClicked = QtCore.Signal(object, object)  ## self, points
    def pointsAt(self, pos):
        '''
        mid 返回鼠标点击位置选中的所有Rect的列表
        '''
        x = pos.x()
        y = pos.y()
        pts = []
        for s in self.dataRects:
            if(s.contains(pos)):
                pts.append(s)
                #print "HIT:", x, y, sx, sy, s2x, s2y
            #else:
                #print "No hit:", (x, y), (sx, sy)
                #print "       ", (sx-s2x, sy-s2y), (sx+s2x, sy+s2y)
        #pts.sort(lambda a,b: cmp(b.zValue(), a.zValue()))
        return pts[::-1]          
    def mouseClickEvent(self, ev):
        if ev.button() == QtCore.Qt.LeftButton:
            pts = self.pointsAt(ev.pos())
            if len(pts) > 0:
                self.ptsClicked = pts
                self.lastClicked = pts
                self.generatePicture()
                #self.update()
                self.sigClicked.emit(self, self.ptsClicked)
                ev.accept()
            else:
                #print "no spots"
                ev.ignore()
        else:
            ev.ignore()
    
    def __init__(self, data):
        pg.GraphicsObject.__init__(self)
        self.data = data  ## data must have fields: time, open, close, min, max
        
        #self.data = np.empty(0, dtype=[('x', float), ('y', float), ('size', float), ('symbol', object), ('pen', object), ('brush', object), ('data', object), ('item', object), ('sourceRect', object), ('targetRect', object), ('width', float)])
        self.lastClicked = []
        self.ptsClicked = []    #
        self.dataRects = np.empty(len(data), dtype=QtCore.QRectF)
        self.generatePicture()
    def generatePicture(self):
        ## pre-computing a QPicture object allows paint() to run much more quickly, 
        ## rather than re-drawing the shapes every time.
        self.picture = QtGui.QPicture()
        p = QtGui.QPainter(self.picture)
        p.setPen(pg.mkPen('w'))
        barWidth = (self.data[1][0] - self.data[0][0]) / 3.
        
        for index,item in enumerate(self.data):
            time = item[0]
            open = item[1]
            high = item[2]
            low = item[3]
            close = item[4]
            
            if(True):
                x = time
            else:
                x = index
            # 01.draw high-low line,when high == low,it means the symbol is not traded.
            if(high != low):
                p.drawLine(QtCore.QPointF(x, low), QtCore.QPointF(x, high))
            
            # 02.decide the color of candle
            if open > close:
                p.setBrush(pg.mkBrush('g'))
            else:
                p.setBrush(pg.mkBrush('r'))
                
           
            # 03.draw the candle rect
            x=x-barWidth
            y=open
            width= barWidth*2
            height=close-open
            rectToDraw = QtCore.QRectF(x,y ,width,height)
            
            for rect in self.ptsClicked:
                if(rect == rectToDraw):
                    p.setPen(pg.mkPen('w'))
                    p.setBrush(pg.mkBrush('w'))                
            p.drawRect(rectToDraw)
            self.dataRects[index]=QtCore.QRectF(x,y ,width,height)
        p.end()
    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)
    def boundingRect(self):
        ## boundingRect _must_ indicate the entire area that will be drawn on
        ## or else we will get artifacts and possibly crashing.
        ## (in this case, QPicture does all the work of computing the bouning rect for us)
        return QtCore.QRectF(self.picture.boundingRect())         
class pgCandleWidget(pg.PlotWidget):
    def __init__(self, dataForCandle=None):
        super(pgCandleWidget, self).__init__()
        # 0) adds candle
        self.candleData = dataForCandle 
        self.item01 = CandlestickItem(dataForCandle)        
        self.addItem(self.item01) 
        # 1)cross hair
        self.vLine = pg.InfiniteLine(angle=90, movable=False)
        self.hLine = pg.InfiniteLine(angle=0, movable=False)
        self.addItem(self.vLine, ignoreBounds=True)
        self.addItem(self.hLine, ignoreBounds=True)
        # 2) adds textInfo
        self.textInfo = pg.TextItem("test")
        self.addItem(self.textInfo, ignoreBounds=True)        
        self.item01.sigClicked.connect(self.mouseClicked)         
        
        self.proxy = pg.SignalProxy(self.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)
    def mouseClicked(self,plot, points):
        self.item01.update()    
    def mouseMoved(self,evt):
        pos = evt[0]  ## using signal proxy turns original arguments into a tuple
        if self.sceneBoundingRect().contains(pos):
            mousePoint = self.plotItem.vb.mapSceneToView(pos)
            index = int(mousePoint.x())
            xLeft = self.candleData[0,0]
            xRight = self.candleData[len(self.candleData)-1,0]
            if index > xLeft and index < xRight:
                #self.textInfo.setText('[%0.1f, %0.1f]' % (mousePoint.x(), mousePoint.y()))
                #self.textInfo.setHtml('<div style="text-align: center"><span style="color: #FFF;">This is the</span><br><span style="color: #FF0; font-size: 16pt;">[%0.1f, %0.1f]</span></div>'% (mousePoint.x(), mousePoint.y()))
                
                a = np.where(self.candleData[:,0]==index)
                if(len(a[0])>0):
                    import matplotlib.dates as mpd
                    import datetime as dt
                
                    date = mpd.num2date(self.candleData[3,0])
                    strDate = dt.datetime.strftime(date, '%Y-%m-%d')                    
                    self.textInfo.setHtml(
                    '<div style="text-align: center">\
                        <span style="color: #FFF;">\
                           Current bar info:\
                        </span>\
                          <br>\
                        <span style="color: #FF0; font-size: 10pt;">\
                          time:%s\
                          <br>\
                          open:%0.3f\
                          <br>\
                          high:%0.3f\
                          <br>\
                          low:%0.3f\
                          <br>\
                          close:%0.3f\
                        </span>\
                    </div>'\
                        % (dt.datetime.strftime(mpd.num2date(self.candleData[a[0][0],0]),'%Y-%m-%d'), 
                           self.candleData[a[0][0],1],
                           self.candleData[a[0][0],2],
                           self.candleData[a[0][0],3],
                           self.candleData[a[0][0],4]))

            
            
            #date = np.array([mpd.date2num(dt.datetime.strptime(dateStr, '%Y-%m-%d')) )                     
                    
            # 0)get environments
            rect = self.sceneBoundingRect()
            top = rect.top()
            left = rect.left()
            bottom = rect.bottom()
            width = rect.width()
            
            xAxis = mousePoint.x()
            yAxis = mousePoint.y()            
            # 1)set postions
            self.vLine.setPos(xAxis)
            self.hLine.setPos(yAxis)               
            self.textInfo.setPos(xAxis,yAxis)            
            

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
    

    
    dialog = QtGui.QDialog()
    layout = QtGui.QHBoxLayout()
    layoutLeft = QtGui.QVBoxLayout()
    layout.addLayout(layoutLeft)
    dialog.setLayout(layout)        
    dialog.setWindowTitle(('ComboView'))
    
    # 2) creates widgets 
    editor = QtGui.QTextEdit()
    candleData = getCandleData()
    candle = pgCandleWidget(dataForCandle=candleData)    
    # 3)arrange widgets
    #layout.addWidget(editor)
    #editor.setText("<span style='font-size: 15pt' style='color: red'>x = %0.1f,y = %0.1f</span>"% (2.0,2.0))
    
    layout.addWidget(candle)
    dialog.show()
    
    sys.exit(app.exec_())