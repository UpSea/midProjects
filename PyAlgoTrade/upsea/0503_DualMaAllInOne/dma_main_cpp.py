from pyalgotrade import plotter

from pyalgotrade.stratanalyzer import sharpe
from pyalgotrade.stratanalyzer import returns
from pyalgotrade.stratanalyzer import drawdown
from pyalgotrade.stratanalyzer import trades

import os,sys
dataRoot = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,os.pardir,os.pardir,'histdata'))        
sys.path.append(dataRoot)        
from feedFactory import feeds

import pandas as pd
#from BollingerBands import BBands
import dma_crossover

class Expert():
    def __init__(self):
        self.instrument = "yhoo"
        self.shortPeriod = 20
        self.longPeriod = 40        
        fd = feeds()
        #mid feedFormat = tushareCsv|yahooCsv|generic|yahoo
        self.feed = fd.getFeeds(feedFormat = "tushareCsv",instrument = self.instrument)
        self.strat = dma_crossover.SMACrossOver(self.feed, self.instrument, self.shortPeriod,self.longPeriod)
        
        #self.strat.setUseAdjustedValues(False)
        
        self.initAnalyzer()
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
            # mid ʹ��Ĭ�ϻ�ͼ������Զ�������,�˴���LineMarker
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
        
        position = strat.getTest()
        SPlotter.getOrCreateSubplot("position").addDataSeries("position", position)    
        return SPlotter
    def run(self,plot):
        # 1.0) ���ձ��� 
        self.strat.attachAnalyzer(self.sharpeRatioAnalyzer)
        # 1.3) ���Խ��
        self.strat.attachAnalyzer(self.returnsAnalyzer)    
        # 1.4) 
        self.strat.attachAnalyzer(self.tradesAnalyzer)
        # 1.4) ���Խ��ͼ�λ�����
        spPlooter = self.analyzer(self.strat,self.instrument)    
        self.strat.run()
        print "Sharpe ratio: %.2f" % self.sharpeRatioAnalyzer.getSharpeRatio(0.05)
    
        # Plot the strategy.
        if(plot):#�Զ��巽ʽ��ȡfigure���������������
            import matplotlib.pyplot as plt
            fig = spPlooter.buildFigure()
            fig.tight_layout()    
            plt.show()
        else:#ʹ��pyalgo�ķ�ʽ����
            spPlooter.plot()


if __name__ == "__main__":
    ex = Expert()
    ex.run(True)