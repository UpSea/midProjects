# -*- coding: utf-8 -*-
from pyalgotrade import strategy
from pyalgotrade.technical import ma
from pyalgotrade.technical import cross
from pyalgotrade.dataseries import SequenceDataSeries
from pyalgotrade.dataseries import DEFAULT_MAX_LEN
import pandas as pd

class DMACrossOver(strategy.BacktestingStrategy):
 def __init__(self, feed = None, instrument = '',shortPeriod =  0,longPeriod = 0,money = None,longAllowed=True,shortAllowed=True):
  strategy.BacktestingStrategy.__init__(self, feed)

  self.position_cost = 0  #mid init position value
  
  mid_DEFAULT_MAX_LEN = 10 * DEFAULT_MAX_LEN
  self.__instrument = instrument
  self.__longPosition = None
  self.__shortPosition = None
  
  self.__position_volume = SequenceDataSeries(maxLen = mid_DEFAULT_MAX_LEN)       #mid 当前持有头寸数量
  self.__position_cost = SequenceDataSeries(maxLen = mid_DEFAULT_MAX_LEN)  #mid 当前持有头寸开仓成本
  self.__position_pnl = SequenceDataSeries(maxLen = mid_DEFAULT_MAX_LEN)   #mid 当前持有头寸价值
  self.__portfolio_value = SequenceDataSeries(maxLen = mid_DEFAULT_MAX_LEN)
  self.__buy = SequenceDataSeries(maxLen = mid_DEFAULT_MAX_LEN)
  self.__sell = SequenceDataSeries(maxLen = mid_DEFAULT_MAX_LEN)
  
  
  self.__buySignal = False
  self.__sellSignal = False
  self.money = money
  self.longAllowed = True
  self.shortAllowed = True        
  #mid 计算ma将使用当天的收盘价格计算
  #mid 1)
  dataSeries = feed[instrument]
  dataSeries.setMaxLen(mid_DEFAULT_MAX_LEN)
  closeSeries = dataSeries.getOpenDataSeries()
  #mid 2)
  prices = closeSeries
  prices.setMaxLen(mid_DEFAULT_MAX_LEN)
  #mid 3)
  self.__sma = ma.SMA(prices, shortPeriod,maxLen=mid_DEFAULT_MAX_LEN)
  self.__lma = ma.SMA(prices,longPeriod,maxLen=mid_DEFAULT_MAX_LEN)

  self.i = 0
 def getAssetStructure(self):
  #mid --------------------------------
  #mid 当前账户资产结构如下方式获取
  #mid Long 和 Short不会同时存在
  #mid 在开仓前，若有反向持仓，则此过程查询并输出已持有的反向持仓
  broker = self.getBroker()
  portfolio_value = broker.getEquity()
  cash = broker.getCash()
  if self.__shortPosition is not None or self.__longPosition is not None:
   bars = self.getFeed().getCurrentBars()  
   
   positions = broker.getPositions()
   
   positionsOpenValue = {}
   positionsCloseValue = {}
   for key,value in positions.items():
    print "key:"+key+",value:"+str(value)
    bar = bars.getBar(key)
    openPrice = bar.getOpen() 
    closePrice = bar.getClose()
    share = broker.getShares(key)
    positionsOpenValue[key] = openPrice*share
    positionsCloseValue[key] = closePrice*share
    
   print 
   print 'current bar asset structure'
   print 'open cash %2.f.' % (cash)
   for key,value in positionsOpenValue.items():
    print "key:"+key+",value:"+str(value)
   print 'close cash %2.f.' % (cash)
   for key,value in positionsCloseValue.items():
    print "key:"+key+",value:"+str(value)    
   print 'portfolio:%2.f' % (portfolio_value)
   
   return portfolio_value,cash,sum(positionsCloseValue.values())
  return portfolio_value,cash,0
 def recordPositions(self):
  # record position      
  #######################################################################
  broker = self.getBroker()
  position = broker.getPositions()                   #mid position is dict of share
  share = broker.getShares(self.__instrument)        #mid position is dict of share
  lastPrice = self.getLastPrice(self.__instrument)  
  portfolio_value = broker.getEquity()               #mid 按close价格计算的权益
  cash = broker.getCash()
  
  position_value = portfolio_value - cash
  
  position_pnl = position_value - self.position_cost
  
  print
  print 'cash: %.2f' %(cash)
  print 'position value: %.2f' % (portfolio_value - cash)
  print 'mid calc: %.2f' %(lastPrice*share+cash)
  print 'broker returned: %.2f' %(portfolio_value)
  
  
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
    self.__position.appendWithDateTime(currentTime,abs(share))                
    #self.__position.append(share)

  else:
   currentTime = self.getCurrentDateTime()
   
   self.__position_volume.appendWithDateTime(currentTime,abs(share))  
   
   self.__position_cost.appendWithDateTime(currentTime,abs(self.position_cost))
   
   self.__position_pnl.appendWithDateTime(currentTime,position_pnl)
   
   self.__portfolio_value.appendWithDateTime(currentTime,portfolio_value)  
   self.__buy.appendWithDateTime(currentTime,self.__buySignal)              
   self.__sell.appendWithDateTime(currentTime,self.__sellSignal) 
 def getInstrument(self):
  return self.__instrument
 def getPortfolio(self):
  return self.__portfolio_value
 def getPositionVolume(self):
  return self.__position_volume    
 def getPositionCost(self):
  return self.__position_cost
 def getPositionPnl(self):
  return self.__position_pnl 
 def getSMA(self):
  return self.__sma
 def getLMA(self):
  return self.__lma
 def getBuy(self):
  return self.__buy
 def getSell(self):
  return self.__sell
 def onEnterOk(self, position):
  execInfo = position.getEntryOrder().getExecutionInfo()   
  portfolio = self.getResult()
  cash = self.getBroker().getCash() 

  '''mid
  以下两种方法都是为了计算持仓成本
  由于getEquity()返回的是依据当日close价格计算出来的权益
  所以，这个值不能作为持仓成本
  持仓成本需要以onEnterOk时bar的open价格计算
  所以应使用第二种算法
  由于经常有跳开现象，所以依据bar(n-1).close发出的market order，
  在bar(n).open执行时通常会有gap出现，表现在position_cost图上时就是持有成本离计划成本会有跳口，
  '''
  if(False):#mid two methods to cacl cost.
   portfolio_value = self.getBroker().getEquity()
   self.position_cost = portfolio_value - cash  
  else:
   feed = self.getFeed()
   bars = feed.getCurrentBars()
   bar = bars.getBar(self.__instrument)
   openPrice = bar.getOpen()   
   closePrice = self.getLastPrice(self.__instrument) #mid lastPrice == closePrice
   share = self.getBroker().getShares(self.__instrument)
   self.position_cost = openPrice*share

  self.info("onEnterOk().current available cash: %.2f,portfolio: %.2f." % (cash,portfolio))
  if isinstance(position, strategy.position.LongPosition):
   self.info("onEnterOK().ExecutionInfo: %s,OPEN LONG %.2f at $%.2f" 
             % (execInfo.getDateTime(),execInfo.getQuantity(),execInfo.getPrice())) 
  elif isinstance(position, strategy.position.ShortPosition):
   self.info("onEnterOK().ExecutionInfo: %s,OPEN SHORT %.2f at $%.2f" 
             % (execInfo.getDateTime(),execInfo.getQuantity(),execInfo.getPrice()))     
   
   
   
 def onEnterCanceled(self, position):
  self.info("onEnterCanceled().current available cash: %.2f." % (self.getBroker().getCash()))
  if isinstance(position, strategy.position.LongPosition):
   self.__longPosition = None
   self.info("onEnterCanceled().OPEN LONG cancled.")                                
  elif isinstance(position, strategy.position.ShortPosition):
   self.__shortPosition = None
   self.info("onEnterCanceled().OPEN SHORT cancled.")
 def onExitOk(self, position):        
  execInfo = position.getExitOrder().getExecutionInfo()     
  portfolio = self.getResult()
  cash = self.getBroker().getCash()
  self.info("onExitOk().current available cash: %.2f,portfolio: %.2f." % (cash,portfolio))

  if isinstance(position, strategy.position.LongPosition):
   self.__longPosition = None
   self.info("onExitOk().ExecutionInfo: %s,CLOSE LONG %.2f at $%.2f" 
             % (execInfo.getDateTime(),execInfo.getQuantity(),execInfo.getPrice()))                    
  elif isinstance(position, strategy.position.ShortPosition):
   self.__shortPosition = None
   self.info("onExitOk().ExecutionInfo: %s,CLOSE SHORT %.2f at $%.2f" 
             % (execInfo.getDateTime(),execInfo.getQuantity(),execInfo.getPrice()))                    
 def onExitCanceled(self, position):
  # If the exit was canceled, re-submit it.
  if isinstance(position, strategy.position.LongPosition):
   self.__longPosition = None
  elif isinstance(position, strategy.position.ShortPosition):
   self.__shortPosition = None
 def logInfo(self,bars = None):
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

  self.info('logInfo().price:%.3f,open:%.2f,high:%.2f,low:%.2f,close:%.2f'%(pPrice,pOpen,pHigh,pLow,pClose))
  #self.info('long:%.2f#short:%.2f'%(pLong,pShort))        
 def run(self):
  strategy.BacktestingStrategy.run(self)

  sma = self.getSMA()
  lma = self.getLMA()
  buy = self.getBuy()
  sell = self.getSell()
  
  portfolio_value = self.getPortfolio()
  
  position_volume = self.getPositionVolume()
  position_cost = self.getPositionCost()
  position_pnl = self.getPositionPnl()
  
  result = pd.DataFrame({'position_volume':list(position_volume),'position_cost':list(position_cost),'position_pnl':list(position_pnl),'short_ema':list(sma),'long_ema':list(lma),
                         'buy':list(buy),'sell':list(sell),'portfolio_value':list(portfolio_value)},
                        columns=['position_volume','position_cost','position_pnl','short_ema','long_ema','buy','sell','portfolio_value'],
                        index=position_volume.getDateTimes())        
  return result
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
  self.__buySignal,self.__sellSignal = False,False
  # mid 1)close
  if(self.longAllowed):
   if self.__longPosition is not None and not self.__longPosition.exitActive():
    #mid 有多仓，检查是否需要平仓
    if(cross.cross_below(self.__sma, self.__lma) > 0):
     print
     self.info("onBars().Status info,before exitMarket(), LONG POSITION to close %.2f" 
               % (self.__longPosition.getShares()))                                    
     self.__longPosition.exitMarket()
  if(self.shortAllowed):
   if self.__shortPosition is not None and not self.__shortPosition.exitActive():
    if(cross.cross_above(self.__sma, self.__lma) > 0):
     print
     self.info("onBars().Status info,before exitMarket(), SHORT POSITION to close %.2f" 
               % (self.__shortPosition.getShares()))  
     self.__shortPosition.exitMarket()    

  # mid 2)open
  if(self.longAllowed):
   if self.__longPosition is None:
    #mid 无多仓，检查是否需要开多仓
    if cross.cross_above(self.__sma, self.__lma) > 0:
     # Enter a buy market order. The order is good till canceled.
     shares = self.money.getShares(strat = self)                    
     self.info("onBars().Status info,before enterLong(), LONG POSITION to open %.2f,need amount: %.2f,available amount: %.2f." % 
               (shares,shares*self.getLastPrice(self.__instrument),self.getBroker().getCash() ))                                    
     self.__longPosition = self.enterLong(self.__instrument, shares, True)
     self.__buySignal = True   
  if(self.shortAllowed):
   if self.__shortPosition is None:
    if cross.cross_below(self.__sma, self.__lma) > 0:
     # Enter a buy market order. The order is good till canceled.
     shares = self.money.getShares(strat = self)
     self.info("onBars().Status info,before enterShort(), SHORT POSITION to open %.2f,need amount: %.2f,available amount: %.2f." % 
               (shares,shares*self.getLastPrice(self.__instrument),self.getBroker().getCash() ))                                    
     self.__shortPosition = self.enterShort(self.__instrument, shares, True)
     self.__sellSignal = True

  self.recordPositions()            