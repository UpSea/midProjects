import matplotlib.pyplot as plt
import matplotlib.dates as mpd
import matplotlib.finance as mpf
class Analyzer03():
    """"""
    #----------------------------------------------------------------------
    def __init__(self,fig=None):
        """Constructor"""
        if fig==None:
            self.fig = plt.figure()
        else:
            self.fig = fig        
    #----------------------------------------------------------------------
    def drawCandle(self,ax,quotes, width=0.6,colorup='b', colordown='r',alpha=0.5,bDrawText=False): 
        mpf.candlestick_ohlc(ax, quotes, width,colorup, colordown,alpha)
        ax.grid(True)
        ax.xaxis_date()
        ax.autoscale_view()
        if(bDrawText):
            self.addText(ax,quotes[:,0],quotes[:,4])
        for label in ax.xaxis.get_ticklabels():
            label.set_color("red")
            label.set_rotation(30)
            label.set_fontsize(12)    
    def addText(self,ax,xAxis,yAxis):        #mid add some y value to ax.
        for x,y in zip(xAxis,yAxis):
            text = '('+str(round(y,3))+')'
            ax.annotate(text,xy=(x,y))       
    def analyze(self, results=None,KData=None,bDrawText=False):
        import matplotlib.pyplot as plt
        import logbook  
        logbook.StderrHandler().push_application()
        log = logbook.Logger('Algorithm')
    
        fig = self.fig
    
        ax1 = fig.add_subplot(311)
        ax1.set_ylabel('Portfolio value (USD)')
        results.portfolio_value.plot(ax=ax1)  

        ax2 = fig.add_subplot(312)
        ax2.set_ylabel('Price (USD)')
    
        ax3 = fig.add_subplot(313)  
        self.drawCandle(ax3,KData,alpha=1.0,bDrawText=bDrawText) 
        # If data has been record()ed, then plot it.
        # Otherwise, log the fact that no data has been recorded.
        if 'AAPL' in results and 'short_ema' in results and 'long_ema' in results:
            results[['AAPL', 'short_ema', 'long_ema']].plot(ax=ax2)
            
            ax3.plot(results.index,results.AAPL)
            ax3.plot(results.index,results.short_ema)
            ax3.plot(results.index,results['long_ema'])
            
            if(bDrawText):
                self.addText(ax2,results.index,results.AAPL)
            
            ax2.plot(results.ix[results.buy].index, results.short_ema[results.buy],
                     '^', markersize=10, color='m')
            ax2.plot(results.ix[results.sell].index,
                     results.short_ema[results.sell],
                     'v', markersize=10, color='k')

            #plt.legend(loc=0)
                # Show the plot.
            fig.set_size_inches(18, 8)
            fig.tight_layout()
        else:
            msg = 'AAPL, short_ema and long_ema data not captured using record().'
            ax2.annotate(msg, xy=(0.1, 0.5))
            log.info(msg)