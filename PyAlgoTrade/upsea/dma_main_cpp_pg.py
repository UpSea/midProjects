# -*- coding: utf-8 -*-
import os,sys
from PyQt4 import QtGui,QtCore
import pandas as pd
import datetime as dt
import time as time
#mid 1)dataCenter
dataRoot = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,os.pardir,'histdata'))        
sys.path.append(dataRoot)        
import dataCenter as dataCenter 
#mid 2)graphOutput
xpower = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,os.pardir,'histdataUI'))
sys.path.append(xpower)        
from Analyzers.Analyzer05 import Analyzer05#from BollingerBands import BBands
#mid 3)strategy
import strategies.dma_crossover as dma_crossover
#mid 4)money
import money.moneyFixed as moneyFixed
import money.moneyFirst as moneyFirst
import money.moneySecond as moneySecond

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
        
        analyzer = Analyzer05(Globals=[]) 
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
class eaController():
    def __init__(self,timeFrom,timeTo,phases):
        self.timeFrom = timeFrom
        self.timeTo = timeTo
        self.phases = phases
    def run(self):
        ea = self.getEa()
        results = self.runByPhase(self.timeFrom,self.timeTo,self.phases,ea)
    
    
        print  "------------------------"
        print self.timeFrom,' to ',self.timeTo
        print  "------------------------"

        for result in results:
            print result         
    def runByPhase(self,timeFrom,timeTo,phases,ea):
        timeStampFrom = int(time.mktime(time.strptime(timeFrom, "%Y-%m-%d %H:%M:%S")))
        timeStampTo   = int(time.mktime(time.strptime(timeTo, "%Y-%m-%d %H:%M:%S")))    
        print timeFrom,timeTo
        
        interval = (timeStampTo - timeStampFrom)/phases
        
        start = timeStampFrom
        results = []
        for index in range(phases):
            end = start + interval
            
            timeFrom = dt.datetime.utcfromtimestamp(start).strftime("%Y-%m-%d %H:%M:%S")
            timeTo = dt.datetime.utcfromtimestamp(end).strftime("%Y-%m-%d %H:%M:%S")
            
            
            timeFrom = dt.datetime.strptime(timeFrom,'%Y-%m-%d %H:%M:%S')    
            timeTo = dt.datetime.strptime(timeTo,'%Y-%m-%d %H:%M:%S')          
    
            result01 = ea.run(timeFrom = timeFrom,timeTo = timeTo)
            
            
            result02 = ea.summary() 
            
            results.append(result02)
            
            start = end  
        return results
    def getEa(self):    
        '''mid
        mid dataProvider = tushare|mt5|yahoo|generic
        mid storageType = csv|mongodb
        mid period 数据类型，D=日k线 W=周 M=月 m1=1分钟 m5=5分钟 m15=15分钟 m30=30分钟 h1=60分钟，默认为D
        
        money = 'moneyFixed'
        money = 'moneyFirst'
        money = 'moneySecond' 
        '''       
        #run(timeFrom = '2016-05-08 00:00:00',timeTo = '2016-05-30 00:00:00',symbol = '000099',money = 'moneyFixed',dataProvider = 'tushare',storageType = 'csv',period = 'D',shortPeriod=10,longPeriod=20)
        #run(timeFrom = '2016-05-08 00:00:00',timeTo = '2016-05-30 00:00:00',symbol = 'XAUUSD',money = 'moneyFirst',dataProvider = 'mt5',storageType = 'mongodb',period = 'm15',shortPeriod=10,longPeriod=20)    
        #run(timeFrom = '2016-05-08 00:00:00',timeTo = '2016-05-30 00:00:00',symbol = '600028',money = 'moneySecond',dataProvider = 'tushare',storageType = 'csv',period = 'h1',shortPeriod=10,longPeriod=20)    
        
        instruments = ['XAUUSD']
        #mid money
        #money = moneyFixed.moneyFixed()
        #money = moneyFirst.moneyFirst()
        money = moneySecond.moneySecond()  
            
        ea = Expert(toPlot=False,  shortPeriod=10,longPeriod=20, 
                      dataProvider = 'mt5',storageType = 'csv',period = 'm5',
                      instruments=instruments,money = money)    
        return ea        
if __name__ == "__main__": 
    app = QtGui.QApplication(sys.argv)    
    startRun = time.clock()
    
    eaController('2016-05-05 00:00:00', '2016-05-30 00:00:00', 5).run()
    
    endRun = time.clock()
    print "run time: %f s" % (endRun - startRun)       
    sys.exit(app.exec_())  
