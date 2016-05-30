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
from Widgets.pgCrossAddition import pgCrossAddition
#----------------------------------------------------------------------
########################################################################
class pgCandleWidgetCross(pgCrossAddition):
    def __init__(self, dataForCandle=None):
        super(pgCandleWidgetCross, self).__init__()
        # 0) adds candle
        self.candleItem = None
        self.candleItemList = []
        self.setCandleData(dataForCandle=dataForCandle)
        # 1)cross hair
        #self.crossHair = pgCrossAddition(self)
        #self.vLine = pg.InfiniteLine(angle=90, movable=False)
        #self.hLine = pg.InfiniteLine(angle=0, movable=False)
        #self.addItem(self.vLine, ignoreBounds=True)
        #self.addItem(self.hLine, ignoreBounds=True)
        # 2) adds textInfo
        self.textInfo = pg.TextItem("test")
        #self.textPrice = pg.TextItem('price')
        #self.textDate = pg.TextItem('date')
        self.addItem(self.textInfo, ignoreBounds=True)
        #self.addItem(self.textPrice, ignoreBounds=True)
        #self.addItem(self.textDate, ignoreBounds=True)
        self.showGrid(x=True, y=True)
        
        self.candleInfo = pg.TextItem("")        ## Make all plots clickable
        self.addItem(self.candleInfo)
        
        #self.scatterAddition(self.candleData[:,0],self.candleData[:,2])   
    def setCandleData(self,dataForCandle = None,graphMode = 'alone'):
        '''mid
        设置此方法，是为了在程序运行过程中能够动态的更新candle
        此图显示过程有两个模式
        1.alone，每个symbol的candles都是独立显示，删除老图，绘制新图
        2.overlay，每个新图都是直接绘制进入老图，产生叠加图，可方便进行图形对比
        '''

        #mid 1) 创建当前传入数据的candlestickItem
        self.candleData = dataForCandle   
        if(self.candleData == None):
            return  
        
        self.candleItem = CandlestickItem(dataForCandle)
        
        if(len(self.candleItemList) > 0 and graphMode == 'alone'):
            #mid 清空老数据
            for candleItem in self.candleItemList:
                self.removeItem(candleItem)
            del self.candleItemList[:]
            
        #mid 加入新数据
        if(self.candleItem is not None):
            self.candleItemList.append(self.candleItem)        
            
        self.addItem(self.candleItem) 
        self.candleItem.sigClicked.connect(self.mouseClicked)           
    def mouseClicked(self,plot, points):
        if(len(points)>0):
            mousePoint = points[0].topRight()
            
            center = points[0].center().x()
            top = points[0].top()
            bottom = points[0].bottom()
            
            xAxis = center
            yAxis = bottom
            
            self.candleInfo.setHtml(
                '<div style="text-align: center">\
                    <span style="color: red; font-size: 10pt;">\
                        %s\
                    </span>\
                    <br>\
                    <span style="color: red; font-size: 10pt;">\
                        %.3f\
                    </span>\
                </div>'\
            % (dt.datetime.strftime(mpd.num2date(xAxis).astimezone(pytz.timezone('utc')),'%Y-%m-%d %H:%M:%S%Z'),yAxis))             
                       
            self.candleInfo.setPos(xAxis,yAxis)         
        self.candleItem.update()       
    def mouseMoved(self,evt):
        import matplotlib.dates as mpd
        import datetime as dt        
        pos = evt[0]  ## using signal proxy turns original arguments into a tuple
        if self.sceneBoundingRect().contains(pos):
            mousePoint = self.plotItem.vb.mapSceneToView(pos)
            index = int(mousePoint.x())
            
            if(self.candleData == None):
                return            
            
            xLeft = self.candleData[0,0]
            xRight = self.candleData[len(self.candleData)-1,0]
            if index >= xLeft and index <= xRight:
                #self.textInfo.setText('[%0.1f, %0.1f]' % (mousePoint.x(), mousePoint.y()))
                #self.textInfo.setHtml('<div style="text-align: center"><span style="color: #FFF;">This is the</span><br><span style="color: #FF0; font-size: 16pt;">[%0.1f, %0.1f]</span></div>'% (mousePoint.x(), mousePoint.y()))
                
                barIndex = self.candleItem.pointIn(mousePoint)
                if(barIndex != None):
                    print(barIndex)
                    currentBar = self.candleData[barIndex,:]    
                    if(barIndex >= 0):
                        #strTime = dt.datetime.strftime(mpd.num2date(currentBar[0]).astimezone(pytz.timezone('Asia/Shanghai')),'%Y-%m-%d %H:%M:%S%Z')
                        strTime = dt.datetime.strftime(mpd.num2date(currentBar[0]).astimezone(pytz.timezone('utc')),'%Y-%m-%d %H:%M:%S%Z')
                        print(barIndex,'----',strTime)
                        open  = currentBar[1]
                        high  = currentBar[2]
                        low   = currentBar[3]
                        close = currentBar[4]
                
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
                                                % (strTime,open,high,low,close))
            #self.textPrice.setHtml(
                                #'<div style="text-align: center">\
                                    #<span style="color: red; font-size: 10pt;">\
                                      #%0.3f\
                                    #</span>\
                                #</div>'\
                                    #% (mousePoint.y()))            
            #self.textDate.setHtml(
                                #'<div style="text-align: center">\
                                    #<span style="color: red; font-size: 10pt;">\
                                      #%s\
                                    #</span>\
                                #</div>'\
                                    #% (dt.datetime.strftime(mpd.num2date(mousePoint.x()),'%Y-%m-%d %H:%M:%S')))                                           
            # 0)get environments
            #rect = self.sceneBoundingRect()
            #topLeft = self.plotItem.vb.mapSceneToView(QtCore.QPointF(rect.left()+35,rect.top())) 
            #bottomRight = self.plotItem.vb.mapSceneToView(QtCore.QPointF(rect.width(),rect.bottom()-40))
            
            xAxis = mousePoint.x()
            yAxis = mousePoint.y()            
            # 1)set postions
            #self.vLine.setPos(xAxis)
            #self.hLine.setPos(yAxis)               
            self.textInfo.setPos(xAxis,yAxis) 
            
            #self.textDate.setPos(xAxis,bottomRight.y())
            #self.textPrice.setPos(topLeft.x(),yAxis)
            #self.crossHair.mouseMoved(evt)
            super(pgCandleWidgetCross, self).mouseMoved(evt)
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    def getCandleData():
        import os,sys        
        xpower = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,os.pardir,'histdata'))
        sys.path.append(xpower)     
        import dataCenter as dataCenter     
        dataCenter = dataCenter.dataCenter()  
        
        dataSource={}
        dataSource['dataProvider'] = 'tushare'
        dataSource['storageFormat']='mongodb'
        dataSource['dataPeriod']='D'
        dataSource['symbol']='600028'
        dataSource['dateStart']='2015-03-19'
        dataSource['dateEnd']='2015-12-31'  


        dataForCandle = dataCenter.retriveCandleData(params = dataSource)    
        return dataForCandle    
    dialog = QtGui.QDialog()
    layout = QtGui.QHBoxLayout()
    layoutLeft = QtGui.QVBoxLayout()
    layout.addLayout(layoutLeft)
    dialog.setLayout(layout)        
    dialog.setWindowTitle(('ComboView'))
    # 2) creates widgets 
    editor = QtGui.QTextEdit()
    editor.setText("<span style='font-size: 15pt' style='color: red'>x = %0.1f,y = %0.1f</span>"% (2.0,2.0))
    candleData = getCandleData()
    candle = pgCandleWidgetCross(dataForCandle=candleData)  
    #candle = pgCrossAddition()
    # 3)arrange widgets
    #layout.addWidget(editor)
    layout.addWidget(candle)
    dialog.showMaximized()
    sys.exit(app.exec_())