'''
mid 2015-10-12 19：59
此程序不再通过zipline从yahoo下载数据，而是自己按zipline所需数据格式构造数据，
并用zipline回测之
'''
import zipline as zp
import pandas as pd
import numpy as np
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
longer_ts = pd.Series(np.random.randn(100),
                      index = pd.date_range('1/1/2000',periods = 100,
                                            tz = 'UTC',name = 'Date'),
                      name='AAPL')
data = pd.DataFrame(longer_ts)
# %% 03 输出数据plot
# data.plot(figsize=(12,8));
# %% 03 回测
result = BuyApple().run(data)

# %% 04 输出回测结果
result.portfolio_value.plot(figsize=(12,8))

