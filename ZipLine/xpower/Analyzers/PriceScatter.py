# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib.dates as mpd
import matplotlib.finance as mpf
import numpy as np
import datetime as dt

import sys
sys.path.append('/home/mid/PythonProjects/xpower/pyqtgraph-0.9.10')
import pyqtgraph as pg

from PyQt4 import QtGui,QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

class PriceScatter():
    """"""
    #----------------------------------------------------------------------
    def __init__(self,Globals=None):
        """Constructor"""
        self.Globals = Globals
    #----------------------------------------------------------------------
    def pricePlot(self,ax,bDrawText=False):
        """"""
        date = np.array([mpd.date2num(date) for date in self.results.index]) 
        if 'AAPL' in self.results:
            ax.plot(date,self.results.AAPL)
            
            ax.scatterAddition(date, self.results.AAPL)                   
    def analyze(self,results=None,KData=None,bDrawText=False):
        # Plot the portfolio and asset data.
        self.results = results
        self.KData = KData
        
        mw = QtGui.QMainWindow()
        print("before append:",len(self.Globals))      
        self.Globals.append(mw)     # mid 必须使窗体变量的生命与mainframe相同，否则，会闪退
        
        dialog  = self.initDialog(results=results,KData=KData)
        mw.setCentralWidget(dialog) 
        mw.showMaximized()
    def initDialog(self,results=None,KData=None,bDrawText=False):
        # 1) creates layouts
        dialog = QtGui.QDialog()   
        mainLayout = QtGui.QHBoxLayout()
        rightLayout = QtGui.QVBoxLayout()
        mainLayout.addLayout(rightLayout)
        dialog.setLayout(mainLayout)        
        dialog.setWindowTitle(('Strategy Results'))
        # 2) creates widgets         
        from Widgets.pgCandleWidgetCross import pgCandleWidgetCross
        from Widgets.pgCrossAddition import pgCrossAddition
        from pyqtgraph.dockarea import DockArea,Dock     
        
    

        area = DockArea()
        ## Create docks, place them into the window one at a time.
        ## Note that size arguments are only a suggestion; docks will still have to
        ## fill the entire dock area and obey the limits of their internal widgets.
        d1 = Dock("price", size=(200,100))
        d2 = Dock("position", size=(200,100))


        area.addDock(d1, 'bottom')  
        area.addDock(d2, 'bottom')  

        rightLayout.addWidget(area)
       
       
       
        
        pgCandleView = pgCandleWidgetCross(dataForCandle=KData)            
        PyqtGraphindicators = pgCrossAddition()
        toShow = pgCandleView
        self.pricePlot(toShow) 
        d1.addWidget(toShow)   
        
        PyqtGraphPosition = pgCrossAddition()
        self.positionPlot(PyqtGraphPosition)        
        d2.addWidget(PyqtGraphPosition)
        PyqtGraphPosition.showGrid(x=True, y=True)
        
        PyqtGraphPosition.setXLink(toShow)        
        return dialog
    def positionPlot(self,ax,bDrawText=False):  
        # 4)create positions axes
        def getPositions(positions):    
            if(len(positions)>0):
                for position in positions:
                    return position['amount']                
            else:
                return 0
        positions = list(map(getPositions, self.results.iloc[:]['positions']))
        
        date = np.array([mpd.date2num(date) for date in self.results.index]) 
        ax.plot(date, positions,pen=(255,0,0), name="Position curve")
        ax.scatterAddition(date, positions)     