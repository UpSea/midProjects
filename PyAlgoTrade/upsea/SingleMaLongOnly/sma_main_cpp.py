from pyalgotrade import plotter
from pyalgotrade.tools import yahoofinance
from pyalgotrade.barfeed import yahoofeed

from pyalgotrade.stratanalyzer import sharpe
from pyalgotrade.stratanalyzer import returns
from pyalgotrade.stratanalyzer import drawdown
from pyalgotrade.stratanalyzer import trades

#from BollingerBands import BBands
import sma_crossover

class Expert():
    def __init__(self):
        self.instrument = "yhoo"
        self.period = 40
        self.feed = self.getFeedFromYahoo(self.instrument)
        #self.feed = self.getFeedFromCsv(self.instrument)
        self.strat = sma_crossover.SMACrossOver(self.feed, self.instrument, self.period)
        
        self.initAnalyzer()
    def getFeedFromCsv(self,instrument):
        feed = yahoofeed.Feed()
        # -*- coding: cp936 -*-
        import sys,os
        fullName = os.path.abspath(os.path.join(os.path.dirname(__file__),"data\\orcl-2000.csv"))     
        feed.addBarsFromCSV(instrument, fullName)  
        return feed
    def getFeedFromYahoo(self,instrument):
        feed = yahoofinance.build_feed([instrument], 2008, 2012, "data")    
        return feed
    def initAnalyzer(self):
        #self.strat = BBands(self.feed, self.instrument, self.bBandsPeriod) 
        
        self.returnsAnalyzer = returns.Returns()
        self.sharpeRatioAnalyzer = sharpe.SharpeRatio()
        self.drawdownAnalyzer = drawdown.DrawDown()
        self.tradesAnalyzer = trades.Trades()        
    def analyzer(self,strat,instrument):
        SPlotter = plotter.StrategyPlotter(strat, True, True, True)  #mid (self, strat, plotAllInstruments=True, plotBuySell=True, plotPortfolio=True)
        #SPlotter.getInstrumentSubplot(instrument).addDataSeries("upper", strat.getBollingerBands().getUpperBand())
        #SPlotter.getInstrumentSubplot(instrument).addDataSeries("middle", strat.getBollingerBands().getMiddleBand())
        SPlotter.getInstrumentSubplot(instrument).addDataSeries("lower", strat.getSMA())
        #SPlotter.getOrCreateSubplot("Returns").addDataSeries("Simple returns", self.returnsAnalyzer.getReturns())    
        #SPlotter.getOrCreateSubplot("SharpeRatio").addDataSeries("Sharpe Ratio", self.sharpeRatioAnalyzer.getReturns())    
        #SPlotter.getOrCreateSubplot("SharpeRatio").addDataSeries("Sharpe Ratio", self.tradesAnalyzer.getCommissionsForAllTrades())    

        def addCallBack():
            # mid 使用默认绘图类绘制自定义数据,此处是LineMarker
            def midBars(bars):
                midOpen = bars[self.instrument].getOpen()
                midClose = bars[self.instrument].getClose()
                print midOpen
                return midClose
            SPlotter.getOrCreateSubplot("orders").addCallback("mid's callback",midBars,plotter.LineMarker)    
        def addDataSeries():
            feedDataSeries = self.feed.getDataSeries()
            feedDataSerie = feedDataSeries.getCloseDataSeries()    
            SPlotter.getOrCreateSubplot("orders02").addDataSeries("mid's dataSeries",feedDataSerie,plotter.LineMarker)
        #addCallBack()
        #addDataSeries()    
    
        return SPlotter
    def run(self,plot):
        # 1.0) 夏普比率 
        self.strat.attachAnalyzer(self.sharpeRatioAnalyzer)
        # 1.3) 策略结果
        self.strat.attachAnalyzer(self.returnsAnalyzer)    
        # 1.4) 
        self.strat.attachAnalyzer(self.tradesAnalyzer)
        # 1.4) 策略结果图形化关联
        spPlooter = self.analyzer(self.strat,self.instrument)    
        self.strat.run()
        print "Sharpe ratio: %.2f" % self.sharpeRatioAnalyzer.getSharpeRatio(0.05)
    
        # Plot the strategy.
        if(plot):#自定义方式获取figure，并对其进行设置
            import matplotlib.pyplot as plt
            fig = spPlooter.buildFigure()
            fig.tight_layout()    
            plt.show()
        else:#使用pyalgo的方式绘制
            spPlooter.plot()


if __name__ == "__main__":
    ex = Expert()
    ex.run(True)