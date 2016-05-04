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
        self.initInvest = int(self.getBroker().getCash() * 0.01)
        self.subPortfolio = 0
        self.threshold = 0
    def getSMA(self):
        return self.__sma
    def getLMA(self):
        return self.__lma
    def getPositionInfo(self,position):
        print position.getActiveOrders()
        print position.getAge()
        print position.getInstrument()
        print position.getLastPrice()
        print position.getNetProfit()
        print position.getPnL()
        print position.getQuantity()
        print position.getReturn()
        print position.getShares()
        print position.getUnrealizedNetProfit()
        print position.getUnrealizedReturn()
    def onEnterCanceled(self, position):
        self.__position = None
    def onExitOk(self, position):
        execInfo = position.getExitOrder().getExecutionInfo()
        self.info("SELL at $%.2f" % (execInfo.getPrice()))
        self.stratInfo()
        self.getPositionInfo(position)
        self.__position = None
    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        self.__position.exitMarket()    
    def stratInfo(self,bars = None):        
        broker = self.getBroker()
        postions = broker.getPositions()
        orders = broker.getActiveOrders()
        
        shares = self.getBroker().getShares(self.__instrument)
        
        print
        if (bars is not None):
            bar = bars[self.__instrument]
            print "Time:%s.Close:%.4f." % (bar.getDateTime(), bar.getClose())        
        print "cash:%.4f" % (broker.getCash())
        print "equity:%.4f" % (broker.getEquity())
        print "positions:"
        for (d,x) in postions.items():
            if(d == self.__instrument):
                print "    instrument:"+d+",postion:"+str(x)          
    def getShares(self,bars):
        if (self.subPortfolio >= self.threshold):
            self.initInvest = int(self.getBroker().getCash() * 0.01)
            shares = int(self.initInvest / bars[self.__instrument].getPrice())
        else:
            shares = int(self.initInvest / bars[self.__instrument].getPrice())            
        return shares
    def getSignalSell(self):
        return cross.cross_below(self.__sma, self.__lma) > 0
    def getSignalBuy(self):
        return cross.cross_above(self.__sma, self.__lma) > 0
    def onBars(self, bars):
        # If a position was not opened, check if we should enter a long position.
        self.stratInfo(bars)
        if self.__position is None:
            signalBuy = self.getSignalBuy()
            if signalBuy:
                shares = self.getShares(bars)
                # Enter a buy market order. The order is good till canceled.
                self.__position = self.enterLong(self.__instrument, shares, True)
        # Check if we have to exit the position.
        elif not self.__position.exitActive():
            signalSell = self.getSignalSell()
            if signalSell:
                self.__position.exitMarket()
        self.stratInfo(bars)