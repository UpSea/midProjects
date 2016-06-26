# -*- coding: utf-8 -*-
import sys,os
xpower = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,os.pardir,'thirdParty','pyqtgraph-0.9.10'))
sys.path.append(xpower)
xpower = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir))
sys.path.append(xpower)
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
            #mid 1)set contents to price and date lable
            self.vLine.setPos(xAxis)
            self.hLine.setPos(yAxis)      
    
            self.textPrice.setHtml(
                                '<div style="text-align: center">\
                                    <span style="color: red; font-size: 10pt;">\
                                      %0.3f\
                                    </span>\
                                </div>'\
                                    % (mousePoint.y()))   
            strTime = mpd.num2date(mousePoint.x()).astimezone(pytz.timezone('utc'))
            if(strTime.year >=1900):
                self.textDate.setHtml(
                                    '<div style="text-align: center">\
                                        <span style="color: red; font-size: 10pt;">\
                                          %s\
                                        </span>\
                                    </div>'\
                                        % (dt.datetime.strftime(strTime,'%Y-%m-%d %H:%M:%S%Z')))                                           
            #mid 2)get position environments
            #mid 2.1)client area rect
            rect = self.sceneBoundingRect()
            leftAxis = self.getAxis('left')
            bottomAxis = self.getAxis('bottom')            
            rectTextDate = self.textDate.boundingRect()         
            #mid 2.2)leftAxis width,bottomAxis height and textDate height.
            leftAxisWidth = leftAxis.width()
            bottomAxisHeight = bottomAxis.height()
            rectTextDateHeight = rectTextDate.height()
            print leftAxisWidth,bottomAxisHeight
            #mid 3)set positions of price and date lable
            topLeft = self.plotItem.vb.mapSceneToView(QtCore.QPointF(rect.left()+leftAxisWidth,rect.top()))
            bottomRight = self.plotItem.vb.mapSceneToView(QtCore.QPointF(rect.width(),rect.bottom()-(bottomAxisHeight+rectTextDateHeight)))
            self.textDate.setPos(xAxis,bottomRight.y())
            self.textPrice.setPos(topLeft.x(),yAxis)    
    #----------------------------------------------------------------------
    def scatterAddition(self,x,y):
        """
        此处将clicked定义为内部函数，是为了将传入参数pgPlot与其绑定
        每个通过scatterAddition加入scatter的pgPlot都会保存一份自己的clicked函数
        而clicked处理的是传入的参数pgPlot
        """
        scatterPrice = pg.ScatterPlotItem(size=5, pen=pg.mkPen(None), pxMode=True, brush=pg.mkBrush(255, 255, 255, 120))            
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
        
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    import os,sys
    dataRoot = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,os.pardir,'histdata'))        
    sys.path.append(dataRoot)        
    import dataCenter as dataCenter   
     
    #mid 1) creates windows
    dialog = QtGui.QDialog()
    layout = QtGui.QHBoxLayout()
    dialog.setLayout(layout)        
    dialog.setWindowTitle(('ComboView'))
    #mid 2) creates widgets 
    candle = pgCrossAddition()
    #mid 3) creates Item and adds Item to widgets
    candleData = dataCenter.getCandleData()  
    candleItem = CandlestickItem(candleData)
    candle.addItem(candleItem)     
    #mid 4) arrange widgets
    layout.addWidget(candle)
    dialog.showMaximized()
    sys.exit(app.exec_())