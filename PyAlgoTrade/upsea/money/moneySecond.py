# -*- coding: utf-8 -*-
import baseMoney
class moneySecond(baseMoney.baseMoney):
    def __init__(self):
        '''mid
        回测过程中，关于账户状况，只有两个数据可以获取：
        1.账户权益价值
        2.账户现金资产价值
        权益价值 = 现金资产价值 + 非现金资产价值
        非现金资产包括账户中持有的所有头寸的价值

        买入时：
        现金减少
        购入资产增加，资产价值以正值表示
        1000现金，买入400 XAUUSD
	1000 = 600现金 + 400 XAUUSD
        卖出时：
	现金增加
	卖出资产减少，资产价值以负值表示
	1000现金，卖出400 XAUUSD
	1000 = 1400 现金 – 400 XAUUSD
        
        portfolio_value = strat.getBroker().getEquity()
        cash = strat.getBroker().getCash()
        feed = self.getFeed()
        bars = feed.getCurrentBars()
        bar = bars.getBar(self.__instrument)
        openPrice = bar.getOpen()   
        closePrice = self.getLastPrice(self.__instrument) #mid lastPrice == closePrice
        share = self.getBroker().getShares(self.__instrument)
        self.position_cost = openPrice*share
        买入卖出的资产平衡公式统一如下：
        
        '''
        self.initPortfolio = 0
        self.initPortfolioCash = 0
        self.portfolioIndex = 0
        
        self.initSubPortfolio = 0
        self.initSubPortfolioCash = 0
        self.subPortfolioIndex = 0
        
        self.curSubPortfolio = 0
    def getShares(self,strat = None):   
        portfolio_value,cash,positions_closeValue = strat.getAssetStructure()
        fasdfadf
        curClosePrice = strat.getLastPrice(strat.getInstrument())
        strat.info(('moneyFirst.getShare().price:%.3f'%(curClosePrice)))
        self.curSubPortfolio = strat.getResult()
        
        if(self.portfolioIndex == 0):
            self.initPortfolio = strat.getBroker().getCash()
            self.initPortfolioCash = self.initPortfolio * 0.40
            
            self.initSubPortfolio = self.initPortfolio
            self.initSubPortfolioCash = self.initPortfolioCash
            self.subPortfolioIndex = 1
            shares = int(self.initPortfolioCash/curClosePrice)
        else:
            if(self.curSubPortfolio > self.initSubPortfolio):
                self.subPortfolioIndex = 0
                self.initSubPortfolioCash = self.initPortfolioCash
            else:
                self.subPortfolioIndex = self.subPortfolioIndex + 1
                
            shares = int ((self.initSubPortfolioCash / curClosePrice)*(100 + self.subPortfolioIndex*2) / 100.00)

        self.portfolioIndex = self.portfolioIndex + 1
        
        
        
        print "portfolioIndex:%d,subPortfolioIndex:%d,curSubPortfolio:%.2f,shares to open:%.2f,initPortfolioCash:%.2f" % (self.portfolioIndex,
                                                                                                        self.subPortfolioIndex,
                                                                                                        self.curSubPortfolio,
                                                                                                        shares,
                                                                                                        self.initPortfolioCash)
        return shares