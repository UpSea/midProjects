from pyalgotrade import strategy
from pyalgotrade.technical import ma
from pyalgotrade.technical import cross
class SMACrossOver(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, shortPeriod,longPeriod):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.__instrument = instrument
        self.__longPosition = None
        self.__shortPosition = None
        # We'll use adjusted close values instead of regular close values.
        self.setUseAdjustedValues(True)
        self.__prices = feed[instrument].getPriceDataSeries()
        self.__sma = ma.SMA(self.__prices, shortPeriod)
        self.__lma = ma.SMA(self.__prices,longPeriod)
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
        longAllowed = True
        shortAllowed = True
        
        shares = int(self.getBroker().getCash() * 0.9 / bars[self.__instrument].getPrice())
        shares = 100
        if(longAllowed):
    
            if self.__longPosition is None:
                if cross.cross_above(self.__sma, self.__lma) > 0:
                    # Enter a buy market order. The order is good till canceled.
                    self.__longPosition = self.enterLong(self.__instrument, shares, True)
            # Check if we have to exit the position.
            elif not self.__longPosition.exitActive() and cross.cross_below(self.__sma, self.__lma) > 0:
                print
                print 'longPosition before closed.'+str(self.__longPosition.getShares())                
                self.__longPosition.exitMarket()
        
        if(shortAllowed):
            # If a position was not opened, check if we should enter a long position.
            if self.__shortPosition is None:
                if cross.cross_below(self.__sma, self.__lma) > 0:
                    # Enter a buy market order. The order is good till canceled.
                    self.__shortPosition = self.enterShort(self.__instrument, shares, True)
            # Check if we have to exit the position.
            elif not self.__shortPosition.exitActive() and cross.cross_above(self.__sma, self.__lma) > 0:
                print
                print 'shortPosition before closed.'+str(self.__shortPosition.getShares())
                self.__shortPosition.exitMarket()    
