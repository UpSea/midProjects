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
        self.portfolioIndex = 0     #mid 总投资次数序号        
        self.initRisk = 0.60        #mid 风险系数
        '''
        设定初始投资额
        '''
    def getShares(self,strat = None):   
        curClosePrice = strat.getLastPrice(strat.getInstrument())
        
        strat.info(('moneyFirst.getShare().price:%.3f'%(curClosePrice)))
        if(self.portfolioIndex == 0):
            '''mid
            由于money是在expert中生成，却是在在与其平级的同样在expert中生成的strategy中调用，
            所以，在money.__init__中是不能调用（至少目前如此，以后或许可调整）
            如此，只能在此处，依据strat参数进行初始化
            '''
            #mid 初始总资产 = 初始总资产中现金数额 + 仓位价值，这几个值作为常量保存初始值
            self.initPortfolio ,self.initCash,positions_closeValue = strat.getAssetStructure()

            #mid 确定初始仓位价值
            self.initSubPortfolio = self.initPortfolio
            
            #mid 当前子投资初始仓位，当前仓位，总是用于子投资计量
            self.initSubPositionCost = self.initSubPortfolio * self.initRisk
            self.curPositionCost =  self.initSubPositionCost
            #mid 自投资序号
            self.subPortfolioIndex = 0
            
            shares = (self.curPositionCost/curClosePrice)
        else:
            curPortfolio ,curCash,curPositions_closeValue = strat.getAssetStructure()

            #mid 如果当前权益大于当前子投资初始价值，开始新的一轮投资
            if(curPortfolio > self.initSubPortfolio):
                #mid 新的循环计数开始
                self.subPortfolioIndex = 0
                #mid 新的循环的初始权益价值
                self.initSubPortfolio = curPortfolio
                #mid 新的循环的初始仓位价值                
                self.initSubPositionCost = self.initSubPortfolio * self.initRisk
                #mid 新的循环的当前仓位价值
                self.curPositionCost = self.initSubPositionCost
            else:
                self.subPortfolioIndex = self.subPortfolioIndex + 1
                if(self.subPortfolioIndex<=20):
                    self.curPositionCost = self.initSubPositionCost * 1
                elif(self.subPortfolioIndex<=40):
                    self.curPositionCost = self.initSubPositionCost * 1
                elif(self.subPortfolioIndex<=60):
                    self.curPositionCost = self.initSubPositionCost * 1.3
                else:
                    self.curPositionCost = self.initSubPositionCost * 1.3

                
            shares = (self.curPositionCost/curClosePrice)
                
        self.portfolioIndex = self.portfolioIndex + 1
        
        
        
        print "portfolioIndex:%d,subPortfolioIndex:%d,curPositionCost:%.2f,shares to open:%.2f" % (self.portfolioIndex,
                                                                                                        self.subPortfolioIndex,
                                                                                                        self.curPositionCost,
                                                                                                        shares)
        return shares