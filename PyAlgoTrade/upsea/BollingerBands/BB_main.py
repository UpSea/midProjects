from pyalgotrade import plotter
from pyalgotrade.tools import yahoofinance
from pyalgotrade.barfeed import yahoofeed

from pyalgotrade.stratanalyzer import sharpe
from pyalgotrade.stratanalyzer import returns
from pyalgotrade.stratanalyzer import drawdown
from pyalgotrade.stratanalyzer import trades

from BollingerBands import BBands

class Expert():
    def __init__(self):
        self.instrument = "yhoo"
        self.bBandsPeriod = 40
        #self.feed = self.getFeedFromYahoo(self.instrument)
        self.feed = self.getFeedFromCsv(self.instrument)
        self.initAnalyzer()
    def getFeedFromCsv(self,instrument):
        feed = yahoofeed.Feed()
        # -*- coding: cp936 -*-
        import sys,os
        path01 = os.path.abspath(os.path.join(os.path.dirname(__file__),"data\\orcl-2000.csv"))     
        #��ȡ�ű��ļ��ĵ�ǰ·��
        def cur_file_dir():
            #��ȡ�ű�·��
            path = sys.path[0]
            #�ж�Ϊ�ű��ļ�����py2exe�������ļ�������ǽű��ļ����򷵻ص��ǽű���Ŀ¼�������py2exe�������ļ����򷵻ص��Ǳ������ļ�·��
            if os.path.isdir(path):
                return path
            elif os.path.isfile(path):
                return os.path.dirname(path)
            
        #��ӡ���
        print cur_file_dir()        
        feed.addBarsFromCSV(instrument, path01)  
        return feed
    def getFeedFromYahoo(self,instrument):
        feed = yahoofinance.build_feed([instrument], 2000, 2016, "data")    
        return feed
    def initAnalyzer(self):
        self.strat = BBands(self.feed, self.instrument, self.bBandsPeriod)        
        self.returnsAnalyzer = returns.Returns()
        self.sharpeRatioAnalyzer = sharpe.SharpeRatio()
        self.drawdownAnalyzer = drawdown.DrawDown()
        self.tradesAnalyzer = trades.Trades()        
    def analyzer(self,strat,instrument):
        SPlotter = plotter.StrategyPlotter(strat, True, True, True)  #mid (self, strat, plotAllInstruments=True, plotBuySell=True, plotPortfolio=True)
        SPlotter.getInstrumentSubplot(instrument).addDataSeries("upper", strat.getBollingerBands().getUpperBand())
        SPlotter.getInstrumentSubplot(instrument).addDataSeries("middle", strat.getBollingerBands().getMiddleBand())
        SPlotter.getInstrumentSubplot(instrument).addDataSeries("lower", strat.getBollingerBands().getLowerBand())
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