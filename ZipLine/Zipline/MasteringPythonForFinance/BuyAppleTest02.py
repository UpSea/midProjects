'''
mid 2015-10-12 19：30
此部分程序可以使用zipline从yahoo下载数据，并使用所下载的数据进行回测
若有需求对次部分程序做修改时，需拷贝新建文件进行，对此文件不的修改，
其作为最小可运行版本需被原样保存。
'''
import zipline as zp
import zipline.utils.factory as zpf
import pandas as pd
import numpy as np
import tushare as ts
from datetime import datetime

# %% 01类定义
class BuyApple(zp.TradingAlgorithm):
    def __init__(self, trace=False):
        BuyApple.trace = trace
        super(BuyApple, self).__init__()
    def initialize(context):
        if BuyApple.trace: print("---> initialize")
        if BuyApple.trace: print(context)
        if BuyApple.trace: print("<--- initialize")
    def handle_data(self, context):
        if BuyApple.trace: print("---> handle_data")
        if BuyApple.trace: print(context)
        self.order("AAPL", 1)
        if BuyApple.trace: print("<-- handle_data")
# %%  02 通过zipline 下载网络数据
# zipline has its own method to load data from Yahoo! Finance
        
# 一次性获取全部日k线数据
tuData = ts.get_hist_data('000001', '2015-01-01', '2015-09-22','D')  

Date = pd.to_datetime(tuData.index)
Date.name = 'Date'
Date.tz = 'UTC'

close = tuData.close
close.index= pd.to_datetime(close.index)
close.name = 'AAPL'

ts = pd.Series(close,index = Date)
data = pd.DataFrame(ts)


# %% 03 回测
#result = BuyApple().run(data)

# %% 04 输出回测结果
#result.portfolio_value.plot(figsize=(12,8))

