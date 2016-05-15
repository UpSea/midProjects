import os,sys
import pandas as pd


class feeds():
    def __init__(self):
        pass
    def getFeeds(self,feedFormat = "tushareCsv",instrument = ""):  
        if(feedFormat == "yahoo"):
            feed = self.__getFeedFromYahoo(instrument)
        elif(feedFormat == "yahooCsv"):
            feed = self.__getFeedFromYahooCsv(instrument)
        elif(feedFormat == "tushareCsv"):
            feed = self.__getFeedFromTushareCsv(instrument)
        elif(feedFormat == "tushare"):
            feed = self.__getFeedFromTushare(instrument)
        elif(feedFormat == "generic"):
            feed = self.__getFeedFromGenericCsv(instrument)
        return feed
    def __getFeedFromGenericCsv(self,instrument):
        from pyalgotrade.barfeed.csvfeed import GenericBarFeed
        from pyalgotrade import bar
        frequency = bar.Frequency.DAY
        barfeed = GenericBarFeed(frequency)
        barfeed.setDateTimeFormat('%Y-%m-%d %H:%M:%S')
        
        dataRoot = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,'histdata','tushare'))        
        code = '000001SZ'
        filename = dataRoot+os.sep+'day'+os.sep+('%s.csv'%code)          
        barfeed.addBarsFromCSV(instrument, filename) 
        return barfeed
    def __getFeedFromTushareCsv(self,instrument):
        #dataRoot = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,'PyAlgoTradeCN','utils'))        
        #sys.path.append(dataRoot)
        import dataFramefeed    
        
        dataRoot = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,'histdata','tushare'))        
        code = '600061'
        filename = dataRoot+os.sep+'day'+os.sep+('%s.csv'%code)          
    
        dat = pd.read_csv(filename,index_col=0,encoding='gbk')
        feed = dataFramefeed.Feed()
        feed.addBarsFromDataFrame(instrument, dat)        
        return feed
    def __getFeedFromYahooCsv(self,instrument):   
        from pyalgotrade.barfeed import yahoofeed        
        feed = yahoofeed.Feed()
        import sys,os
        dataPath = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,'histdata','yahoo'))                  
        fullName = os.path.abspath(os.path.join(dataPath,"yhoo-2015-yahoofinance.csv"))     
        feed.addBarsFromCSV(instrument, fullName)  
        return feed
    def __getFeedFromYahoo(self,instrument):
        from pyalgotrade.tools import yahoofinance        
        import sys,os
        dataPath = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,'histdata','yahoo'))          
        feed = yahoofinance.build_feed([instrument], 2015, 2015, dataPath)    
        return feed
    def __getFeedFromTushare(self,instrument):
        import tusharedb.tusharefinance as tusharefinance
        import sys,os
        dataPath = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,'histdata','tushare'))          
        feed = tusharefinance.build_feed([instrument], 2015, 2015, dataPath)    
        return feed        
        