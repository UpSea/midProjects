# -*- coding: utf-8 -*-
import os,sys
import pandas as pd
from tusharedb.tushareDataManager import tushareDataCenter


class dataCenter():
    def __init__(self):
        dataPath = os.path.abspath(os.path.join(os.path.dirname(__file__),'data','csv','tusharedb'))                
        self.tsCenter = tushareDataCenter(dataPath)    
                
    def getCodes(self,codesType,sourceType):
        if(codesType == 'tushare'):
            return self.tsCenter.getCodes(sourceType)
        elif(codesType == 'yahoo'):
            if(sourceType == 'remote'):
                pass
            elif(sourceType == 'mongodb'):
                pass
            elif(sourceType == 'csv'):
                pass 
        elif(codesType == 'sina'):
            if(sourceType == 'remote'):
                pass
            elif(sourceType == 'mongodb'):
                pass
            elif(sourceType == 'csv'):
                pass             
        elif(codesType == 'datayes'):
            if(sourceType == 'remote'):
                pass
            elif(sourceType == 'mongodb'):
                pass
            elif(sourceType == 'csv'):
                pass    
        return None
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
        '''mid
        使用系统自定义的与数据提供者的数据格式相互独立的csv格式储存的文件
        可以作为用户管理各种数据源的统一格式使用
        '''
        from pyalgotrade.barfeed.csvfeed import GenericBarFeed
        from pyalgotrade import bar
        frequency = bar.Frequency.DAY
        barfeed = GenericBarFeed(frequency)
        barfeed.setDateTimeFormat('%Y-%m-%d %H:%M:%S')
        
        dataRoot = os.path.abspath(os.path.join(os.path.dirname(__file__),'data','generic','csv'))        
        filename = dataRoot+os.sep+'day'+os.sep+('%s.csv'%instrument)          
        barfeed.addBarsFromCSV(instrument, filename) 
        return barfeed
    def __getFeedFromTushareCsv(self,instrument):
        '''mid
        直接读取某个tushare格式的csv文件到pandas，再解析为feed格式返回
        '''
        import tusharedb.tusharefeed as tusharefeed        
        dataRoot = os.path.abspath(os.path.join(os.path.dirname(__file__),'data','tusharedb','csv'))        
        filename = dataRoot+os.sep+'day'+os.sep+('%s.csv'%instrument)          
    
        dat = pd.read_csv(filename,index_col=0,encoding='gbk')
        feed = tusharefeed.Feed()
        feed.addBarsFromDataFrame(instrument, dat)   
        return feed
    def __getFeedFromYahooCsv(self,instrument,fromYear = 2014,toYear = 2016):   
        from pyalgotrade.barfeed import yahoofeed        
        feed = yahoofeed.Feed()
        import sys,os
        dataPath = os.path.abspath(os.path.join(os.path.dirname(__file__),'data','yahoodb','csv'))    
        
        for year in range(fromYear, toYear+1):
            fileName = os.path.join(dataPath, "%s-%d-yahoofinance.csv" % (instrument, year))
            if os.path.exists(fileName):              
                feed.addBarsFromCSV(instrument, fileName)  
        return feed
    def __getFeedFromYahoo(self,instrument):
        from pyalgotrade.tools import yahoofinance        
        import sys,os
        dataPath = os.path.abspath(os.path.join(os.path.dirname(__file__),'data','yahoodb','csv'))          
        feed = yahoofinance.build_feed([instrument], 2015, 2015, dataPath)    
        return feed
    def __getFeedFromTushare(self,instrument):
        '''mid
        通过tusharedatamanager查询某个csv文件是否存在，如果不存在则通过tushare模块下载
        将已存在的csv文件通过tusharedatamanager读入dataframe，再解析为feed格式返回
        '''
        import tusharedb.tusharefinance as tusharefinance
        import sys,os
        dataPath = os.path.abspath(os.path.join(os.path.dirname(__file__),'data','tusharedb','csv'))          
        feed = tusharefinance.build_feed([instrument], 2015, 2015, dataPath)    
        return feed        
        