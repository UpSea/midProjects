# -*- coding: utf-8 -*-
from pyalgotrade import strategy
from pyalgotrade.technical import ma
from pyalgotrade.technical import cross
from pyalgotrade.dataseries import SequenceDataSeries

class DMACrossOver(strategy.BacktestingStrategy):
    def __init__(self, feed = None, instrument = '',shortPeriod =  0,longPeriod = 0,money = None,longAllowed=True,shortAllowed=True):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.__instrument = instrument
        self.__longPosition = None
        self.__shortPosition = None
        self.__position = SequenceDataSeries()
        self.money = money
        self.longAllowed = True
        self.shortAllowed = True        
        # We'll use adjusted close values instead of regular close values.
        self.__prices = feed[instrument].getPriceDataSeries()
        self.__sma = ma.SMA(self.__prices, shortPeriod)
        self.__lma = ma.SMA(self.__prices,longPeriod)
        
        self.i = 0
    def recordPositions(self):
        # record position      
        #######################################################################
        broker = self.getBroker()
        share = broker.getShares(self.__instrument)
        position = broker.getPositions()
        curTime = self.getCurrentDateTime()
        if(False):
            yLimit = self.money.getShares()*1.1
            if(self.i==0):
                self.__position.append(yLimit)
                self.i = self.i + 1
            elif(self.i==1):
                self.__position.append(-yLimit)
                self.i = self.i + 1
            else:
                self.__position.append(share)

        else:
            self.__position.append(share)
    def getTest(self):
        return self.__position    
    def getSMA(self):
        return self.__sma
    def getLMA(self):
        return self.__lma
    def onEnterOk(self, position):
        execInfo = position.getEntryOrder().getExecutionInfo()        
        if isinstance(position, strategy.position.LongPosition):
            print 'longPosition opened by broker.'+str(position.getShares())
            self.info("BUY at $%.2f" % (execInfo.getPrice()))                    
        elif isinstance(position, strategy.position.ShortPosition):
            print 'shortPosition opened by broker.'+str(position.getShares())
            self.info("SELL at $%.2f" % (execInfo.getPrice()))                    
    def onEnterCanceled(self, position):
        if isinstance(position, strategy.position.LongPosition):
            self.__longPosition = None
        elif isinstance(position, strategy.position.ShortPosition):
            self.__shortPosition = None
    def onExitOk(self, position):
        if isinstance(position, strategy.position.LongPosition):
            self.__longPosition = None
            print 'longPosiont closed by broker.'+str(position.getShares())
        elif isinstance(position, strategy.position.ShortPosition):
            self.__shortPosition = None
            print 'shortPosition closed by broker.'+str(position.getShares())
    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        if isinstance(position, strategy.position.LongPosition):
            self.__longPosition = None
        elif isinstance(position, strategy.position.ShortPosition):
            self.__shortPosition = None
    def onBars(self, bars):
        # If a position was not opened, check if we should enter a long position.
        #print 'onBars'        
        #shares = int(self.getBroker().getCash() * 0.9 / bars[self.__instrument].getPrice())
        
        self.recordPositions()            
        
        if(self.longAllowed):
    
            if self.__longPosition is None:
                if cross.cross_above(self.__sma, self.__lma) > 0:
                    # Enter a buy market order. The order is good till canceled.
                    shares = self.money.getShares()
                    self.__longPosition = self.enterLong(self.__instrument, shares, True)
            # Check if we have to exit the position.
            elif not self.__longPosition.exitActive() and cross.cross_below(self.__sma, self.__lma) > 0:
                print
                print 'longPosition before closed.'+str(self.__longPosition.getShares())                
                self.__longPosition.exitMarket()
        
        if(self.shortAllowed):
            # If a position was not opened, check if we should enter a long position.
            if self.__shortPosition is None:
                if cross.cross_below(self.__sma, self.__lma) > 0:
                    # Enter a buy market order. The order is good till canceled.
                    shares = self.money.getShares()
                    self.__shortPosition = self.enterShort(self.__instrument, shares, True)
            # Check if we have to exit the position.
            elif not self.__shortPosition.exitActive() and cross.cross_above(self.__sma, self.__lma) > 0:
                print
                print 'shortPosition before closed.'+str(self.__shortPosition.getShares())
                self.__shortPosition.exitMarket()    
