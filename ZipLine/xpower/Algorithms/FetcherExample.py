# -*- coding: utf-8 -*-
# This example runs the same momentum play as the first sample 
# (https://www.quantopian.com/help#sample-basic), but this time it uses more
# securities during the backtest.
    
# Important note: All securities in an algorithm must be traded for the 
# entire length of the backtest.  For instance, if you try to backtest both
# Google and Facebook against 2011 data you will get an error; Facebook
# wasn't traded until 2012.

# First step is importing any needed libraries.
from datetime import datetime
import pytz
import zipline.transforms.ta as ta
import zipline as zp
from zipline.protocol import BarData
#import zipline.protocol.BarData 
''' mid 2016-3-16 18:27
此程序来自Quantopian同名程序
原有计算平均值的方法总会出错，特改为ta方式
ta需要在initialize中预定义，如此，在handle_data中每调用一次，ta会保存历史数据
若直接在handle_data中调用，则无法保存数据，而导致每次调用时ta中都只有1个数据
'''
def rename_col(df):
    df = df.rename(columns={'New York 15:00': 'price'})
    df = df.rename(columns={'Value': 'price'})
    df = df.fillna(method='ffill')
    df = df[['price', 'sid']]
    # Correct look-ahead bias in mapping data to times   
    df = df.tshift(1, freq='b')
    log.info(' \n %s ' % df.head())
    return df
def preview(df):
    log.info(' \n %s ' % df.head())
    return df  
class DualEmaTalib(zp.TradingAlgorithm):       
    def __init__(self, *args, **kwargs):
        super(DualEmaTalib, self).__init__(*args, **kwargs)    #mid 采用super(child,self).method()格式调用某个类的父类的方法。
    def initialize(context):
        # import the external data
        fetch_csv should be customized by oneself
        fetch_csv('https://www.quandl.com/api/v1/datasets/JOHNMATT/PALL.csv?trim_start=2012-01-01',
                  date_column='Date',
                  symbol='palladium',
                  pre_func = preview,
                  post_func=rename_col,
                  date_format='%Y-%m-%d')
    
        fetch_csv('https://www.quandl.com/api/v1/datasets/BUNDESBANK/BBK01_WT5511.csv?trim_start=2012-01-01',
                  date_column='Date',
                  symbol='gold',
                  pre_func = preview,
                  post_func=rename_col,
                  date_format='%Y-%m-%d')
        
        # Tiffany
        context.stock = symbol('TIF')
    def handle_data(context, data):
        # Invest 10% of the portfolio in Tiffany stock when the price of gold is low.
        # Decrease the Tiffany position to 5% of portfolio when the price of gold is high.
    
        if (data['gold'].price < 1600):
            order_target_percent(context.stock, 0.10)
        if (data['gold'].price > 1750):
            order_target_percent(context.stock, 0.05)
    
        #record the variables   
        if 'price' in data['palladium']:
            record(palladium=data['palladium'].price, gold=data['gold'].price) 
if __name__ == '__main__':
    import sys
    sys.path.append('/home/mid/PythonProjects/xpower')      
    
    import zipline.utils.factory as zpf
    import matplotlib.pyplot as plt
    
    data = zpf.load_from_yahoo(stocks=['BA','AAPL'],
                               indexes={},
                               start=datetime(2015, 1, 1),
                               end=datetime(2016, 3, 5),
                               adjusted=True)
    algo = DualEmaTalib(instant_fill=True,
                          capital_base=50000,
                          env=None,
                          sim_params = None,  # 设置有此参数时，start和end不能再设置，否则，显得多余也会运行assert错误
                          #start = algo['start'],
                          #end = algo['end'],
                          data_frequency = 'daily')
    def dumpDict(dictStr):
        """"""
        import json
        jsonDumpsIndentStr = json.dumps(dictStr, indent=4,skipkeys = False,default=str,sort_keys=True)
        print (jsonDumpsIndentStr) 
    def analyze(data,  results):
        fig = plt.figure()
        ax1 = fig.add_subplot(211, ylabel='Price in $')
        data['AAPL'].plot(ax=ax1, color='r', lw=2.)
        results[['short_mavg', 'short_mavg']].plot(ax=ax1, lw=2.)
        #ax1.plot( results.ix[ results.buy].index,  results.average_price[ results.buy],
                 #'^', markersize=10, color='m')
        #ax1.plot( results.ix[ results.sell].index,  results.average_price[ results.sell],
                 #'v', markersize=10, color='k')
        ax2 = fig.add_subplot(212, ylabel='Portfolio value in $')
        results.portfolio_value.plot(ax=ax2, lw=2.)
        #ax2.plot( results.ix[ results.buy].index,
                  #results.portfolio_value[ results.buy],
                 #'^', markersize=10, color='m')
        #ax2.plot( results.ix[ results.sell].index,
                  #results.portfolio_value[ results.sell],
                 #'v', markersize=10, color='k')
        plt.legend(loc=0)
        plt.gcf().set_size_inches(14, 10)    
    algo.dumpDict = dumpDict
    results = algo.run(data)
    analyze(data,results)
    plt.show()