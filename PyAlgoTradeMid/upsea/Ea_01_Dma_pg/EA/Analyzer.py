# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib.dates as mpd
import matplotlib.finance as mpf
import numpy as np
import datetime as dt

import sys,os
xpower = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,os.pardir,os.pardir,os.pardir,'thirdParty','pyqtgraph-0.9.10'))
sys.path.append(xpower)
import pyqtgraph as pg

from PyQt4 import QtGui,QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

class Analyzer():
    """"""
    #----------------------------------------------------------------------
    def __init__(self,Globals=None):
        """
        在XPower中执行时，此类的对象是临时的。
        若作为显示窗体的对象调用时，对象内存在show后需要不被释放
        所以，设置此父对象参数，使本对象和父对象一样长寿。
        在展示某个窗口时，为了使某个弹出窗口可以多次并存弹出，被弹出窗口也需要重复定义并全局化
        """
        self.Globals = Globals
        self.Globals.append(self)
    def addText(self,ax,xAxis,yAxis):        #mid add some y value to ax.
        for x,y in zip(xAxis,yAxis):
            text = '('+str(round(y,3))+')'
            ax.annotate(text,xy=(x,y))   
    #----------------------------------------------------------------------
    def portfolioPlot(self,ax,bDrawText=False):
        """"""
        date = np.array([mpd.date2num(date) for date in self.results.index])  
        if 'portfolio_value' in self.results:
            ax.plot(date,self.results.portfolio_value,pen=(255,255,255))
            ax.scatterAddition(date, self.results.portfolio_value) 
    #----------------------------------------------------------------------
    def orderPlot(self,ax):
        """"""
        def getOrdersAmount(order):    
            if(len(order)>0):
                for item in order:
                    return item['amount']                
            else:
                return 0
        def getOrderDatetime(order):    
            if(len(order)>0):
                for item in order:
                    return item['created']                
            else:
                return 0
        
        if 'orders' in self.results:
            orders  = self.results['orders']
            orders  = orders.iloc[np.where(orders)] # mid some order==[],should be removed.
            ordersAmount = list(map(getOrdersAmount, orders))
            ordersCreated = list(map(getOrderDatetime, orders))
        
            date = np.array([mpd.date2num(date) for date in ordersCreated]) 
        
            ax.plot(date, ordersAmount,pen=(255,0,0), name="Orders amount curve")
            ax.scatterAddition(date, ordersAmount)   
    def positionCostPlot(self,ax,bDrawText=False):  
        if 'position_cost' in self.results:
            position_cost = self.results.position_cost
            date = np.array([mpd.date2num(date) for date in self.results.index]) 
        
            indexOfZero = position_cost[:] == 0
            count = len(position_cost[indexOfZero])
            
            #date[0:count] = position_cost[count]
            
            dateOfNoneZero = date[count:]
            position_costOfNoneZero = position_cost[count:]
            
            ax.plot(dateOfNoneZero,position_costOfNoneZero ,pen=(255,255,255), name="Position curve")
            ax.scatterAddition(dateOfNoneZero, position_costOfNoneZero)   
            
    def positionVolumePlot(self,ax,bDrawText=False):  
        if 'position_volume' in self.results:
            position_volume = self.results.position_volume
            date = np.array([mpd.date2num(date) for date in self.results.index]) 
        
            ax.plot(date, position_volume,pen=(255,255,255), name="Position curve")
            ax.scatterAddition(date, position_volume)  
            
    def positionPnlPlot(self,ax,bDrawText=False):
        date = np.array([mpd.date2num(date) for date in self.results.index])
        if 'position_pnl' in self.results:
            position_pnl = np.array(self.results.position_pnl)
            ax.plot(date,position_pnl , pen=(255,255,255), name="Red curve")
            ax.scatterAddition(date, position_pnl)    
    def signalPlot(self,ax):
        date = np.array([mpd.date2num(date) for date in self.results.index]) 
        if 'buy' in self.results and 'sell' in self.results:     
            xBuy = np.array([mpd.date2num(date) for date in self.results.ix[self.results.buy].index])         
            yBuy = np.array(self.results.short_ema[self.results.buy])            
            for x1,y1 in zip(xBuy,yBuy):
                a1 = pg.ArrowItem(angle=90, tipAngle=60, headLen=5, tailLen=0, tailWidth=5, pen={'color': 'r', 'width': 1})
                ax.addItem(a1)
                a1.setPos(x1,y1)        
                
            xSell = np.array([mpd.date2num(date) for date in self.results.ix[self.results.sell].index])         
            ySell = np.array(self.results.short_ema[self.results.sell])            
            for x1,y1 in zip(xSell,ySell):
                a1 = pg.ArrowItem(angle=-90, tipAngle=60, headLen=5, tailLen=0, tailWidth=5, pen={'color': 'g', 'width': 1})
                ax.addItem(a1)
                a1.setPos(x1,y1)          
    #----------------------------------------------------------------------
    def indicatorsPlot(self,ax):
        """"""
        date = np.array([mpd.date2num(date) for date in self.results.index]) 
        if 'short_ema' in self.results and 'long_ema' in self.results:
            ax.plot(date,self.results.short_ema)
            ax.plot(date,self.results['long_ema'])          
    #----------------------------------------------------------------------
    def pricePlot(self,ax,bDrawText=False):
        """"""
        date = np.array([mpd.date2num(date) for date in self.results.index]) 
        if 'AAPL' in self.results:
            ax.plot(date,self.results.AAPL)
            ax.scatterAddition(date, self.results.AAPL)

   
    def showPAT(self,results = None,KData = None):
        dialog = self.initDialog(results=results, KData=KData)
        self.Globals.append(dialog)
        dialog.showMaximized()         
    def analyze(self,results=None,KData=None,bDrawText=False):
        # Plot the portfolio and asset data.
        self.results = results
        self.KData = KData  
        drawer = 'pat'
        if(drawer == 'pat'):
            self.showPAT(results=results, KData=KData)
        else:
            self.showDialog(results=results, KData=KData, bDrawText=bDrawText)
    #----------------------------------------------------------------------
    def showDialog(self,results=None,KData=None,bDrawText=False):
        """"""
        startDialog = self.StartDialog()
        self.Globals.append(startDialog)
        startDialog.show()        
    #----------------------------------------------------------------------
    def showMainWindow(self,results=None,KData=None,bDrawText=False):
        """"""
        mw = QtGui.QMainWindow()
        print("before append:",len(self.Globals))      
        self.Globals.append(mw)     # mid 必须使窗体变量的生命与mainframe相同，否则，会闪退
        
        leftDock = self.initLeftDock(mw)
        dialog  = self.initDialog(results=results,KData=KData)
        
        mw.addDockWidget(QtCore.Qt.LeftDockWidgetArea,leftDock)  
        mw.setCentralWidget(dialog) 
        mw.showMaximized()        
    def slotShowPriceTable(self):
        KData = self.KData
        colTime = 0
        colOpen = 1
        colHigh = 2
        colLow = 3
        colClose = 4
        
        self.TablePrice = QtGui.QTableWidget()
        self.TablePrice.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)  
        self.TablePrice.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)  
        self.TablePrice.setSelectionBehavior(QtGui.QTableWidget.SelectRows)  
        self.TablePrice.setSelectionMode(QtGui.QTableWidget.SingleSelection)  
        self.TablePrice.setAlternatingRowColors(True)         
        self.TablePrice.clear()
        
        header = ['datetime','open','high','low','close']
        self.TablePrice.setColumnCount(len(header))
        self.TablePrice.setRowCount(len(KData))
        self.TablePrice.setHorizontalHeaderLabels(header)     #mid should be after .setColumnCount()
        self.TablePrice.setWindowTitle("history")
        #self.TableHistories.showMaximized()
        self.TablePrice.show()          

        for index,date,price in zip(np.arange(len(self.results.index)),self.results.index,self.results.AAPL):
            datetime = dt.datetime.strftime(date,'%Y-%m-%d %H:%M:%S')
            price = str(price)
            
            self.TablePrice.setItem(index,0,QtGui.QTableWidgetItem(datetime))
            self.TablePrice.setItem(index,1,QtGui.QTableWidgetItem(price))            
    def slotShowHistoryTable(self):
        KData = self.KData
        colTime = 0
        colOpen = 1
        colHigh = 2
        colLow = 3
        colClose = 4
        
        self.TableHistories = QtGui.QTableWidget()
        self.TableHistories.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)  
        self.TableHistories.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)  
        self.TableHistories.setSelectionBehavior(QtGui.QTableWidget.SelectRows)  
        self.TableHistories.setSelectionMode(QtGui.QTableWidget.SingleSelection)  
        self.TableHistories.setAlternatingRowColors(True)         
        
        
        self.TableHistories.clear()
        header = ['datetime','open','high','low','close']
        self.TableHistories.setColumnCount(len(header))
        self.TableHistories.setRowCount(len(KData))
        self.TableHistories.setHorizontalHeaderLabels(header)     #mid should be after .setColumnCount()
        self.TableHistories.setWindowTitle("history")
        #self.TableHistories.showMaximized()
        self.TableHistories.show()          

        for row in np.arange(0,len(KData)):
            datetime = dt.datetime.strftime(mpd.num2date(KData[row,colTime]),'%Y-%m-%d %H:%M:%S')
            openPrice = str(KData[row,colOpen])
            highPrice = str(KData[row,colHigh])
            lowPrice = str(KData[row,colLow])
            closePrice = str(KData[row,colClose])
            
            self.TableHistories.setItem(row,0,QtGui.QTableWidgetItem(datetime))
            self.TableHistories.setCellWidget(row,1,QtGui.QLabel(str(openPrice)))
            self.TableHistories.setItem(row,2,QtGui.QTableWidgetItem(highPrice))
            self.TableHistories.setItem(row,3,QtGui.QTableWidgetItem(lowPrice))
            self.TableHistories.setItem(row,4,QtGui.QTableWidgetItem(closePrice))
    #----------------------------------------------------------------------
    def slotShowComboView(self):
        """"""
        dialog  = self.initDialog(results=self.results,KData=self.KData)
        self.Globals.append(dialog)
        dialog.show()         
    #----------------------------------------------------------------------
    def slotShowCandleView(self):
        """"""
        # 1) creates layouts
        dialog = QtGui.QDialog()   
        mainLayout = QtGui.QHBoxLayout()
        rightLayout = QtGui.QVBoxLayout()
        mainLayout.addLayout(rightLayout)
        dialog.setLayout(mainLayout)        
        dialog.setWindowTitle(('Strategy Results'))
        # 2) creates widgets 
        #  2.1)candle
        from Widgets.pgCandleWidgetCross import pgCandleWidgetCross
        from Widgets.pgCrossAddition import pgCrossAddition
        pgCandleView = pgCandleWidgetCross(dataForCandle=self.KData)        
        self.pricePlot(pgCandleView) 

        rightLayout.addWidget(pgCandleView)
 
        self.Globals.append(dialog)
        dialog.show()    
    #----------------------------------------------------------------------
    def StartDialog(self):
        """"""
        dialog = QtGui.QDialog()
        # 2) arranges dialog
        mainLayout = QtGui.QHBoxLayout()
        leftLayout = QtGui.QVBoxLayout()
        mainLayout.addLayout(leftLayout)
        dialog.setLayout(mainLayout)         
    
        EditStrategy = QtGui.QTextEdit()
        self.TableOrders = QtGui.QTableWidget()
        
        buttonShowHistoryTable = QtGui.QPushButton(('HistoryTable'))
        buttonShowPriceTable = QtGui.QPushButton(('PriceTable'))
        buttonShowComboView = QtGui.QPushButton(('ComboView'))
        buttonShowCandleView = QtGui.QPushButton(('CandleView'))
    
        dialog.connect(buttonShowHistoryTable,QtCore.SIGNAL("clicked()"),self.slotShowHistoryTable)
        dialog.connect(buttonShowPriceTable,QtCore.SIGNAL("clicked()"),self.slotShowPriceTable)
        dialog.connect(buttonShowComboView,QtCore.SIGNAL("clicked()"),self.slotShowComboView)
        dialog.connect(buttonShowCandleView,QtCore.SIGNAL("clicked()"),self.slotShowCandleView)

        leftLayout.addWidget(buttonShowHistoryTable)
        leftLayout.addWidget(buttonShowPriceTable)
        leftLayout.addWidget(buttonShowComboView)
        leftLayout.addWidget(buttonShowCandleView)

        leftLayout.addWidget(self.TableOrders)
        leftLayout.addWidget(EditStrategy) 
    
        EditStrategy.setText('the text info outputs of the current strategy.')
        self.initTableOrders()
        
        return dialog
    def initLeftDock(self,mw):
        '''
        mid QDockWidget下作排版时，不能直接设置Layout+排版Layout
        而是需要先setWidget,之后，对added widget加入layout做排版
        '''
        # 1) creates dialog
        dock=QtGui.QDockWidget("ResultsView",mw)
        dialog = self.StartDialog()
        dock.setWidget(dialog)        
        # 3)sets dock
        dock.setFeatures(QtGui.QDockWidget.DockWidgetMovable)
        dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)        
        dock.setMaximumWidth(1000)
        dock.setMinimumWidth(500)    
        return dock    
    def initTableOrders(self):
        """"""
        self.TableOrders.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)  
        self.TableOrders.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)  
        self.TableOrders.setSelectionBehavior(QtGui.QTableWidget.SelectRows)  
        self.TableOrders.setSelectionMode(QtGui.QTableWidget.SingleSelection)  
        self.TableOrders.setAlternatingRowColors(True)         

        self.TableOrders.clear()
        header = ["symbol","timeCreated","limitReached","lot","commission"]
        self.TableOrders.setColumnCount(len(header))
        
        orders  = self.results['orders']
        orders  = orders.iloc[np.where(orders)]
        self.TableOrders.setRowCount(len(orders))
        self.TableOrders.setHorizontalHeaderLabels(header)     #mid should be after .setColumnCount()
       
        import datetime as dt       
        timeStr = dt.datetime.strftime
        for index,date,price in zip(np.arange(len(self.results.index)),self.results.index,self.results.AAPL):
            datetime = timeStr(date,'%Y-%m-%d %H:%M:%S')        
            print('initTableOrders().date----datetime:',date,'----',datetime)
        print('----------')
        for row,order in zip(np.arange(len(orders)),orders):
            created = order[0]['created']
            
            strCreated = timeStr(created,'%Y-%m-%d %H:%M:%S')
            print('time.order created',created,'----',strCreated)       
            
            limit_reached = order[0]['limit_reached']
            stop = order[0]['stop']
            status = order[0]['status']
            reason = order[0]['reason']
            dt = order[0]['dt']
            amount = order[0]['amount']
            limit = order[0]['limit']
            stop_reached = order[0]['stop_reached']
            commission = order[0]['commission']
            
            sid = order[0]['sid']
            symbol = sid.symbol
            
            self.TableOrders.setItem(row,0,QtGui.QTableWidgetItem(symbol))
            self.TableOrders.setItem(row,1,QtGui.QTableWidgetItem(strCreated))
            self.TableOrders.setItem(row,2,QtGui.QTableWidgetItem(str(limit_reached)))
            self.TableOrders.setItem(row,3,QtGui.QTableWidgetItem(str(amount)))
            self.TableOrders.setItem(row,4,QtGui.QTableWidgetItem(str(commission)))
    def initDialog(self,results=None,KData=None,bDrawText=False):
        '''
        orders，记录当日00:00前一日开盘时间发送的交易命令
        trasactions，记录当日00:00前一日已执行的orders
        positions，记录当日00:00时，各个symbols的positions
        所以，这三个量都是数组，且大小不定，所以，不宜图形方式展示，适宜table方式展示
        其他单值参数都可以考虑图形化方式
        特别是pnl，cash，portfolio等
        perf的生成时点是00:00，其内容为00:00前一天的活动
        perf转化记录入result时，需要设置Index，
        此Index的值为生成记录时点后的一天的收盘时间。
        
        例如:
        有三个交易日:2015-12-01，12-02，12-03
        开收盘时间:Asia/Shanghai:09:30--15:00 (utc:01:30--07:00)
        使用instant_fill==True方式执行订单
        每日开盘时Buy(1)
        
        有如下Events列表会生成并被处理
        1)2015-12-01 00:00 utc
        生成perf
                perf内容：由于是第一交易日的开始时间(非开市时间)，无内容可记
        记录入result：
                记录Index:result.index = 2015-12-01 07:00
        2)2015-12-01 01:30 utc
        生成order，生成transaction，生成position
        3)2015-12-02 00:00 utc
        生成perf
                perf内容：2015-12-01 00:00 utc 至 2015-12-02 00:00 utc期间发生的交易事项及内容
        记录入result:
                记录Index:result.index = 2015-12-02 07:00
        
        之后的4)5)6)同上
        
        不合逻辑的地方需特别注意：
	1)perf的生成时间和记录时间不一致，00:00生成(当日开始(非开市))，07:00记录(当日收市)
	2)perf记录的是00:00之前一日的交易，记录时点却是当日收盘(当日收盘时间的记录，给人直观的理解应是记录当日开盘到收盘期间发生的业务)
        '''
        self.results = results
        # 1) creates layouts
        dialog = QtGui.QDialog()   
        mainLayout = QtGui.QHBoxLayout()
        rightLayout = QtGui.QVBoxLayout()
        mainLayout.addLayout(rightLayout)
        dialog.setLayout(mainLayout)        
        dialog.setWindowTitle(('Strategy Results'))

        import os,sys        
        xpower = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,os.pardir,os.pardir,os.pardir,'histdataUI'))
        sys.path.append(xpower)
    
        from Widgets.pgCandleWidgetCross import pgCandleWidgetCross
        from Widgets.pgCrossAddition import pgCrossAddition
        from pyqtgraph.dockarea import DockArea,Dock 
        area = DockArea()   
        rightLayout.addWidget(area)
        
        # 2) creates widgets 
        #  2.1)candle        
        pgCandleView = pgCandleWidgetCross(dataForCandle=KData)        
        self.pricePlot(pgCandleView) 
        self.pricePlot(pgCandleView)    
        self.indicatorsPlot(pgCandleView) 
        self.signalPlot(pgCandleView)
        dCandle = Dock("candles",closable=True, size=(200,300))     ## give this dock the minimum possible size
        area.addDock(dCandle, 'bottom') 
        dCandle.addWidget(pgCandleView)        
        
        #  2.2)position_pnl 当前position_pnl曲线
        if(True):
            PyqtGraphPnl = pgCrossAddition()
            self.positionPnlPlot(PyqtGraphPnl,bDrawText=bDrawText)
            self.signalPlot(PyqtGraphPnl)
            dPnl = Dock("position_pnl", closable=True, size=(200,100))
            area.addDock(dPnl, 'bottom')    
            dPnl.addWidget(PyqtGraphPnl)           
            PyqtGraphPnl.setXLink(pgCandleView)
        # 2.3)position_cost 
        if(True):
            PyqtGraphPositionCost = pgCrossAddition()
            self.positionCostPlot(PyqtGraphPositionCost)
            dPositionCost = Dock("position_cost",closable=True, size=(200,100))
            area.addDock(dPositionCost, 'bottom')        
            dPositionCost.addWidget(PyqtGraphPositionCost)             
            PyqtGraphPositionCost.setXLink(pgCandleView)         
        #  2.3)position_volume
        if(False):
            PyqtGraphPosition = pgCrossAddition()
            self.positionVolumePlot(PyqtGraphPosition)
            dPosition = Dock("position_volume",closable=True, size=(200,100))
            area.addDock(dPosition, 'bottom')        
            dPosition.addWidget(PyqtGraphPosition)             
            PyqtGraphPosition.setXLink(pgCandleView)
        #  2.4)portfolio  总资产变动曲线 cash + equity
        if(True):
            PyqtGraphPortfolio = pgCrossAddition()
            self.portfolioPlot(PyqtGraphPortfolio)
            dPortfolio = Dock("portfolio", closable=True,size=(200,100))
            area.addDock(dPortfolio, 'bottom')     
            dPortfolio.addWidget(PyqtGraphPortfolio)        
            PyqtGraphPortfolio.setXLink(pgCandleView)
        #  2.5)indicator
        if(False):
            PyqtGraphindicators = pgCrossAddition()
            self.pricePlot(PyqtGraphindicators)    
            self.indicatorsPlot(PyqtGraphindicators)
            dIndicator = Dock("indicator",closable=True, size=(200,100))
            dIndicator.addWidget(PyqtGraphindicators)
            area.addDock(dIndicator, 'bottom', dCandle)  
            PyqtGraphindicators.setXLink(pgCandleView)
          
        #  2.6)order
        #PyqtGraphOrder = pgCrossAddition()
        #self.orderPlot(PyqtGraphOrder)
        #self.pricePlot(PyqtGraphOrder)

        ## Create docks, place them into the window one at a time.
        ## Note that size arguments are only a suggestion; docks will still have to
        ## fill the entire dock area and obey the limits of their internal widgets.
        #d6 = Dock("order time,amount",size=(200,100))

        #area.addDock(d6, 'bottom', d1)

  
        #d6.addWidget(PyqtGraphOrder)
        
        #PyqtGraphOrder.setXLink(pgCandleView)
        return dialog
    