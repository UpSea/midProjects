# -*- coding: utf-8 -*-
import EA.ea_mpl as ea
import os,sys
dataRoot = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir))        
sys.path.append(dataRoot)        
import money.moneyFixed as moneyFixed

if __name__ == "__main__":    
    #mid dataProvider = tushare|yahoo|generic
    #mid storageType = csv|mongodb
    #mid ktype 数据类型，D=日k线 W=周 M=月 m5=5分钟 m15=15分钟 m30=30分钟 h1=60分钟，默认为D
    money = moneyFixed.moneyFixed()  
    
    instruments = ['600028']
    ex = ea.Expert(toPlot=True,  shortPeriod=20,longPeriod=30, 
                dataProvider = 'tushare',storageType = 'mongodb',period = 'D',
                instruments=instruments,money = money,
                fromYear = 2014,toYear=2016)
    ex.run()