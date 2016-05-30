# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtCore, QtGui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.finance as mpf
import numpy   as np

class mplCandleWidget(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, dataForCandle=None,parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        axes01 = fig.add_subplot(111)
        #axes02 = fig.add_subplot(212)
        self.candlePlot(axes01,dataForCandle,alpha=1.0) 
        
        FigureCanvas.__init__(self, fig)
        fig.tight_layout()
    def candlePlot(self,ax,quotes, width=0.6,colorup='r', colordown='g',alpha=0.5): 
        if sys.version > '3':
            PY3 = True
        else:
            PY3 = False   
            
        if (PY3 == True):        
            mpf.candlestick_ohlc(ax, quotes, width,colorup, colordown,alpha)
        else:        
            #opens, closes, highs, lows,
            time  = quotes[:,0]
            opens = quotes[:,1]
            closes= quotes[:,4]
            highs = quotes[:,2]
            lows  = quotes[:,3]    
            quotesNew = np.vstack((time,opens,closes,highs,lows))
            mpf.candlestick(ax, quotesNew.T, width,colorup, colordown,alpha)
        ax.xaxis_date()
        ax.autoscale_view()
        #self.addText(ax,quotes[:,0],quotes[:,4])
        for label in ax.xaxis.get_ticklabels():
            label.set_color("red")
            label.set_rotation(30)
            label.set_fontsize(12)   
        ax.grid(True)        
        
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    import os,sys
    dataRoot = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,os.pardir,'histdata'))        
    sys.path.append(dataRoot)        
    import dataCenter as dataCenter   
    candleData = dataCenter.getCandleData()  
    
    
    mw = mplCandleWidget(dataForCandle=candleData)
    
    mw.showMaximized()
    sys.exit(app.exec_())