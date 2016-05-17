# -*- coding: utf-8 -*-
from PyQt4 import QtGui,QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import matplotlib.finance as mpf

class HistoryCandleView(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self,dataForCandle=None,fnUpdateBarInfoCallback=None, parent=None, width=5, height=4, dpi=100):
        self.updateBarInfo = fnUpdateBarInfoCallback
        fig = plt.figure()
        #fig.subplots_adjust(top=0.98,bottom=0.05,left=0.15,right=0.99,hspace =0.1,wspace = 0.1) 

        self.fig = fig
        ax1 = fig.add_subplot(2,4,1)
        ax2 = fig.add_subplot(2,4,2)
        ax3 = fig.add_subplot(2,2,2)
        ax4 = fig.add_subplot(2,1,2)     
        
        fig.tight_layout()        
        
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
        mpf.candlestick(ax, quotes, width,colorup, colordown,alpha)
        ax.xaxis_date()
        ax.autoscale_view()
        #self.addText(ax,quotes[:,0],quotes[:,4])
        for label in ax.xaxis.get_ticklabels():
            label.set_color("red")
            label.set_rotation(30)
            label.set_fontsize(12)   
        ax.grid(True)  



if __name__ == '__main__':
    import os,sys        
    '''
    if(rowSelected>=0):   #a row selected or table is not empty.
        symbolToDownload = self.tableLocalSymbols.item(rowSelected,0).text()
        dataConverter = DataConverter()
        # 1)connect to Mongodb 
        connect = Mongodb('192.168.0.212', 27017)
        connect.use('Tushare')    #database            
        # 2)retrive data from specified collection
        strStart = '2013-12-01'
        dateEnd = dt.datetime.now()
        strEnd = dateEnd.strftime('%Y-%m-%d')  
        frequency = 'D'
        connect.setCollection(frequency)    #table
        history = connect.retrive(symbolToDownload,strStart,strEnd,frequency)
        dataForCandle = dataConverter.DataFrameToCandle(history)            
        
        mainLayout = QtGui.QHBoxLayout(self)
        
        self.historyView = QtGui.QMainWindow()
        self.historyView.setWindowTitle(self.tr(symbolToDownload))
        canvas = HistoryCandleView(dataForCandle=dataForCandle, width=5, height=4, dpi=100)
        self.historyView.setCentralWidget(canvas)

        self.historyView.show()                       
    else:   #none selected and empty table    
    
    '''
    app = QtGui.QApplication([])
    def getCandleData():
        xpower = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,os.pardir,'histdata'))
        sys.path.append(xpower)
    
        import feedsForCandle as feedsForCandle
    
        dataSource={}
        dataSource['ip']='192.168.0.212'
        dataSource['port']=27017
        dataSource['database']='Tushare'
        dataSource['symbol']='600028'
        dataSource['dateStart']='2013-08-19'
        dataSource['dateEnd']='2015-08-31'
        dataSource['frequency']='D'
        dataForCandle = feedsForCandle.GetCandlesFromMongodb(dataSource)
        return dataForCandle    
    
    candleData = getCandleData()    
    #w = QtGui.QWidget()

    symbol = 'none to download.'
    QtGui.QMessageBox.information(None,"Information",str(symbol))      
    
    
    #mainLayout = QtGui.QHBoxLayout(self)
    
    historyView = QtGui.QMainWindow()
    historyView.setWindowTitle(str('600028'))
    canvas = HistoryCandleView(dataForCandle=candleData, width=5, height=4, dpi=100)
    historyView.setCentralWidget(canvas)

    historyView.show()       
    
    
    
    
    #w.show()
    sys.exit(app.exec_())
                 
