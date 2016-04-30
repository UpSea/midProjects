# This example runs the same momentum play as the first sample 
# (https://www.quantopian.com/help#sample-basic), but this time it uses more
# securities during the backtest.
    
# Important note: All securities in an algorithm must be traded for the 
# entire length of the backtest.  For instance, if you try to backtest both
# Google and Facebook against 2011 data you will get an error; Facebook
# wasn't traded until 2012.

# First step is importing any needed libraries.
'''
本例对Record Variables Example功能有扩充
其中多symbol的计算处理很有借鉴意义
应参照其实现对Multiple Security Example做出修改
'''



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
class DualEmaTalib(zp.TradingAlgorithm):       
    def __init__(self, *args, **kwargs):
        super(DualEmaTalib, self).__init__(*args, **kwargs)    #mid 采用super(child,self).method()格式调用某个类的父类的方法。
    # This initialize function sets any data or variables that you'll use in
    # your algorithm.
    def initialize(context):
        context.stocks = context.symbols('BA','AAPL')  # Boeing
    
        context.ShortEmas = {}
        context.LongEmas = {}
        for stock in context.stocks:
            context.ShortEmas[stock] = ta.EMA(timeperiod=20)
            context.LongEmas[stock] = ta.EMA(timeperiod=80)

    # Now we get into the meat of the algorithm. 
    def handle_data(context, data):
        # Create a variable for the price of the Boeing stock
        context.price = data[context.stocks[1]].price
        
        # Create variables to track the short and long moving averages. 
        # The short moving average tracks over 20 days and the long moving average
        # tracks over 80 days. 
        shorts = {}
        longs = {}
        for stock in context.stocks:
            current_data = BarData()
            current_data[0] = data[stock]
            shorts[stock] = context.ShortEmas[stock].handle_data(current_data)
            longs[stock] = context.LongEmas[stock].handle_data(current_data)
        
        short = shorts[context.stocks[0]]
        long = longs[context.stocks[0]]
        # If the short moving average is higher than the long moving average, then 
        # we want our portfolio to hold 500 stocks of Boeing
        if short is None or long is None:
            return        
        if (short > long).all():
            context.order_target(context.stocks[0], +500)
        
        # If the short moving average is lower than the long moving average, then
        # then we want to sell all of our Boeing stocks and own 0 shares
        # in the portfolio. 
        elif (short < long).all():
            context.order_target_value(context.stocks[0], 0)
    
        # Record our variables to see the algo behavior. You can record up to 
        # 5 custom variables. To see only a certain variable, deselect the 
        # variable name in the custom graph in the backtest. 
        context.record(short_mavg = short[context.stocks[1]],
               long_mavg = long[context.stocks[1]],
               goog_price = context.price)   
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