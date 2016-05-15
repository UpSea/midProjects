# -*- coding: utf-8 -*-
import zipline.transforms.ta as ta
import zipline as zp
''' mid 2016-3-16 18:27
此程序来自Quantopian同名程序
原有计算平均值的方法总会出错，特改为ta方式
ta需要在initialize中预定义，如此，在handle_data中每调用一次，ta会保存历史数据
若直接在handle_data中调用，则无法保存数据，而导致每次调用时ta中都只有1个数据
'''
class DualEmaTalib(zp.TradingAlgorithm):       
    def __init__(self, *args, **kwargs):
        super(DualEmaTalib, self).__init__(*args, **kwargs)    #mid 采用super(child,self).method()格式调用某个类的父类的方法。
    def initialize(self):
        self.security = self.symbol('AAPL')
        self.short_ema_trans = ta.EMA(timeperiod=5)
        self.invested = False        
    def handle_data(self, data):
        # We've built a handful of useful data transforms for you to use,
        # such as moving average. 
        # To make market decisions, we're calculating the stock's 
        # moving average for the last 5 days and its current price. 
        average_price = self.short_ema_trans.handle_data(data)
        current_price = data[self.security].price
        print(average_price)
        if average_price[0] is None:
            return        
        # Another powerful built-in feature of the Quantopian backtester is the
        # portfolio object.  The portfolio object tracks your positions, cash,
        # cost basis of specific holdings, and more.  In this line, we calculate
        # the current amount of cash in our portfolio.   
        cash = self.portfolio.cash
        buy = False
        sell = False        
        # Here is the meat of our algorithm.
        # If the current price is 1% above the 5-day average price 
        # AND we have enough cash, then we will order.
        # If the current price is below the average price, 
        # then we want to close our position to 0 shares.
        if (current_price > 1.01*average_price).all() and not self.invested:
            if cash > current_price:
                # Need to calculate how many shares we can buy
                number_of_shares = int(cash/current_price)
                # Place the buy order (positive means buy, negative means sell)
                self.order(self.security, +number_of_shares)
                #self.log.info("Buying %s" % (self.security.symbol))
                buy = True
                self.invested = True                
        elif (current_price < average_price).all() and  self.invested:
            # Sell all of our shares by setting the target position to zero
            self.order_target(self.security, 0)
            #log.info("Selling %s" % (self.security.symbol))
            sell = True
            self.invested = False            
        # You can use the record() method to track any custom signal. 
        # The record graph tracks up to five different variables. 
        # Here we record the Apple stock price.
        self.record(stock_price = data[self.security].price,
                    average_price = average_price[self.security],
                    buy = buy,
                    sell = sell)        
if __name__ == '__main__':
    import sys
    sys.path.append('/home/mid/PythonProjects/xpower')      
    
    import zipline.utils.factory as zpf
    from datetime import datetime
    import matplotlib.pyplot as plt
    
    data = zpf.load_from_yahoo(stocks=['AAPL'],
                               indexes={},
                               start=datetime(2016, 1, 1),
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
        results[['stock_price', 'average_price']].plot(ax=ax1, lw=2.)
        ax1.plot( results.ix[ results.buy].index,  results.average_price[ results.buy],
                 '^', markersize=10, color='m')
        ax1.plot( results.ix[ results.sell].index,  results.average_price[ results.sell],
                 'v', markersize=10, color='k')
        ax2 = fig.add_subplot(212, ylabel='Portfolio value in $')
        results.portfolio_value.plot(ax=ax2, lw=2.)
        ax2.plot( results.ix[ results.buy].index,
                  results.portfolio_value[ results.buy],
                 '^', markersize=10, color='m')
        ax2.plot( results.ix[ results.sell].index,
                  results.portfolio_value[ results.sell],
                 'v', markersize=10, color='k')
        plt.legend(loc=0)
        plt.gcf().set_size_inches(14, 10)    
    algo.dumpDict = dumpDict
    results = algo.run(data)
    analyze(data,results)
    plt.show()