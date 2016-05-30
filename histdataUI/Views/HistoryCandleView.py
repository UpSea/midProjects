# -*- coding: utf-8 -*-
from PyQt4 import QtGui,QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import matplotlib.finance as mpf
import datetime as dt
import matplotlib.dates as mpd
import numpy as np
import os,sys        

class HistoryCandleView(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self,dataForCandle=None,fnUpdateBarInfoCallback=None, parent=None, width=5, height=4, dpi=100):
        if(fnUpdateBarInfoCallback is not None):
            self.updateBarInfo = fnUpdateBarInfoCallback
        fig = plt.figure()
        #fig.subplots_adjust(top=0.98,bottom=0.05,left=0.15,right=0.99,hspace =0.1,wspace = 0.1) 

        self.fig = fig
        ax1 = fig.add_subplot(2,4,1)
        ax2 = fig.add_subplot(2,4,2)
        ax3 = fig.add_subplot(2,2,2)
        ax4 = fig.add_subplot(2,1,2)     
        
        fig.tight_layout()        
        
        if(dataForCandle is None):
            return
        self.candlePlot(ax1,dataForCandle[-50:-1],colorup='r',colordown='g',alpha=1)
        self.candlePlot(ax2,dataForCandle[-100:-50],colorup='r',colordown='g',alpha=1)    
        self.candlePlot(ax3,dataForCandle[-100:-1],colorup='r',colordown='g',alpha=1)    
        self.candlePlot(ax4,dataForCandle,alpha=1.0)   
        
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        #cMousePress = fig.canvas.mpl_connect('button_press_event', self.onclick) 
        cMouseMove = fig.canvas.mpl_connect('motion_notify_event', self.slotNotifyMotion)
        cMouseEnter = fig.canvas.mpl_connect('axes_enter_event', self.slotEnterAxes)
        cMouseLeave = fig.canvas.mpl_connect('axes_leave_event', self.slotLeaveAxes)
        self.InAxes = False
        #fig.canvas.mpl_disconnect(cid)
    def updateBarInfo(self,event):
        """"""
        #info = 'event.name:{}\nButton:{}\nFig x,y:{}, {}\nData x:{},\nData y:{}'.format(
            #event.name,event.button,event.x,event.y,mpd.num2date(event.xdata),event.ydata) 
        info = 'event.name:{}\nButton:{}\nFig x,y:{}, {}\nData x:{},\nData y:{}'.format(
            event.name,event.button,event.x,event.y,dt.datetime.strftime(mpd.num2date(event.xdata),'%Y-%m-%d %H:%M:%S')  ,event.ydata)        
        #self.infoEdit.setText(info)    
    #----------------------------------------------------------------------
    def slotEnterAxes(self,event):
        """"""
        self.InAxes = True   
    #----------------------------------------------------------------------
    def slotLeaveAxes(self,event):
        """"""
        self.InAxes = False     
    def slotNotifyMotion(self,event):
        if(self.InAxes and event.inaxes is not None):
            self.updateBarInfo(event) 
    def addText(self,ax,xAxis,yAxis):        #mid add some y value to ax.
        for x,y in zip(xAxis,yAxis):
            text = '('+str(round(y,3))+')'
            ax.annotate(text,xy=(x,y))   
    #----------------------------------------------------------------------
    def candlePlot(self,ax,quotes, width=0.6,colorup='b', colordown='r',alpha=0.5): 
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

