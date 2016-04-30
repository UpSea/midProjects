'''
mid 2015-10-12 19：30
此部分程序可以使用zipline从yahoo下载数据，并使用所下载的数据进行回测
若有需求对次部分程序做修改时，需拷贝新建文件进行，对此文件不的修改，
其作为最小可运行版本需被原样保存。
'''
import zipline as zp
import zipline.utils.factory as zpf
from datetime import datetime
# %% 01类定义
class BuyApple(zp.TradingAlgorithm):
    trace=False
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
data = zpf.load_from_yahoo(stocks=['AAPL'], 
                           indexes={}, 
                           start=datetime(1990, 1, 1),
                           end=datetime(2014, 1, 1), 
                           adjusted=False)
# %% 03 输出数据plot
# data.plot(figsize=(12,8));
# %% 03 回测
result = BuyApple(trace=False).run(data[0:10])

# %% 04 输出回测结果
result.portfolio_value.plot(figsize=(12,8))

