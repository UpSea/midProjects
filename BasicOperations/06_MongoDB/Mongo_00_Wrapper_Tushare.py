#! /usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
import tushare as ts
import pandas as pd
from Mongo_00_Wrapper import Client

########################################################################
class ClientTushare(Client):
    #----------------------------------------------------------------------
    def downloadAndStore(self,symbol,start,end,frequency):
        """"""
        # 2)download history data    
        quotes = ts.get_hist_data(symbol,start,end,frequency)
        
        # 3)construct a secutrity
        security = {'symbol':symbol}
        security['profile'] = 'not available,please wait for next time.'
        a = {}
        security['boards']={'director':{'name':'wanglinzhong'},'prisident':{'name':'xijinping'}}
        
        ticks = {}
        tickType = {}
        security['history']=tickType
        
        tickType[frequency] = ticks
        
        for i in range(0,len(quotes)):          
            tick = {}
            ticks[quotes.index[i]] = tick
            for column in quotes.columns:
                tick[column] = quotes[column][i]
        return self.insert(security)
    #----------------------------------------------------------------------
    def retrive(self,symbol,start,end,frequency):
        securities = self.find({'symbol':symbol})
        print('retrived ok')
        
        historyDf = pd.DataFrame()
        historyDf['open'] = pd.Series()
        historyDf['high'] = pd.Series()
        historyDf['low']  = pd.Series()
        historyDf['close']= pd.Series()    
        
        for security in securities:
            print('symbol:',security['symbol'])
            history = security['history'][frequency]
    
            for tickDate in history:
                historyDf.loc[tickDate] = [history[tickDate]['open'],
                                           history[tickDate]['high'],
                                           history[tickDate]['low'],
                                           history[tickDate]['close']]
                
        historyDf.index.names = ['Date'] 
        historyDf.columns.names=['OHLC']
        historyDf.sort_index(inplace=True,ascending=True)

        return historyDf
    
    def downloadAndUpdate(self,symbol,start,end,frequency):
        """"""
        # 2)download history data    
        quotes = ts.get_hist_data(symbol,start,end,frequency)
        
        # 3)construct a secutrity
        security = {'symbol':symbol}
        security['profile'] = 'not available,please wait for next time.'
        a = {}
        security['boards']={'director':{'name':'wanglinzhong'},'prisident':{'name':'xijinping'}}
        
        ticks = {}
        tickType = {}
        security['history']=tickType
        
        tickType[frequency] = ticks
        
        for i in range(0,len(quotes)):          
            tick = {}
            ticks[quotes.index[i]] = tick
            for column in quotes.columns:
                tick[column] = quotes[column][i]
        return self.insert(security)