# -*- coding: utf-8 -*-
import os,sys
from PyQt4 import QtGui,QtCore
#mid 1)dataCenter
dataRoot = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,os.pardir,os.pardir,os.pardir,'histdata'))        
sys.path.append(dataRoot)        
xpower = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,os.pardir,'histdataUI'))
sys.path.append(xpower)   

import dataCenter as dataCenter 
from Analyzer import Analyzer
import Dma_crossover as dma_crossover
class Expert():
    def __init__(self,toPlot = True,instruments = [],shortPeriod = 20,longPeriod = 40,dataProvider = 'tushare',
                 storageType = 'mongodb',period = 'D',money = None):
        self.instruments = instruments
        self.instrument = instruments[0]
        self.shortPeriod = shortPeriod
        self.longPeriod = longPeriod
        self.dataProvider = dataProvider
        self.storageType = storageType
        self.period = period
        self.toPlot = toPlot        
        self.money = money
        self.analyzers = []     #mid every ea has many windows which should be kept separatly,other wise previous one will be release after new one constructed. 
    def run(self,timeFrom = None,timeTo = None):
        self.timeFrom = timeFrom
        self.timeTo = timeTo        
        self.dataCenter = dataCenter.dataCenter()           
        feeds = self.dataCenter.getFeedsForPAT(dataProvider = self.dataProvider,storageType = self.storageType,instruments = self.instruments,
                                               period=self.period,timeTo = timeTo,timeFrom=timeFrom)
        self.feed = feeds[self.instrument]

        #mid strategy
        self.strat = dma_crossover.DMACrossOver(feed=self.feed, instrument=self.instrument,shortPeriod=self.shortPeriod,
                                                longPeriod=self.longPeriod,money=self.money)
        #self.strat.setUseAdjustedValues(False)
        
        #mid results
        self.initAnalyzer()        
        result = self.strat.run()
        if(self.toPlot):
            analyzer = Analyzer(Globals=[]) 
            dataForCandle = dataCenter.getCandleData(dataProvider = self.dataProvider,dataStorage = self.storageType,dataPeriod = self.period,
                                                    symbol = self.instrument,dateStart=timeFrom,dateEnd = timeTo)     
            analyzer.analyze(result,dataForCandle)        
            self.analyzers.append(analyzer)
        
        return result        
    def initAnalyzer(self):
        from pyalgotrade.stratanalyzer import sharpe
        from pyalgotrade.stratanalyzer import returns
        from pyalgotrade.stratanalyzer import drawdown
        from pyalgotrade.stratanalyzer import trades        
        # 1.0) 策略结果
        self.returnsAnalyzer = returns.Returns()
        # 1.1) 夏普比率 
        self.sharpeRatioAnalyzer = sharpe.SharpeRatio()
        # 1.2) 
        self.drawdownAnalyzer = drawdown.DrawDown()
        # 1.3)
        self.tradesAnalyzer = trades.Trades()     
        
        self.strat.attachAnalyzer(self.sharpeRatioAnalyzer)
        self.strat.attachAnalyzer(self.returnsAnalyzer)    
        self.strat.attachAnalyzer(self.tradesAnalyzer)   
        self.strat.attachAnalyzer(self.drawdownAnalyzer)
    #----------------------------------------------------------------------
    def summary(self):
        return "from %s to %s:returns:%.2f%%,sharpe:%.2f,MaxDrawdown:%.2f%%,Longest drawdown duration:(%s)" % (str(self.timeFrom),str(self.timeTo),
                                                                                                            self.returnsAnalyzer.getCumulativeReturns()[-1] * 100,
                                                                                                            self.sharpeRatioAnalyzer.getSharpeRatio(0.05),
                                                                                                            self.drawdownAnalyzer.getMaxDrawDown() * 100,
                                                                                                            self.drawdownAnalyzer.getLongestDrawDownDuration())
    def detail(self):
        """"""        
        print "-------------------------------------------------------------------------"
        print "Final portfolio value: $%.2f" % self.strat.getResult()
        print "Cumulative returns: %.2f %%" % (self.returnsAnalyzer.getCumulativeReturns()[-1] * 100)
        print "Sharpe ratio: %.2f" % (self.sharpeRatioAnalyzer.getSharpeRatio(0.05))
        print "Max. drawdown: %.2f %%" % (self.drawdownAnalyzer.getMaxDrawDown() * 100)
        print "Longest drawdown duration: (%s)" % (self.drawdownAnalyzer.getLongestDrawDownDuration())
        
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
        print "-------------------------------------------------------------------------"
