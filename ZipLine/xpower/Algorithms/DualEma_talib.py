# -*- coding: utf-8 -*-
from zipline.transforms.ta import EMA
import zipline.transforms.ta as ta
import zipline as zp
class DualEmaTalib(zp.TradingAlgorithm):       
    def __init__(self, *args, **kwargs):
        super(DualEmaTalib, self).__init__(*args, **kwargs)    #mid 采用super(child,self).method()格式调用某个类的父类的方法。
    def initialize(self):
        self.asset = self.symbol('AAPL')
    
        # Add 2 mavg transforms, one with a long window, one with a short window.
        self.short_ema_trans = ta.EMA(timeperiod=20)
        self.long_ema_trans = EMA(timeperiod=40)
    
        # To keep track of whether we invested in the stock or not
        self.invested = False
    def handle_data(self, data):
        #mid only long
        short_ema = self.short_ema_trans.handle_data(data)
        long_ema = self.long_ema_trans.handle_data(data)
        if short_ema is None or long_ema is None:
            return
    
        buy = False
        sell = False
    
        if (short_ema > long_ema).all() and not self.invested:
            self.order(self.asset, 100)
            self.invested = True
            buy = True
        elif (short_ema < long_ema).all() and self.invested:
            self.order(self.asset, -100)
            self.invested = False
            sell = True
    
        self.record(AAPL=data[self.asset].price,
               short_ema=short_ema[self.asset],
               long_ema=long_ema[self.asset],
               buy=buy,
               sell=sell)
        
if __name__ == '__main__':
    import zipline.utils.factory as zpf
    from datetime import datetime
    import matplotlib.pyplot as plt
    
    data = zpf.load_from_yahoo(stocks=['AAPL'],
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
        results[['short_ema', 'long_ema']].plot(ax=ax1, lw=2.)
        ax1.plot( results.ix[ results.buy].index,  results.short_ema[ results.buy],
                 '^', markersize=10, color='m')
        ax1.plot( results.ix[ results.sell].index,  results.short_ema[ results.sell],
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