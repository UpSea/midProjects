# -*- coding: utf-8 -*-
import os,sys
from PyQt4 import QtGui,QtCore
import pandas as pd

#mid 1)dataCenter
dataRoot = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,os.pardir,'histdata'))        
sys.path.append(dataRoot)        
import dataCenter as dataCenter 
#mid 2)graphOutput
xpower = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,os.pardir,'histdataUI'))
sys.path.append(xpower)        
from Analyzers.Analyzer05 import Analyzer05#from BollingerBands import BBands
#mid 3)strategy
import strategies.dma_crossover_rev as dma_crossover_rev
#mid 4)money
import money.moneyFixed as moneyFixed
import money.moneyFirst as moneyFirst
import money.moneySecond as moneySecond

class Expert():
    def __init__(self,toPlot = True,instruments = [],shortPeriod = 20,longPeriod = 40,dataProvider = 'tushare',
                 storageType = 'mongodb',period = 'D',toYear = '',fromYear='',money = None):
        self.instrument = instruments[0]
        self.shortPeriod = shortPeriod
        self.longPeriod = longPeriod
        self.toPlot = toPlot
        
        #mid data
        self.dataCenter = dataCenter.dataCenter()           
        #mid dataProvider = tushareCsv|tushare|yahooCsv|yahoo|generic
        feeds = self.dataCenter.getFeedsForPAT(dataProvider = dataProvider,storageType = storageType,instruments = instruments,period=period,
                                                   toYear = toYear,fromYear=fromYear)
        self.feed = feeds[self.instrument]
        #mid money
        self.money = money
        
        #mid strategy
        self.strat = dma_crossover_rev.DMACrossOverRev(feed=self.feed, instrument=self.instrument,shortPeriod=self.shortPeriod,
                                                longPeriod=self.longPeriod,money=money)
        #self.strat.setUseAdjustedValues(False)
        
        #mid results
        self.initAnalyzer()
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
    def printStats(self):
        """"""        
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
    def run(self):
        result = self.strat.run()
        return result

if __name__ == "__main__": 

    app = QtGui.QApplication(sys.argv)
    #----------------------------------------------------------------------------------------------------
    symbol = '600701'
    instruments = [symbol]
    dataForCandle = dataCenter.getCandleData(symbol = symbol)     
    
    #mid ea01
    money = moneyFixed.moneyFixed()
    money = moneyFirst.moneyFirst()
    '''mid
    mid dataProvider = tushare|yahoo|generic
    mid storageType = csv|mongodb
    mid period 数据类型，D=日k线 W=周 M=月 m5=5分钟 m15=15分钟 m30=30分钟 h1=60分钟，默认为D
    '''    
    ex01 = Expert(toPlot=False,  shortPeriod=20,longPeriod=30, 
                dataProvider = 'tushare',storageType = 'mongodb',period = 'D',
                instruments=instruments,money = money,
                fromYear = 2014,toYear=2016)
    result01 = ex01.run()
    #mid ea02
    analyzer = Analyzer05(Globals=[]) 

    analyzer.analyze(result01,dataForCandle)

    ex01.printStats()    
    
    
    #mid 3a03
    # ---------------------------------------------------------------------------------------------------
    sys.exit(app.exec_())  
    '''

    money = moneyFixed.moneyFixed()
    ex = Expert(toPlot=True, instrument='000001SZ', shortPeriod=20, 
               longPeriod=40, feedFormat='generic',
               money = money)
    ex.run()

    money = moneyFixed.moneyFixed()
    ex = Expert(toPlot=True, instrument='AAPL', shortPeriod=20, 
               longPeriod=40, feedFormat='yahoo',
               money = money)
    ex.run()
    money = moneyFixed.moneyFixed()
    ex = Expert(toPlot=True, instrument='AAPL', shortPeriod=20, 
               longPeriod=40, feedFormat='yahooCsv',
               money = money)
    ex.run()

    
    money = moneyFixed.moneyFixed()
    ex = Expert(toPlot=True, instrument='600243', shortPeriod=20, 
               longPeriod=40, feedFormat='tushareCsv',
               money = money)
    ex.run()        
    
    '''
