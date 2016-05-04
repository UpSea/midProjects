def onBars(self, bars):
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