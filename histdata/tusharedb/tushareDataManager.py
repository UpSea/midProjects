# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 11:04:32 2015

@author: lenovo
"""
from itertools import izip
#import sys
import os,sys
dataRoot = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,os.pardir))        
sys.path.append(dataRoot) 
import constant as ct

import pylab as plt
import pandas as pd
import tushare as ts
import numpy as np
import time,os
from pandas import DataFrame
from pyalgotrade import bar        

#reload(sys)
#sys.setdefaultencoding('utf-8')
#code为全部，code_inuse为起止日期完备的数据

class tushareDataCenter():
    def __init__(self):
        self.dataRoot = os.path.abspath(os.path.join(os.path.dirname(__file__)))        
        self.codefile = self.dataRoot +os.sep + "code.csv"   
        self.codeinusefile = self.dataRoot + os.sep + "code_inuse.csv"
        self.codenewinusefile = self.dataRoot + os.sep + "code_new_inuse.csv"
    def downloadAndStoreCodes(self,code):
        dat = ts.get_industry_classified()
        dat = dat.drop_duplicates('code') 
        dat.to_csv(self.codefile,encoding='gbk')    
    def exists(self,instrument,frequency):
        from pyalgotrade import bar        
        try:
            if frequency == bar.Frequency.DAY:
                fileName = os.path.join(self.dataRoot,'day',('%s.csv'%instrument))
                if os.path.exists(fileName):
                    return True
                else:
                    return False
            elif frequency == bar.Frequency.WEEK:
                fileName = os.path.join(self.dataRoot,'day',('%s.csv'%instrument))
                if os.path.exists(fileName):
                    return True
                else:
                    return False                
            else:
                raise Exception("Invalid frequency")
        except Exception, e:
            raise e   
    def downloadAndStoreKDataByCode(self,instrument,_start_,_end_):
        try:
            _data_ = ts.get_hist_data(instrument,start=None,end=None)  #默认取3年，start 8-1包括
            fileName = os.path.join(self.dataRoot,'day',('%s.csv'%instrument))
            if _data_ is not None and _data_.size != 0:
                if os.path.exists(fileName):
                    _data_.to_csv(fileName, mode='a', header=None,encoding='gbk')
                else:
                    _data_.to_csv(fileName,encoding='gbk')
            else:
                return False
        except IOError: 
            pass    #不行的话还是continue
        return True
    def downloadAndStoreAllData(self):
        '''mid 下载代码表及其中所有历史数据
        1.自tushare下载代码表:code.csv
        2.据下载的代码表下载历史数据
        3.根据下载的历史数据判断对应的代码是否有效
        4.对有效代码生成单独列表并单独存放：code_insuse.csv
            有效代码判断逻辑：该代码下载的历史数据的起始日起和结束日期必须在规定的范围之内
            范围定义在constant.py中，ct._start_range,ct._end_range
        
        历史数据根目录为此文件上级目录下的histdata目录，根下为代码文件，/day下为日线，/min下为分钟线
        '''
        dat = pd.read_csv(self.codefile,index_col=0,encoding='gbk')
        inuse = []
        i = 0
        for code in dat['code'].values:
            i+= 1
            print i,code
            if i > 15:
                break
            try:
                _data_ = ts.get_hist_data(str(code),end=ct._MIDDLE_)
                if _data_ is not None:
                    _data_.to_csv((self.dataRoot+os.sep+'day'+os.sep+('%s.csv'%code)),encoding='gbk')
                    print str(_data_.index[0])+':'+str(_data_.index[-1])
                    if _data_.index[-1] in ct._start_range and _data_.index[0] in ct._end_range:
                        inuse.append(code)
            except IOError: 
                pass    #不行的话还是continue           
        print len(inuse)
        _df_inuse = DataFrame(inuse,columns={'code'})
        _df_inuse.to_csv(self.codeinusefile,encoding='gbk')
    #从网络中更新数据,code 必须为str，dat中的为int
    def downloadAndStoreOrAppendAllData(self,_start_ ='2015-08-01',_end_ = ct._TODAY_):
        '''mid 对代码表文件中的代码对应的最新历史数据进行下载
        1.依据已下载代码表轮流下载对应代码数据
        2.对已有下载的代码对应的数据进行append，对尚未下载的数据对应的文件进行创建
        3.新做code_new_inuse.csv,此文件中的code必须要在原inuse.csv中存在，且新下载的数据满足此过程中新设置的头尾日期限定
        '''        
        dat = pd.read_csv(self.codefile,index_col=0,encoding='gbk')
        inuse = pd.read_csv(self.codeinusefile,index_col=0,parse_dates=[0],encoding='gbk')
        new_inuse = []
        
        i=0
        for code in dat['code'].values:
            i+= 1
            print i,code
            if i > 10:
                break        
            try:
                _data_ = ts.get_hist_data(str(code),start=_start_,end=_end_)
                filename = path+os.sep+'day'+os.sep+('%s.csv'%code)
                if _data_ is not None and _data_.size != 0:
                    if os.path.exists(filename):
                        _data_.to_csv(filename, mode='a', header=None,encoding='gbk')
                    else:
                        _data_.to_csv(filename,encoding='gbk')
                    startRange = pd.date_range(start=_start_,periods=7)
                    endRange = pd.date_range(end=_end_,periods=7)
                    if code in inuse['code'].values and _data_.index[0] in endRange and _data_.index[-1] in startRange:
                        new_inuse.append(code)  
            except IOError: 
                pass    #不行的话还是continue           
        print len(new_inuse)
        _df_inuse = DataFrame(new_inuse,columns={'code'})
        _df_inuse.to_csv(self.codenewinusefile,encoding='gbk')
                    
    def retriveAllData(self):      
        '''mid加载所有本地数据
        1.数据结构为dict
        2.dict成员为dataframe
        3.dict的key为code，code类型为int
        '''
        dat = pd.read_csv(self.codefile,index_col=0,encoding='gbk')
        dic = {}
        
        i = 0
        for code in dat['code'].values:
            i+= 1
            #print i,code
            try:
                df = pd.read_csv(self.dataRoot+os.sep+'day'+os.sep+('%s.csv'%code),index_col=0,parse_dates=[0],encoding='gbk')  
                if df is not None:
                    dic[code] = df
                    print i,code,type(code)
            except IOError: 
                pass    #不行的话还是continue
        return dic

    #仅适用数据头尾完备的code    
    def retriveCodesInuse(self):
        try:
            dat = pd.read_csv(self.codeinusefilepath,index_col=0,parse_dates=[0],encoding='gbk')
        except Exception: 
            dat = ts.get_industry_classified()
        dat = dat.drop_duplicates('code')                                                   #去除重复code
        return dat['code'].values 

  
    def retriveKDataByCode(self,instrument,frequency=bar.Frequency.DAY):
        if frequency == bar.Frequency.DAY:
            fileName = os.path.join(self.dataRoot,'day',('%s.csv'%instrument))
        elif frequency == bar.Frequency.WEEK:
            fileName = os.path.join(self.dataRoot,'day',('%s.csv'%instrument))
    
        try:        
            dat = pd.read_csv(fileName,index_col=0,encoding='gbk')
            #dat = pd.read_csv(fileName,index_col=0,parse_dates=[0],encoding='gbk')  #parse_dates直接转换数据类型 string->datastamp
        except Exception,e:
            dat = None            
            raise e
        
        return dat.sort_index(axis=0,ascending=True)
    def get_macd(self,df):
        _columns_ = ['EMA_12','EMA_26','DIFF','MACD','BAR']
        a = np.zeros(len(df)*5).reshape(len(df),5) #也可以EMA_12 = [0 for i in range(len(df))]
        a[-1][0] =  df['close'][0]    #EMA_12
        a[-1][1] =  df['close'][0]
        
        for i in range(len(df)):
            a[i][0] = a[i-1][0]*11/13+df['close'][i]*2/13  #EMA_12       
            a[i][1] = a[i-1][1]*25/27+df['close'][i]*2/27 #EMA_26
            a[i][2] =  a[i][0]-a[i][1]  #DIFF
            a[i][3] = a[i-1][3]*8/10+a[i][2]*2/10 #MACD
            a[i][4]=2*(a[i][2]-a[i][3])
        return DataFrame(a,index = df.index,columns = _columns_) 

    #df为原dataframe da为macd
    def plt_macd(self,df,da):
        my_dfs = [df['open'], da['EMA_12'], da['EMA_26'], da['DIFF'], da['MACD'], da['BAR'],] # or in your case [ df,do]
        my_opts = [ {"color":"green", "linewidth":1.0, "linestyle":"-","label":"open"},
                    {"color":"blue","linestyle":"-","label":"EMA_12"},
                    {"color":"yellow","linestyle":"-","label":"EMA_26"},
                    {"color":"black","linestyle":"-","label":"DIFF"},
                    {"color":"red","linestyle":"-","label":"MACD"},
                    {"color":"orange","linestyle":"-","label":"BAR"}]
        for d,opt in izip(my_dfs, my_opts):
            d.plot( **opt)
        plt.grid()
        plt.legend(loc=0)
        plt.show()  
    #选择下跌行情中天量成交和高换手率，后期加入小盘股等指标，scope 为近15日
    #scope =15,看最近15天的情况，v_times 为当日成交量为前一日的倍数，t_percent为当日换手率
    def bigVolume(self,scope=15,v_times=5,t_percent=20):
        inuse = pd.read_csv(self.codeinusefile,index_col=0,parse_dates=[0],encoding='gbk')
        rs_list = []
        i=0
        for code in inuse['code'].values:
            try:
                _data_ = pd.read_csv(self.dataRoot+os.sep+'day'+os.sep+('%s.csv'%code),index_col=0,parse_dates=[0],encoding='gbk')
                dd = (_data_['volume']/_data_['volume'].shift(1)>v_times) & (_data_['turnover']>t_percent)
                dd = dd & (_data_['close']<22)
                if dd[-scope:].any():
                    i+=1
                    if i<5:
                        _data_['close'].plot()
                    rs_list.append(code)
                    print i,code
            except IOError: 
                pass    #不行的话还是continue        
    def change_type_to_yahoo(self):
        '''mid
        此方法将所有来自tushare的数据转化为同yahoo数据格式，以方便用于pyalgotrade调用
        '''
        inuse = pd.read_csv('d:/data/code_inuse.csv',index_col=0,parse_dates=[0],encoding='gbk')               
        inuse.to_csv('d:/data2/code_inuse.csv',encoding='gbk')
        re_columns ={'high':'High','low':'Low','open':'Open','close':'Close','volume':'Volume','price_change':'Adj Close'}  
        i=0
        for code in inuse['code'].values:
            i+= 1
            print i,code
            _data_ = pd.read_csv('d:/data/%s.csv'%code,index_col=0,parse_dates=[0],encoding='gbk')  #默认取3年，start 8-1包括
            _data_=_data_.rename(columns=re_columns)
            _data_.index.name = 'Date'
            _data_.to_csv('d:/data2/%s.csv'%code,columns=['Open','High','Low','Close','Volume','Adj Close'],
                          date_format="%Y-%m-%d",encoding='gbk')
    def getBetaSample(self):  
        '''mid
        仅是一个实例，用于演示，无特定功能
        '''
        def get_beta(values1, values2):
            # http://statsmodels.sourceforge.net/stable/regression.html
            model = sm.OLS(values1, values2)
            results = model.fit()
            return results.params[0]
        value1=[0.5,1.0,1.5,2.0,2.5,3.0]
        value2=[1.75,2.45,3.81,4.80,7.00,8.60]
        print get_beta(value1,value2) 
        
if __name__ == "__main__":
    tsCenter = tushareDataCenter()
    if(False):
        tsCenter.downloadAndStoreOrAppendAllData()
    if(False):
        #mid 1)加载所有KData数据
        d = tsCenter.retriveAllData()
    if(False):
        #mid 应做修改，使用codes列表进行下载
        code = '600209'
        d = tsCenter.downloadAndStoreKDataByCode(code)
    if(False):
        #mid 2)下载代码表
        tsCenter.downloadAndStoreCodes()
    if(False):
        #mid 3)依据已下载代码表下载所有对应KData到本地
        tsCenter.downloadAndStoreAllData()      
    if(True):
        #mid 4)依据代码，检索本地数据，并图形化输出
        kdata = tsCenter.retriveKDataByCode('000881')
        start = u'2015-04-01'
        end = u'2015-12-31'
        data = kdata.loc[start:end,['open','high','low','close']]
        data = kdata.loc[start:end,:]
        
        kdata = data
        
        da = tsCenter.get_macd(kdata)
        da = tsCenter.plt_macd(kdata,da)
    if(False):
        tsCenter.bigVolume()
''' mid 读取并图形化某个symbol的数据
df = pd.read_csv(datafile,index_col=0,parse_dates=[0],encoding='gbk') 
da = get_macd(df) 
plt_macd(df,da)
'''
#_data_ = pd.read_csv(datafile,index_col=0,encoding='gbk')  
#dic = read_data()
#_data_ = ts.get_hist_data('900901',start=ct._START_,end=ct._MIDDLE_)
#print _data_
#重命名索引名，列名，将调整收盘价置为none


    

#refresh_data()              
#change_type_to_yahoo()
#bigVolume()
#_data_ = pd.read_csv('d:/data/600848.csv',index_col=0,parse_dates=[0],encoding='gbk')
#_data_.plot() 