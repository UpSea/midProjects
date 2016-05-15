# -*- coding: utf-8 -*-
import sys
sys.path.append('/home/mid/PythonProjects/xpower/pyqtgraph-0.9.10')
from PyQt4 import QtCore, QtGui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.finance as mpf

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
        mpf.candlestick_ohlc(ax, quotes, width,colorup, colordown,alpha)
        ax.xaxis_date()
        ax.autoscale_view()
        #self.addText(ax,quotes[:,0],quotes[:,4])
        for label in ax.xaxis.get_ticklabels():
            label.set_color("red")
            label.set_rotation(30)
            label.set_fontsize(12)   
        ax.grid(True)        
        
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    
    def getCandleData():
        import sys
        #sys.path.append('/home/mid/PythonProjects/xpower')  
        from os.path import dirname, realpath
        root = dirname(dirname(realpath(__file__)))
        sys.path.append(root)          
        
        from DataSources.GetDataFromMongodb import GetDataFromMongodb
        dataSource={}
        dataSource['ip']='192.168.1.100'
        dataSource['port']=27017
        dataSource['database']='Tushare'
        dataSource['symbol']='600311'
        dataSource['dateStart']='2014-12-19'
        dataSource['dateEnd']='2015-08-31'
        dataSource['frequency']='D'
        dataForZipline,dataForCandle = GetDataFromMongodb(dataSource)
        return dataForCandle    
    
    candleData = getCandleData()
    
    mw = mplCandleWidget(dataForCandle=candleData)
    
    mw.show()
    sys.exit(app.exec_())