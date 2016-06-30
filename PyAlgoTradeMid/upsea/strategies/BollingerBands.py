# -*- coding: utf-8 -*-
from pyalgotrade import strategy
from pyalgotrade.technical import bollinger

class BBands(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, bBandsPeriod):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.__instrument = instrument
        self.__bbands = bollinger.BollingerBands(feed[instrument].getCloseDataSeries(), bBandsPeriod, 2)

    def getBollingerBands(self):
        return self.__bbands

    def onBars(self, bars):
        lower = self.__bbands.getLowerBand()[-1]
        upper = self.__bbands.getUpperBand()[-1]
        if lower is None:
            return
        broker = self.getBroker()
        postions = broker.getPositions()
        orders = broker.getActiveOrders()
        
        
        shares = self.getBroker().getShares(self.__instrument)
        bar = bars[self.__instrument]
        if shares == 0 and bar.getClose() < lower:
            sharesToBuy = int(self.getBroker().getCash(False) / bar.getClose()*0.1)
            self.marketOrder(self.__instrument, sharesToBuy)
        elif shares > 0 and bar.getClose() > upper:
            self.marketOrder(self.__instrument, -1*shares)
            for (d,x) in postions.items():
                if(d == self.__instrument):
                    print "instrument:"+d+",postion:"+str(x)            
