# -*- coding: utf-8 -*-
import baseMoney
class moneyFirst(baseMoney.baseMoney):
    def __init__(self):
        self.initPortfolio = 0
        self.initPortfolioCash = 0
        self.portfolioIndex = 0
        
        self.initSubPortfolio = 0
        self.initSubPortfolioCash = 0
        self.subPortfolioIndex = 0
        
        self.curSubPortfolio = 0
    def getShares(self,strat = None):   
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