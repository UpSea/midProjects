import sys
sys.path.append('/home/mid/PythonProjects/xpower/pyqtgraph-0.9.10')
sys.path.append('/home/mid/PythonProjects/xpower')
from PyQt4 import QtCore, QtGui
import pyqtgraph as pg
import numpy as np
import matplotlib.dates as mpd
import datetime as dt
import pytz


from Widgets.pgCandleItem import CandlestickItem

#----------------------------------------------------------------------
########################################################################
class pgCrossAddition(pg.PlotWidget):
    """
    此类给pg.PlotWidget()添加crossHair功能
    所有从此类继承的子类都将获得此crossHair功能
    """
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        super(pgCrossAddition, self).__init__()
        self.vLine = pg.InfiniteLine(angle=90, movable=False)
        self.hLine = pg.InfiniteLine(angle=0, movable=False)
        self.textPrice = pg.TextItem('price')
        self.textDate = pg.TextItem('date')
        
        self.addItem(self.textDate, ignoreBounds=True)
        self.addItem(self.textPrice, ignoreBounds=True)        
        self.addItem(self.vLine, ignoreBounds=True)
        self.addItem(self.hLine, ignoreBounds=True)    
        self.proxy = pg.SignalProxy(self.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)        
    def mouseMoved(self,evt):
        import matplotlib.dates as mpd
        import datetime as dt          
        pos = evt[0]  ## using signal proxy turns original arguments into a tuple
        if self.sceneBoundingRect().contains(pos):
            mousePoint = self.plotItem.vb.mapSceneToView(pos)        
            xAxis = mousePoint.x()
            yAxis = mousePoint.y()            
            # 1)set postions
            self.vLine.setPos(xAxis)
            self.hLine.setPos(yAxis)      
    
            self.textPrice.setHtml(
                                '<div style="text-align: center">\
                                    <span style="color: red; font-size: 10pt;">\
                                      %0.3f\
                                    </span>\
                                </div>'\
                                    % (mousePoint.y()))            
            self.textDate.setHtml(
                                '<div style="text-align: center">\
                                    <span style="color: red; font-size: 10pt;">\
                                      %s\
                                    </span>\
                                </div>'\
                                    % (dt.datetime.strftime(mpd.num2date(mousePoint.x()).astimezone(pytz.timezone('utc')),'%Y-%m-%d %H:%M:%S%Z')))                                           
            # 0)get environments
            rect = self.sceneBoundingRect()
            topLeft = self.plotItem.vb.mapSceneToView(QtCore.QPointF(rect.left()+35,rect.top())) 
            bottomRight = self.plotItem.vb.mapSceneToView(QtCore.QPointF(rect.width(),rect.bottom()-40))
    
            self.textDate.setPos(xAxis,bottomRight.y())
            self.textPrice.setPos(topLeft.x(),yAxis)    
    #----------------------------------------------------------------------
    def scatterAddition(self,x,y):
        """
        此处将clicked定义为内部函数，是为了将传入参数pgPlot与其绑定
        每个通过scatterAddition加入scatter的pgPlot都会保存一份自己的clicked函数
        而clicked处理的是传入的参数pgPlot
        """
        scatterPrice = pg.ScatterPlotItem(size=10, pen=pg.mkPen(None), pxMode=True, brush=pg.mkBrush(255, 255, 255, 120))            
        spots = [{'pos': (x,price)} for x,price in zip(x,y)]
        scatterPrice.addPoints(spots)
        self.addItem(scatterPrice)
        
        self.scatterInfo = pg.TextItem("test")        ## Make all plots clickable
        self.addItem(self.scatterInfo)
 
        self.lastClicked = []
        def clicked(plot, points):
            if(len(points)>0):
                mousePoint = points[0].pos()
                self.scatterInfo.setHtml(
                    '<div style="text-align: center">\
                        <span style="color: red; font-size: 10pt;">\
                            %s\
                        </span>\
                        <br>\
                        <span style="color: red; font-size: 10pt;">\
                            %.3f\
                        </span>\
                    </div>'\
                % (dt.datetime.strftime(mpd.num2date(mousePoint.x()).astimezone(pytz.timezone('utc')),'%Y-%m-%d %H:%M:%S%Z'),
                   mousePoint.y()
                ))             
                xAxis = mousePoint.x()
                yAxis = mousePoint.y()                          
                self.scatterInfo.setPos(xAxis,yAxis) 
            for p in self.lastClicked:
                p.resetPen()
            for p in points:
                p.setPen('b', width=2)
            self.lastClicked = points    
        scatterPrice.sigClicked.connect(clicked)          