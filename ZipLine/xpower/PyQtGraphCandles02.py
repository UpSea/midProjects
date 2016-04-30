import sys
sys.path.append('/home/mid/PythonProjects/xpower/pyqtgraph-0.9.10')
from PyQt4 import QtCore, QtGui
import numpy as np
import pyqtgraph as pg
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.finance as mpf

def getCandleData():
    from DataSources.GetDataFromMongodb import GetDataFromMongodb
    dataSource={}
    dataSource['ip']='192.168.1.100'
    dataSource['port']=27017
    dataSource['database']='Tushare'
    dataSource['symbol']='600311'
    dataSource['dateStart']='2013-08-19'
    dataSource['dateEnd']='2015-08-31'
    dataSource['frequency']='D'
    dataForZipline,dataForCandle = GetDataFromMongodb(dataSource)
    return dataForCandle

class CandlestickItem(pg.GraphicsObject):
    def __init__(self, data):
        pg.GraphicsObject.__init__(self)
        self.data = data  ## data must have fields: time, open, close, min, max
        self.generatePicture()
    
    def generatePicture(self):
        ## pre-computing a QPicture object allows paint() to run much more quickly, 
        ## rather than re-drawing the shapes every time.
        self.picture = QtGui.QPicture()
        p = QtGui.QPainter(self.picture)
        p.setPen(pg.mkPen('w'))
        barWidth = (self.data[1][0] - self.data[0][0]) / 3.
        
        for index,item in enumerate(self.data):
            time = item[0]
            open = item[1]
            high = item[2]
            low = item[3]
            close = item[4]
            
            # 01.draw high-low line,when high == low,it means the symbol is not traded.
            if(high != low):
                p.drawLine(QtCore.QPointF(index, low), QtCore.QPointF(index, high))
            
            # 02.decide the color of candle
            if open > close:
                p.setBrush(pg.mkBrush('g'))
            else:
                p.setBrush(pg.mkBrush('r'))
            
            # 03.draw the candle rect
            x=index-barWidth
            y=open
            width= barWidth*2
            height=close-open

            p.drawRect(QtCore.QRectF(x,y ,width,height))
        p.end()
    
    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)
    
    def boundingRect(self):
        ## boundingRect _must_ indicate the entire area that will be drawn on
        ## or else we will get artifacts and possibly crashing.
        ## (in this case, QPicture does all the work of computing the bouning rect for us)
        return QtCore.QRectF(self.picture.boundingRect())
    
class MyMplCanvas(FigureCanvas):
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
class MyPyqtGraphPlot(pg.PlotWidget):
    def __init__(self, dataForCandle=None):
        super(MyPyqtGraphPlot, self).__init__()
        item01 = CandlestickItem(dataForCandle)        
        self.addItem(item01)                  
class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('pyqtgraph example: PlotWidget')
        self.resize(800,800)
        centerwidget = QtGui.QWidget()
        self.setCentralWidget(centerwidget)
        layout = QtGui.QVBoxLayout()
        centerwidget.setLayout(layout)
        
        candleData = getCandleData()
        
        mplWidget = MyMplCanvas(dataForCandle=candleData,width=5, height=4, dpi=100)
        layout.addWidget(mplWidget)    
        
        plt = MyPyqtGraphPlot(dataForCandle=candleData)
        layout.addWidget(plt)
        
        PyqtGraph02 = pg.PlotWidget()
        layout.addWidget(PyqtGraph02)
        
        
        #p3.setXLink(p1)
        
        PyqtGraph02.setXLink(plt)
        
        x = np.random.normal(size=300)
        y = np.random.normal(size=300)
    
        PyqtGraph02.plot(x,y, pen=(255,0,0), name="Red curve")

        for x1,y1 in zip(x,y):
            a1 = pg.ArrowItem(angle=x1*100, tipAngle=x1*10, headLen=x1*10, tailLen=y1*10, tailWidth=y1*10, pen={'color': 'w', 'width': 3})
            PyqtGraph02.addItem(a1)
            a1.setPos(x1,y1)         
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    
    mw = MainWindow()
    mw.show()

    sys.exit(app.exec_())