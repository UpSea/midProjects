# -*- coding: utf-8 -*-
import baseMoney
class moneyFirst(baseMoney.baseMoney):
    def __init__(self):
        self.init = 30000
        self.i = 0
    def getShares(self):        
        money = self.init + self.i*1000
        self.i = self.i + 1
        return money