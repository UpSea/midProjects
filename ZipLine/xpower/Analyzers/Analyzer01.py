import matplotlib.pyplot as plt
import matplotlib.dates as mpd
import matplotlib.finance as mpf
import numpy as np
import datetime as dt

class Analyzer01():
    """"""
    #----------------------------------------------------------------------
    def __init__(self,fig=None):
        """Constructor"""
        if fig==None:
            self.fig = plt.figure()
        else:
            self.fig = fig
    def addText(self,ax,xAxis,yAxis):        #mid add some y value to ax.
        #return
        for x,y in zip(xAxis,yAxis):
            text = '('+str(round(y,3))+')'
            ax.annotate(text,xy=(x,y))   
    #----------------------------------------------------------------------
    def candlePlot(self,ax,quotes, width=0.6,colorup='b', colordown='r',alpha=0.5,bDrawText=False): 
        mpf.candlestick_ohlc(ax, quotes, width,colorup, colordown,alpha)

        ax.xaxis_date()
        ax.autoscale_view()
        if(bDrawText):
            self.addText(ax,quotes[:,0],quotes[:,4])
        for label in ax.xaxis.get_ticklabels():
            label.set_color("red")
            label.set_rotation(30)
            label.set_fontsize(12)   
        ax.grid(True)  
    #----------------------------------------------------------------------
    def portfolioPlot(self,ax,bDrawText=False):
        """"""
        ax.set_ylabel('Portfolio value (USD)')  
        ax.plot(self.results.index,self.results.portfolio_value)
        ax.scatter(self.results.index,self.results.portfolio_value,s=self.results.portfolio_value/1000,c='g')
        if(bDrawText):
            self.addText(ax,self.results.index,self.results.portfolio_value)  
        ax.grid(True)  
    def positionPlot(self,ax,bDrawText=False):  
        # 4)create positions axes
        def getPositions(positions):    
            if(len(positions)>0):
                for position in positions:
                    return position['amount']                
            else:
                return 0
        positions = list(map(getPositions, self.results.iloc[:]['positions']))
        ax.plot(self.results.index, positions)
        ax.scatter(self.results.index, positions,s=positions*5000,c='r')
        ax.set_ylabel('Position')
        if(bDrawText):
            self.addText(ax,self.results.index,positions)
        ax.grid(True)      
    #----------------------------------------------------------------------
    def pricePlot(self,ax,bDrawText=False):
        """"""
        ax.plot(self.results.index,self.results.AAPL)
        ax.scatter(self.results.index,self.results.AAPL)
        ax.set_ylabel('AAPL price (USD)')
        if(bDrawText):
            self.addText(ax,self.results.index,self.results.AAPL)   
        ax.grid(True)  
    def pnlPlot(self,ax,bDrawText=False):
        # 5)creat pnl axes
        ax.plot(self.results.index, self.results.pnl)
        ax.scatter(self.results.index, self.results.pnl,s=self.results.AAPL**2+100,c='r')
        ax.set_ylabel('pnl')
        if(bDrawText):
            self.addText(ax,self.results.index,self.results.pnl)     
        ax.grid(True)  
    def analyze(self,results=None,KData=None,bDrawText=False):
        # Plot the portfolio and asset data.
        self.results = results
        self.KData = KData
        
        fig = self.fig
        
        ax1 = fig.add_subplot(511)
        ax2 = fig.add_subplot(512)
        ax3 = fig.add_subplot(513)        
        ax4 = fig.add_subplot(514)        
        ax5 = fig.add_subplot(515)
        
        self.pnlPlot(ax1,bDrawText=bDrawText)
        self.positionPlot(ax2,bDrawText=bDrawText)
        self.portfolioPlot(ax3,bDrawText=bDrawText)
        self.pricePlot(ax4,bDrawText=bDrawText)
        self.candlePlot(ax5,KData,alpha=1.0,bDrawText=bDrawText)
        
       
        # Show the plot.
        fig.set_size_inches(18, 8)
        fig.tight_layout()