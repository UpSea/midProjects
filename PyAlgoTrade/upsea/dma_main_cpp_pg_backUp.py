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
                 storageType = 'mongodb',period = 'D',timeFrom = None,timeTo=None,money = None):
        self.timeFrom = timeFrom
        self.timeTo = timeTo
        self.instrument = instruments[0]
        self.shortPeriod = shortPeriod
        self.longPeriod = longPeriod
        self.toPlot = toPlot
        
        #mid data
        self.dataCenter = dataCenter.dataCenter()           
        feeds = self.dataCenter.getFeedsForPAT(dataProvider = dataProvider,storageType = storageType,instruments = instruments,period=period,
                                                   timeTo = timeTo,timeFrom=timeFrom)
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
    
    def run(self):
        result = self.strat.run()
        return result
def run(timeFrom = '',timeTo = '',symbol = '',dataProvider = '',storageType = '',period = '',money = None,shortPeriod=10,longPeriod=20):
    #mid ea01    
    timeFrom = dt.datetime.strptime(timeFrom,'%Y-%m-%d %H:%M:%S')    
    timeTo = dt.datetime.strptime(timeTo,'%Y-%m-%d %H:%M:%S')      
    
    if(money == 'moneyFixed'):
        money = moneyFixed.moneyFixed()
    elif(money == 'moneyFirst'):
        money = moneyFirst.moneyFirst()
    elif(money == 'moneySecond'):
        money = moneySecond.moneySecond()
    instruments = [symbol]

  


    ex01 = Expert(toPlot=False,  shortPeriod=shortPeriod,longPeriod=longPeriod, 
                  dataProvider = dataProvider,storageType = storageType,period = period,
                  instruments=instruments,money = money,
                  timeFrom = timeFrom,timeTo=timeTo)
    startRun = time.clock()
    result01 = ex01.run()
    endRun = time.clock()

    #mid ea02
    startAnalize = time.clock()    
    if(False):
        analyzer = Analyzer05(Globals=[]) 
        dataForCandle = dataCenter.getCandleData(dataProvider = dataProvider,dataStorage = storageType,dataPeriod = period,symbol = symbol,dateStart=timeFrom,dateEnd = timeTo)     
        analyzer.analyze(result01,dataForCandle)
    endAnalize = time.clock()
    result02 = ex01.summary()    
    #ex01.detail()
    print
    #print "total bars: %f" % len(dataForCandle)
    print "run time: %f s" % (endRun - startRun)
    print "analize time: %f s" % (endAnalize - startAnalize)
    print         
    
    return result02
    
if __name__ == "__main__": 
    #app = QtGui.QApplication(sys.argv)
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
    timeFrom = '2016-05-05 00:00:00'
    timeTo = '2016-05-30 00:00:00'
    startRun = time.clock()
    
    timeStampFrom = int(time.mktime(time.strptime(timeFrom, "%Y-%m-%d %H:%M:%S")))
    timeStampTo   = int(time.mktime(time.strptime(timeTo, "%Y-%m-%d %H:%M:%S")))    
    print timeFrom,timeTo
    i = 5
    interval = (timeStampTo - timeStampFrom)/i
    
    start = timeStampFrom
    results = []
    for index in range(i):
        end = start + interval
        
        timeStart = dt.datetime.utcfromtimestamp(start).strftime("%Y-%m-%d %H:%M:%S")
        timeEnd = dt.datetime.utcfromtimestamp(end).strftime("%Y-%m-%d %H:%M:%S")
        
        result = run(timeFrom = timeStart,timeTo = timeEnd,symbol = 'XAUUSD',money = 'moneySecond',dataProvider = 'mt5',storageType = 'csv',period = 'm5',shortPeriod=10,longPeriod=20)    
        results.append(result)
        
        start = end    
        
        
    for result in results:
        print result
        


    endRun = time.clock()
    print "run time: %f s" % (endRun - startRun)           
        
        
    #sys.exit(app.exec_())  
