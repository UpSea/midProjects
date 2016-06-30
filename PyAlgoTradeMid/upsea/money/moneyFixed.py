# -*- coding: utf-8 -*-
import baseMoney
class moneyFixed(baseMoney.baseMoney):
    def __init__(self):
        self.initCash = 0
        self.openIndex = 0
    def getShares(self,strat = None):   
        curPrice = strat.getLastPrice(strat.getInstrument())
        strat.info(('moneyFixed.getShare().price:%.3f'%(curPrice)))
        
        if(self.openIndex == 0):
            self.initCash = strat.getBroker().getCash()*0.60
            self.openIndex = self.openIndex + 1
            
        #shares = int(self.initCash/curPrice)
        shares = (self.initCash/curPrice)
        print
        print 'initCash:%2.f,curPrice:%2.f' % (self.initCash,curPrice)
        print 'cost:%2.f'%(shares*curPrice)
        return shares