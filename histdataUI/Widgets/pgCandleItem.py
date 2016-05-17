# -*- coding: utf-8 -*-
import sys,os
xpower = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,os.pardir,os.pardir,'thirdParty','pyqtgraph-0.9.10'))
sys.path.append(xpower)

from PyQt4 import QtCore, QtGui
import pyqtgraph as pg
import numpy as np
class CandlestickItem(pg.GraphicsObject):
    sigClicked = QtCore.Signal(object, object)  ## self, points
    #----------------------------------------------------------------------
    def pointIn(self,pos):
        """
        返回鼠标位置所在的candle的序号
        """
        x = pos.x()
        y = pos.y()
        index = None
        for index,rect in zip(np.arange(0,len(self.dataRects)),self.dataRects):
            if(rect.contains(pos)):
                return index 
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
            if len(pts) > 0:    # mid 如果当前鼠标单击的范围在candles中，则重新绘制picture，并调用update重绘
                self.ptsClicked = pts
                self.generatePicture()
                
                #mid 此处特意注销update(),将其安排在信号响应函数中，仅是为了演示信号处理流程
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
        
        self.lastClicked = []
        self.ptsClicked = []
        self.bSelected = False
        self.dataRects = np.empty(len(data), dtype=QtCore.QRectF)        
        
        self.generatePicture()
    def generatePicture(self):
        ## pre-computing a QPicture object allows paint() to run much more quickly, 
        ## rather than re-drawing the shapes every time.
        self.picture = QtGui.QPicture()
        p = QtGui.QPainter(self.picture)
        p.setPen(pg.mkPen('w'))
        halfBarWidth = (self.data[1][0] - self.data[0][0]) / 3.
        
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
            x=x-halfBarWidth
            y=open
            barWidth= halfBarWidth*2
            height=close-open
            rectToDraw = QtCore.QRectF(x,y ,barWidth,height)
            
            if(not self.bSelected):
                for lastRect in self.lastClicked:
                    for newRect in self.ptsClicked:
                        if(lastRect == newRect):
                            self.bSelected = True
            
            
            
            if(not self.bSelected):
                for rect in self.ptsClicked:
                    if(rect == rectToDraw):
                        self.lastClicked = self.ptsClicked 
                        p.setPen(pg.mkPen('w'))
                        p.setBrush(pg.mkBrush('w')) 
            else:
                self.bSelected = False
                
            p.drawRect(QtCore.QRectF(x,y ,barWidth,height))
            self.dataRects[index]=QtCore.QRectF(x,y ,barWidth,height)
        p.end()
    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)
    def boundingRect(self):
        ## boundingRect _must_ indicate the entire area that will be drawn on
        ## or else we will get artifacts and possibly crashing.
        ## (in this case, QPicture does all the work of computing the bouning rect for us)
        return QtCore.QRectF(self.picture.boundingRect())         