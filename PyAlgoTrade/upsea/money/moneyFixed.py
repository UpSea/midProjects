# -*- coding: utf-8 -*-
import baseMoney
class moneyFixed(baseMoney.baseMoney):
    def __init__(self):
        self.init = 100000
    def getShares(self):        
        money = self.init
        return money