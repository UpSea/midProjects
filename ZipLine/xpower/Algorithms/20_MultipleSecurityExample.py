# This example runs the same momentum play as the first sample 
# (https://www.quantopian.com/help#sample-basic), but this time it uses more
# securities during the backtest.
    
# Important note: All securities in an algorithm must be traded for the 
# entire length of the backtest.  For instance, if you try to backtest both
# Google and Facebook against 2011 data you will get an error; Facebook
# wasn't traded until 2012.

# First step is importing any needed libraries.

import datetime as dt
import pytz
import zipline.transforms.ta as ta
import zipline as zp
import logbook

''' mid 2016-3-16 18:27
此程序来自Quantopian同名程序
原有计算平均值的方法总会出错，特改为ta方式
ta需要在initialize中预定义，如此，在handle_data中每调用一次，ta会保存历史数据
若直接在handle_data中调用，则无法保存数据，而导致每次调用时ta中都只有1个数据
'''
class DualEmaTalib(zp.TradingAlgorithm):       
    def __init__(self, *args, **kwargs):
        super(DualEmaTalib, self).__init__(*args, **kwargs)    #mid 采用super(child,self).method()格式调用某个类的父类的方法。
    def initialize(context):
        # Here we initialize each stock.
        # By calling symbols('AAPL', 'IBM', 'CSCO') we're storing the Security objects.
        context.stocks = context.symbols('AAPL', 'IBM', 'CSCO')
        context.add_history(3, '1d', 'price')
        context.i = 0
        
        
        logbook.StderrHandler().push_application()
        context.log = logbook.Logger('Algorithm')        
        
        
        context.vwap = {}
        context.price = {}
     
        # Setting our maximum position size, like previous example
        context.max_notional = 1000000.1
        context.min_notional = -1000000.0
    
        # Initializing the time variables we use for logging
        # Convert timezone to US EST to avoid confusion
        est = pytz.timezone('US/Eastern')
        context.d=dt.datetime(2000, 1, 1, 0, 0, 0, tzinfo=est)
    def beforeDataHandled(context,data):
        #mid 01) buffers the history,
        context._most_recent_data = data
        if context.history_container:
            context.history_container.update(data, context.datetime)
        #context._handle_data(context, data)
        # Unlike trading controls which remain constant unless placing an
        # order, account controls can change each bar. Thus, must check
        # every bar no matter if the algorithm places an order or not.
        context.validate_account_controls()    
        
        #mid 02) checks the values of buffers
        dp = context.history_container.digest_panels
        for k in dp.keys():
            df = dp[k].buffer['price']
            a = df.dropna()
            print('No.',context.i,':Len.',len(a))
            print('Contents:')        
            print(a)
        print(context.history_container.buffer_panel.buffer['price'])    
    def handle_data(context, data):
        context.beforeDataHandled(data)
        context.i += 1
        # Skip first 40 days to get full windows      
        if context.i < 3:
            return        
        # Initializing the position as zero at the start of each frame
        notional=0
        
        # This runs through each stock.  It computes
        # our position at the start of each frame.
        for stock in context.stocks:
            price = data[stock].price 
            notional = notional + context.portfolio.positions[stock].amount * price
            tradeday = data[stock].datetime
            
        # This runs through each stock again.  It finds the price and calculates
        # the volume-weighted average price.  If the price is moving quickly, and
        # we have not exceeded our position limits, it executes the order and
        # updates our position.
        for stock in context.stocks:   
            vwap = data[stock].vwap(3)   #此处会调用history()这个函数也是需要自定义的
            price = data[stock].price  
    
            if price < vwap * 0.995 and notional > context.min_notional:
                context.order(stock,-100)
                notional = notional - price*100
            elif price > vwap * 1.005 and notional < context.max_notional:
                context.order(stock,+100)
                notional = notional + price*100
            #aaa = stock.symbol
            #context.record(aaa = price)
        # If this is the first trade of the day, it logs the notional.
        if (context.d + dt.timedelta(days=1)) < tradeday:
            context.log.debug(str(notional) + ' - notional start ' + tradeday.strftime('%m/%d/%y'))
            context.d = tradeday
            
        #context.record(short_mavg = short[context.stocks[1]],
                    #long_mavg = long[context.stocks[1]],
                    #goog_price = context.price)          
if __name__ == '__main__':
    import sys
    sys.path.append('/home/mid/PythonProjects/xpower')      
    
    import zipline.utils.factory as zpf
    import matplotlib.pyplot as plt
    
    data = zpf.load_from_yahoo(stocks=['AAPL', 'IBM', 'CSCO'],
                               indexes={},
                               start=dt.datetime(2016, 1, 1),
                               end=dt.datetime(2016, 3, 5),
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
        data[['AAPL', 'IBM', 'CSCO']].plot(ax=ax1, color='r', lw=2.)
        #results[['stock_price', 'average_price']].plot(ax=ax1, lw=2.)
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