class MyDialog(QtGui.QDialog):  
    def __init__(self,dataForCandle=None, parent=None):  
        super(MyDialog, self).__init__(parent)  
        # 1) set mainlayout
        layout = QtGui.QHBoxLayout()  
        self.setLayout(layout)     
        # 2) creates layoutLeft and add it to mainlayout
        layoutLeft = QtGui.QVBoxLayout()  
        layout.addLayout(layoutLeft)  
        # 3) add table to layoutLeft
        barLable = QtGui.QLabel('Bar Info:')        
        self.MyTable = QtGui.QTableWidget(4,2)  
        self.MyTable.setHorizontalHeaderLabels(['Item','data'])  
        newItem = QtGui.QTableWidgetItem("datetime")  
        newItem = QtGui.QTableWidgetItem("2015-07-05 22:00:00")          
        self.MyTable.setItem(0, 0, newItem)  
        self.MyTable.setItem(0, 1, newItem) 
        layoutLeft.addWidget(barLable)
        layoutLeft.addWidget(self.MyTable)  
        # 4) add edit to layoutLeft
        infoLable = QtGui.QLabel('Symbol Info:')
        self.infoEdit=QtGui.QTextEdit()
        layoutLeft.addWidget(infoLable)
        layoutLeft.addWidget(self.infoEdit)
        # 5) add canvas to layoutLeft
        fig = plt.figure()
        fig.subplots_adjust(top=0.98,bottom=0.05,left=0.15,right=0.99,hspace =0.1,wspace = 0.1) 
        self.fig = fig
        ax1 = fig.add_subplot(1,1,1) 
        
        mu, sigma    =    100,    15
        x    =    mu    +    sigma    *    np.random.randn(10000)# the histogram of the data
        n, bins, patches =  plt.hist(x,50, normed=1, facecolor='g', alpha=0.75)
        ax1.set_xlabel('Smarts')
        ax1.set_ylabel('Probability')
        ax1.set_title('Histogram of IQ')
        ax1.text(60,.025,'$\mu=100,\\sigma=15$')
        ax1.axis([40,160,0,0.03])
        ax1.grid(True)        

        fig.tight_layout()
        detailCanvas = FigureCanvas(fig)
        #layoutLeft.addWidget(detailCanvas)
        # 4) add button to layoutLeft
        button01 = QtGui.QPushButton('OK01')   
        button02 = QtGui.QPushButton('OK02')
        layoutLeft.addWidget(button01)
        layoutLeft.addWidget(button02)        
        # 5) add candleView to mainlayout
        canvas = HistoryCandleView(dataForCandle=dataForCandle,fnUpdateBarInfoCallback=self.updateBarInfo)        
        #layout.addWidget(canvas)
        
        layout.setStretchFactor(layoutLeft,10)
        #layout.setStretchFactor(canvas,60)
    #----------------------------------------------------------------------
    def updateBarInfo(self,event):
        """"""
        #info = 'event.name:{}\nButton:{}\nFig x,y:{}, {}\nData x:{},\nData y:{}'.format(
            #event.name,event.button,event.x,event.y,mpd.num2date(event.xdata),event.ydata) 
        info = 'event.name:{}\nButton:{}\nFig x,y:{}, {}\nData x:{},\nData y:{}'.format(
            event.name,event.button,event.x,event.y,dt.datetime.strftime(mpd.num2date(event.xdata),'%Y-%m-%d %H:%M:%S')  ,event.ydata)        
        self.infoEdit.setText(info)

if __name__ == '__main__':
    import os,sys        
    app = QtGui.QApplication([])
    def getCandleData():
        import os,sys
        dataRoot = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,os.pardir,'histdata'))        
        sys.path.append(dataRoot)        
        import dataCenter as dataCenter   
    
        dataSource={}
        dataSource['dataProvider'] = 'tushare'
        dataSource['storageFormat']='mongodb'
        dataSource['dataPeriod']='D'
        dataSource['symbol']='600028'
        dataSource['dateStart']='2015-03-19'
        dataSource['dateEnd']='2015-12-31'  
        dataSource['alone'] = True
        dataSource['overlay'] = False   
        
        dataCenter = dataCenter.dataCenter()        
        dataForCandle = dataCenter.retriveCandleData(params = dataSource)     
        
        return dataForCandle    
    
    candleData = getCandleData()  
    myWindow = MyDialog(dataForCandle=candleData)  
    myWindow.show()    
    
    sys.exit(app.exec_())
                 
