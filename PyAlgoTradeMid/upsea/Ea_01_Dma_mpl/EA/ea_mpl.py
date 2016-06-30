# -*- coding: utf-8 -*-
import os,sys
from pyalgotrade import plotter

from .dma_crossover import cross as cross

dataRoot = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,os.pardir,os.pardir,os.pardir,'histdata'))        
sys.path.append(dataRoot)        

import dataCenter as dataCenter 
import dma_crossover as dma_crossover
class Expert():
    def __init__(self,toPlot = True,instruments = [],shortPeriod = 20,longPeriod = 40,dataProvider = 'tushare',storageType = 'mongodb',period = 'D',toYear = '',fromYear='',money = None):
        self.instrument = instruments[0]
        self.shortPeriod = shortPeriod
        self.longPeriod = longPeriod
        self.toPlot = toPlot
        
        #mid data
        self.dataCenter = dataCenter.dataCenter()           
        #mid dataProvider = tushareCsv|tushare|yahooCsv|yahoo|generic
        feeds = self.dataCenter.getFeedsForPAT(dataProvider = dataProvider,storageType = storageType,instruments = instruments,period=period,
                                                   timeTo = toYear,timeFrom=fromYear)
        self.feed = feeds[self.instrument]
        #mid money
        self.money = money
        
        #mid strategy
        self.strat = dma_crossover.DMACrossOver(feed=self.feed, instrument=self.instrument,shortPeriod=self.shortPeriod,
                                                longPeriod=self.longPeriod,money=money)
        #self.strat.setUseAdjustedValues(False)
        
        #mid results
        self.initAnalyzer()
    def initAnalyzer(self):
        from pyalgotrade.stratanalyzer import sharpe
        from pyalgotrade.stratanalyzer import returns
        from pyalgotrade.stratanalyzer import drawdown
        from pyalgotrade.stratanalyzer import trades        
        
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
        
        position = strat.getPositionVolume()
        SPlotter.getOrCreateSubplot("position").addDataSeries("position", position)    
        return SPlotter
    def run(self):
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
        if(self.toPlot):#自定义方式获取figure，并对其进行设置
            import matplotlib.pyplot as plt
            fig = spPlooter.buildFigure()
            fig.tight_layout()    
            plt.show()
        else:#使用pyalgo的方式绘制
            spPlooter.plot()
