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
        mpf.candlestick_ohlc(ax, quotes, width,colorup, colordown,alpha)
        ax.xaxis_date()
        ax.autoscale_view()
        #self.addText(ax,quotes[:,0],quotes[:,4])
        for label in ax.xaxis.get_ticklabels():
            label.set_color("red")
            label.set_rotation(30)
            label.set_fontsize(12)   
        ax.grid(True)  
