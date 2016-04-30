'''
mid 此程序原先通过ziplilne内置方法从yahoo获取数据并进行运算
从此数据的格式如下：
    In [45]:type(data)
    Out[45]:pandas.core.frame.DataFrame
内容如下：
    In [39]:data['1999']
    Out[39]:
                                       AAPL
        Date                               
        1999-01-04 00:00:00+00:00   41.2500
        1999-01-05 00:00:00+00:00   43.3125
        1999-01-06 00:00:00+00:00   41.7500
        1999-01-07 00:00:00+00:00   45.0000
        1999-01-08 00:00:00+00:00   45.0000
        ...                             ...
        1999-12-27 00:00:00+00:00   99.3125
        1999-12-28 00:00:00+00:00   98.1875
        1999-12-29 00:00:00+00:00  100.6875
        1999-12-30 00:00:00+00:00  100.3125
        1999-12-31 00:00:00+00:00  102.8125
        
        [252 rows x 1 columns]
        
只需将得自tushare的数据按此格式转换，即可用新数据运行回测。
同时需要注意以下时间Index格式的不同
1）
data2000.index
    Out[128]: 
    DatetimeIndex(['2000-01-03', '2000-01-04', '2000-01-05', '2000-01-06',
                   '2000-01-07'],
                  dtype='datetime64[ns]', name='Date', freq=None, tz='UTC')
2）
dataTs.index
    Out[129]: 
    Index(['2015-01-05', '2015-01-06', '2015-01-07', '2015-01-08', '2015-01-09',
           '2015-01-12', '2015-01-13', '2015-01-14', '2015-01-15', '2015-01-16', 
           ...
           '2015-09-09', '2015-09-10', '2015-09-11', '2015-09-14', '2015-09-15',
           '2015-09-16', '2015-09-17', '2015-09-18', '2015-09-21', '2015-09-22'],
          dtype='object', name='date', length=178)

zipLine获取的数据的index是datetime54[ns]
tushare获取的数据的index是object

这个需要转换
'''
import zipline as zp
import zipline.utils.factory as zpf
from datetime import datetime

import tushare as ts
import pandas as pd
import numpy as np

class BuyApple(zp.TradingAlgorithm):
    """ Simple trading algorithm that does nothing
    but buy one share of AAPL every trading period.
    """
    
    # trace=False
    
    def __init__(self, trace=False):
        BuyApple.trace = trace
        super(BuyApple, self).__init__()
    
    def initialize(context):
        if BuyApple.trace: 
            print("---> mid start initialize")
        if BuyApple.trace: 
            print(context)
        if BuyApple.trace: 
            print("<--- mid end initialize")
        
    def handle_data(self, context):
        if BuyApple.trace: 
            print("---> mid start handle_data")
        if BuyApple.trace: 
            print(context)
        self.order("AAPL", 1)
        if BuyApple.trace: 
            print("<-- mid end handle_data")  
            
# %% 根据字符串数组构造Datetime
strDate = ['2015-01-05', '2015-01-06', '2015-01-07', '2015-01-08', '2015-01-09',
           '2015-01-12', '2015-01-13', '2015-01-14', '2015-01-15', '2015-01-16']
date = pd.to_datetime(strDate)
data = pd.DataFrame(np.random.randn(10),index = date)
#%% 人工构建Datetime
longer_ts = pd.Series(np.random.randn(100),
                      index = pd.date_range('1/1/2000',periods = 100,tz = 'UTC',name = 'Date'),name='AAPL')

data = pd.DataFrame(longer_ts)

# %% 回测

data.plot(figsize=(12,8))

result = BuyApple(trace = True).run(data[:5])
"""
data = zpf.load_from_yahoo(stocks=['AAPL'], 
                           indexes={}, 
                           start=datetime(1990, 1, 1),
                           end=datetime(2014, 1, 1), 
                           adjusted=False)
"""
'''
datetime64 生成方式01


生成方式02

dates = [datetime(2011,1,2),datetime(2011,1,5)]
ts = pd.TimeSeries(np.random.randn(2),index = dates)
'''

#data2000 = data['2015-01-03':'2015-01-16']



#data2000.plot(figsize=(12,8));

#dataTs = ts.get_hist_data('000001', '2015-01-01', '2015-09-22', 'D') 

# dataTsClose = pd.DataFrame(dataTs['close'])

#result = BuyApple(trace=True).run(data2000)

# result = BuyApple(trace=True).run(data['2015-01-01':'2015-09-22'])
'''
result.portfolio_value.plot(figsize=(12,8))

result_for_2000 = BuyApple().run(data['2000'])
result_for_2000.portfolio_value.plot(figsize=(12,8))


'''

