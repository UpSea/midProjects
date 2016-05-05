from pyalgotrade import plotter
from pyalgotrade.tools import yahoofinance
from pyalgotrade.barfeed import yahoofeed

from pyalgotrade.stratanalyzer import sharpe
from pyalgotrade.stratanalyzer import returns
from pyalgotrade.stratanalyzer import drawdown
from pyalgotrade.stratanalyzer import trades

#from BollingerBands import BBands
import dma_crossover

class Expert():
    def __init__(self):
        self.instrument = "yhoo"
        self.shortPeriod = 20
        self.longPeriod = 40
        self.feed = self.getFeedFromYahoo(self.instrument)
        #self.feed = self.getFeedFromCsv(self.instrument)
        self.strat = dma_crossover.SMACrossOver(self.feed, self.instrument, self.shortPeriod,self.longPeriod)
        self.initAnalyzer()
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
        SPlotter.getInstrumentSubplot(instrument).addDataSeries("short", strat.getSMA())
        SPlotter.getInstrumentSubplot(instrument).addDataSeries("long", strat.getLMA())
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
    def stat(self):
        print "Sharpe ratio: %.2f" % self.sharpeRatioAnalyzer.getSharpeRatio(0.05)
        
        
        print "Final portfolio value: $%.2f" % self.strat.getResult()
        print "Cumulative returns: %.2f %%" % (self.returnsAnalyzer.getCumulativeReturns()[-1] * 100)
        print "Sharpe ratio: %.2f" % (self.sharpeRatioAnalyzer.getSharpeRatio(0.05))
        print "Max. drawdown: %.2f %%" % (self.drawdownAnalyzer.getMaxDrawDown() * 100)
        print "Longest drawdown duration: %s" % (self.drawdownAnalyzer.getLongestDrawDownDuration())
        
        print
        print "Total trades: %d" % (self.tradesAnalyzer.getCount())
        if self.tradesAnalyzer.getCount() > 0:
            profits = self.tradesAnalyzer.getAll()
            print "Avg. profit: $%2.f" % (profits.mean())
            print "Profits std. dev.: $%2.f" % (profits.std())
            print "Max. profit: $%2.f" % (profits.max())
            print "Min. profit: $%2.f" % (profits.min())
            returns = self.tradesAnalyzer.getAllReturns()
            print "Avg. return: %2.f %%" % (returns.mean() * 100)
            print "Returns std. dev.: %2.f %%" % (returns.std() * 100)
            print "Max. return: %2.f %%" % (returns.max() * 100)
            print "Min. return: %2.f %%" % (returns.min() * 100)
        
        print
        print "Profitable trades: %d" % (self.tradesAnalyzer.getProfitableCount())
        if self.tradesAnalyzer.getProfitableCount() > 0:
            profits = self.tradesAnalyzer.getProfits()
            print "Avg. profit: $%2.f" % (profits.mean())
            print "Profits std. dev.: $%2.f" % (profits.std())
            print "Max. profit: $%2.f" % (profits.max())
            print "Min. profit: $%2.f" % (profits.min())
            returns = self.tradesAnalyzer.getPositiveReturns()
            print "Avg. return: %2.f %%" % (returns.mean() * 100)
            print "Returns std. dev.: %2.f %%" % (returns.std() * 100)
            print "Max. return: %2.f %%" % (returns.max() * 100)
            print "Min. return: %2.f %%" % (returns.min() * 100)
        
        print
        print "Unprofitable trades: %d" % (self.tradesAnalyzer.getUnprofitableCount())
        if self.tradesAnalyzer.getUnprofitableCount() > 0:
            losses = self.tradesAnalyzer.getLosses()
            print "Avg. loss: $%2.f" % (losses.mean())
            print "Losses std. dev.: $%2.f" % (losses.std())
            print "Max. loss: $%2.f" % (losses.min())
            print "Min. loss: $%2.f" % (losses.max())
            returns = self.tradesAnalyzer.getNegativeReturns()
            print "Avg. return: %2.f %%" % (returns.mean() * 100)
            print "Returns std. dev.: %2.f %%" % (returns.std() * 100)
            print "Max. return: %2.f %%" % (returns.max() * 100)
            print "Min. return: %2.f %%" % (returns.min() * 100)        
    def run(self,plot):
        # 1.2) 回撤统计
        self.strat.attachAnalyzer(self.drawdownAnalyzer)
        # 1.2) 夏普比率 
        self.strat.attachAnalyzer(self.sharpeRatioAnalyzer)
        # 1.3) 策略结果
        self.strat.attachAnalyzer(self.returnsAnalyzer)    
        # 1.4) 交易统计
        self.strat.attachAnalyzer(self.tradesAnalyzer)
        # 1.4) 策略结果图形化关联
        spPlooter = self.analyzer(self.strat,self.instrument)    
        self.strat.run()
        self.stat()
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