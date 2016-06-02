# -*- coding: utf-8 -*-
from pyalgotrade import strategy
from pyalgotrade.technical import ma
from pyalgotrade.technical import cross
from pyalgotrade.dataseries import SequenceDataSeries
from pyalgotrade.dataseries import DEFAULT_MAX_LEN

class DMACrossOver(strategy.BacktestingStrategy):
    def __init__(self, feed = None, instrument = '',shortPeriod =  0,longPeriod = 0,money = None,longAllowed=True,shortAllowed=True):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.__instrument = instrument
        self.__longPosition = None
        self.__shortPosition = None
        self.__position = SequenceDataSeries(maxLen=30 * DEFAULT_MAX_LEN)
        self.money = money
        self.longAllowed = True
        self.shortAllowed = True        
        #mid 计算ma将使用当天的收盘价格计算
        dataSeries = feed[instrument]
        priceSeries = dataSeries.getPriceDataSeries()
        openSeries = dataSeries.getOpenDataSeries()
        closeSeries = dataSeries.getOpenDataSeries()
        prices = closeSeries
        
        self.__sma = ma.SMA(prices, shortPeriod)
        self.__lma = ma.SMA(prices,longPeriod)
        
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
                currentTime = self.getCurrentDateTime()
                self.__position.appendWithDateTime(currentTime,share)                
                #self.__position.append(share)

        else:
            currentTime = self.getCurrentDateTime()
            self.__position.appendWithDateTime(currentTime,share)               
            #self.__position.append(share)
    def getTest(self):
        return self.__position    
    def getSMA(self):
        return self.__sma
    def getLMA(self):
        return self.__lma
    def onEnterOk(self, position):
        print
        execInfo = position.getEntryOrder().getExecutionInfo()        
        if isinstance(position, strategy.position.LongPosition):
            self.info("onEnterOK().ExecutionInfo: %s,OPEN LONG %.2f at $%.2f" % (execInfo.getDateTime(),execInfo.getQuantity(),execInfo.getPrice()))                    
        elif isinstance(position, strategy.position.ShortPosition):
            self.info("onEnterOK().ExecutionInfo: %s,OPEN SHORT %.2f at $%.2f" % (execInfo.getDateTime(),execInfo.getQuantity(),execInfo.getPrice()))     
        print
    def onEnterCanceled(self, position):
        if isinstance(position, strategy.position.LongPosition):
            self.__longPosition = None
            self.info("onEnterCanceled().ExecutionInfo: %s,OPEN LONG %.2f at $%.2f" % (execInfo.getDateTime(),execInfo.getQuantity(),execInfo.getPrice()))                                
        elif isinstance(position, strategy.position.ShortPosition):
            self.__shortPosition = None
            self.info("onEnterCanceled().ExecutionInfo: %s,OPEN SHORT %.2f at $%.2f" % (execInfo.getDateTime(),execInfo.getQuantity(),execInfo.getPrice()))                                
    def onExitOk(self, position):        
        print
        execInfo = position.getExitOrder().getExecutionInfo()        
        if isinstance(position, strategy.position.LongPosition):
            self.__longPosition = None
            self.info("onExitOk().ExecutionInfo: %s,CLOSE LONG %.2f at $%.2f" % (execInfo.getDateTime(),execInfo.getQuantity(),execInfo.getPrice()))                    
        elif isinstance(position, strategy.position.ShortPosition):
            self.__shortPosition = None
            self.info("onExitOk().ExecutionInfo: %s,CLOSE SHORT %.2f at $%.2f" % (execInfo.getDateTime(),execInfo.getQuantity(),execInfo.getPrice()))                    
        print    
    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        if isinstance(position, strategy.position.LongPosition):
            self.__longPosition = None
        elif isinstance(position, strategy.position.ShortPosition):
            self.__shortPosition = None
    def onBars(self, bars):
        '''mid
        此处是onBars，这个和zipline的概念完全不同
        zipline中，需要覆写的是handle_data，这个东西是个tick概念，所以没有OHLC的，只是个price
        PAT中，每次onBars，都会传入一个newbar的OHLC，此时，要如何按这个OHLC决策，全由你
        依据OHLC做完决策后，可以发送交易指令：
        * Order.Type.MARKET
        * Order.Type.LIMIT
        * Order.Type.STOP
        * Order.Type.STOP_LIMIT
        1.市价单，依据下一个bar的openPrice执行命令：
            self.enterLong()
        2.限价单
        3.止损单市价单
        4.止损限价单
        
        当前似乎没有止盈单
        
        在均线策略中，应该在每个newbar到来时，按closePrice的均线计算指标值，然后发送市价单
        1.每个newbar按close价格计算指标，并在下一个bar按open成交
        2.每个newbar按open价格计算指标，并在此newbar按open成交
        以上1,2的计算逻辑是一致的。如果当前bar的close和下一个bar的open相差无几时，两种算法的回测结果也应相差无几
        '''
        # If a position was not opened, check if we should enter a long position.
        #print 'onBars'        
        #shares = int(self.getBroker().getCash() * 0.9 / bars[self.__instrument].getPrice())
        pLong,pShort = 0,0
        if(self.__longPosition is not None):
            pLong = self.__longPosition.getShares()
        if(self.__shortPosition is not None):
            pShort = self.__shortPosition.getShares()
        
        
        bar = bars[self.__instrument]
        pOpen = bar.getOpen()
        pHigh = bar.getHigh()
        pLow = bar.getLow()
        pClose = bar.getClose()
        pPrice = bar.getPrice()
        
        #self.info('price:%.3f,open:%.2f,high:%.2f,low:%.2f,close:%.2f'%(pPrice,pOpen,pHigh,pLow,pClose))
        #self.info('long:%.2f#short:%.2f'%(pLong,pShort))
        
        self.recordPositions()            
        
        if(self.longAllowed):
            if self.__longPosition is None:
                #mid 无多仓，检查是否需要开多仓
                if cross.cross_above(self.__sma, self.__lma) > 0:
                    # Enter a buy market order. The order is good till canceled.
                    shares = self.money.getShares()                    
                    self.info("onBars().Status info,before enterLong(), LONG POSITION to open %.2f" % (shares))                                    
                    self.__longPosition = self.enterLong(self.__instrument, shares, True)
            elif not self.__longPosition.exitActive():
                #mid 有多仓，检查是否需要平仓
                if(cross.cross_below(self.__sma, self.__lma) > 0):
                    self.info("onBars().Status info,before exitMarket(), LONG POSITION to close %.2f" % (self.__longPosition.getShares()))                                    
                    self.__longPosition.exitMarket()
        
        if(self.shortAllowed):
            # If a position was not opened, check if we should enter a long position.
            if self.__shortPosition is None:
                if cross.cross_below(self.__sma, self.__lma) > 0:
                    # Enter a buy market order. The order is good till canceled.
                    shares = self.money.getShares()
                    self.info("onBars().Status info,before enterShort(), SHORT POSITION to open %.2f" % (shares))                                    
                    self.__shortPosition = self.enterShort(self.__instrument, shares, True)
            # Check if we have to exit the position.
            elif not self.__shortPosition.exitActive():
                if(cross.cross_above(self.__sma, self.__lma) > 0):
                    self.info("onBars().Status info,before exitMarket(), SHORT POSITION to close %.2f" % (self.__shortPosition.getShares()))                                    
                    self.__shortPosition.exitMarket()    
