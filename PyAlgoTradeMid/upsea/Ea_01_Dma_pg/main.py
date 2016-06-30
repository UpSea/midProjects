# -*- coding: utf-8 -*-
import os,sys
from PyQt4 import QtGui,QtCore
import time as time
import datetime as dt

#mid 3)money
dataRoot = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir))        
sys.path.append(dataRoot)
import money.moneyFixed  as moneyFixed
import money.moneyFirst  as moneyFirst
import money.moneySecond as moneySecond
import EA.Ea             as Ea
 
class eaController():
    def __init__(self,timeFrom,timeTo,phases):
        self.timeFrom = timeFrom
        self.timeTo = timeTo
        self.phases = phases
    def run(self):
        ea = self.getEa()
        results = self.runByPhase(self.timeFrom,self.timeTo,self.phases,ea)
    
    
        print  "------------------------"
        print self.timeFrom,' to ',self.timeTo
        print  "------------------------"

        for result in results:
            print result         
    def runByPhase(self,timeFrom,timeTo,phases,ea):
        #mid str to pyTimeStamp
        timeStampFrom = int(time.mktime(time.strptime(timeFrom, "%Y-%m-%d %H:%M:%S")))
        timeStampTo   = int(time.mktime(time.strptime(timeTo, "%Y-%m-%d %H:%M:%S")))    
        print timeFrom,timeTo
        
        interval = (timeStampTo - timeStampFrom)/phases
        
        startTimeStamp = timeStampFrom
        results = []
        for index in range(phases):
            endTimeStamp = startTimeStamp + interval
            
            #mid pyTimeStamp to datetime
            timeFromDatetime = dt.datetime.utcfromtimestamp(startTimeStamp)
            timeToDatetime = dt.datetime.utcfromtimestamp(endTimeStamp)
            '''
            #mid pyTimeStamp to datetime to str
            timeFrom = dt.datetime.utcfromtimestamp(startTimeStamp).strftime("%Y-%m-%d %H:%M:%S")
            timeTo = dt.datetime.utcfromtimestamp(endTimeStamp).strftime("%Y-%m-%d %H:%M:%S")
            
            #mid str to datetime
            timeFrom = dt.datetime.strptime(timeFrom,'%Y-%m-%d %H:%M:%S')    
            timeTo = dt.datetime.strptime(timeTo,'%Y-%m-%d %H:%M:%S')              
            
            '''
            result01 = ea.run(timeFrom = timeFromDatetime,timeTo = timeToDatetime)
        
            result02 = ea.summary() 
            
            results.append(result02)
            
            startTimeStamp = endTimeStamp
        return results
    def getEa(self):    
        '''mid
        mid dataProvider = tushare|mt5|yahoo|generic
        mid storageType = csv|mongodb
        mid period 数据类型，D=日k线 W=周 M=月 m1=1分钟 m5=5分钟 m15=15分钟 m30=30分钟 h1=60分钟，默认为D
        
        money = 'moneyFixed'
        money = 'moneyFirst'
        money = 'moneySecond' 
        '''       
        #run(timeFrom = '2016-05-08 00:00:00',timeTo = '2016-05-30 00:00:00',symbol = '000099',money = 'moneyFixed',dataProvider = 'tushare',storageType = 'csv',period = 'D',shortPeriod=10,longPeriod=20)
        #run(timeFrom = '2016-05-08 00:00:00',timeTo = '2016-05-30 00:00:00',symbol = 'XAUUSD',money = 'moneyFirst',dataProvider = 'mt5',storageType = 'mongodb',period = 'm15',shortPeriod=10,longPeriod=20)    
        #run(timeFrom = '2016-05-08 00:00:00',timeTo = '2016-05-30 00:00:00',symbol = '600028',money = 'moneySecond',dataProvider = 'tushare',storageType = 'csv',period = 'h1',shortPeriod=10,longPeriod=20)    
        
        instruments = ['XAUUSD']
        #mid money
        #money = moneyFixed.moneyFixed()
        #money = moneyFirst.moneyFirst()
        money = moneySecond.moneySecond()  
            
        ea = Ea.Expert(toPlot=False,  shortPeriod=10,longPeriod=20, 
                      dataProvider = 'mt5',storageType = 'csv',period = 'm5',
                      instruments=instruments,money = money)    
        return ea        

if __name__ == "__main__": 
    app = QtGui.QApplication(sys.argv)    
    startRun = time.clock()
    
    eaController('2016-05-05 00:00:00', '2016-05-30 00:00:00', 5).run()
    
    endRun = time.clock()
    print "run time: %f s" % (endRun - startRun)       
    sys.exit(app.exec_())  
