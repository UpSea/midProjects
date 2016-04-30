from pyalgotrade import strategy
from pyalgotrade.technical import ma
from pyalgotrade.technical import cross


class SMACrossOver(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, shortPeriod,longPeriod):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.__instrument = instrument
        self.__position = None
        # We'll use adjusted close values instead of regular close values.
        self.setUseAdjustedValues(True)
        self.__prices = feed[instrument].getPriceDataSeries()
        self.__sma = ma.SMA(self.__prices, shortPeriod)
        self.__lma = ma.SMA(self.__prices,longPeriod)
    def getSMA(self):
        return self.__sma
    def getLMA(self):
        return self.__lma
    def onEnterCanceled(self, position):
        self.__position = None

    def onExitOk(self, position):
        self.__position = None

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        self.__position.exitMarket()
    def outputPositions(self):
        broker = self.getBroker()
        positions = broker.getPositions()
        for (d,x) in positions.items():
            if(d == self.__instrument):
                print "instrument:"+d+",postion:"+str(x)           
    def onBars(self, bars):
        # If a position was not opened, check if we should enter a long position.
           
        
        #shares = position[self.__instrument]
             
        self.outputPositions()
        shares = 100 
        self.__position = self.enterLong(self.__instrument, shares, True)
        if self.__position is not None:
            self.__position.exitMarket()           
        #self.marketOrder(self.__instrument, 1*shares)
        self.outputPositions()
      

        return 
        position =   0
        if self.__position is not None:
            print "Positions: %.2f" % self.__position.getShares()
            position = self.__position.getShares()


        shares = 100 
        if cross.cross_above(self.__sma, self.__lma) > 0 and position <= 0:
            # Enter a buy market order. The order is good till canceled.
            if self.__position is not None:
                self.__position.exitMarket()   
            self.__position = self.enterLong(self.__instrument, shares, True)
        elif cross.cross_below(self.__sma,self.__lma) > 0 and position >= 0:
            if self.__position is not None:
                self.__position.exitMarket()   
            self.__position=self.enterShort(self.__instrument, shares, True)                
            # Check if we have to exit the position.
        #if cross.cross_below(self.__sma, self.__lma) > 0 and position > 0:
            #self.__position.exitMarket()    
        #if cross.cross_above(self.__sma, self.__lma) > 0 and position < 0:
            #self.__position.exitMarket()      
            
        #bar = bars[self.__instrument]
        #print "Time:%s.Close:%.4f." % (bar.getDateTime(), bar.getClose())
