# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# Copyright 2014 Quantopian, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Dual Moving Average Crossover algorithm.
This algorithm buys apple once its short moving average crosses
its long moving average (indicating upwards momentum) and sells
its shares once the averages cross again (indicating downwards
momentum).
"""
from zipline.transforms.ta import EMA
#import zipline.transforms.ta as ta
import talib as talib
#from zipline.api import order_target, record, symbol, history, add_history
import zipline as zp

class DualEmaTalib(zp.TradingAlgorithm):       
    def __init__(self, *args, **kwargs):
        super(DualEmaTalib, self).__init__(*args, **kwargs)    #mid 采用super(child,self).method()格式调用某个类的父类的方法。
    def initialize(context):
        # Register 2 histories that track daily prices,
        # one with a 100 window and one with a 300 day window
        context.stocks = context.symbols('AAPL', 'IBM', 'CSCO')
        
        context.add_history(20, '1d', 'price')
        context.add_history(40, '1d', 'price')
        context.i = 0
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
        if context.i < 40:
            return
        # Compute averages
        # history() has to be called with the same params
        # from above and returns a pandas dataframe.
        short_mavg = context.history(20, '1d', 'price').mean()
        long_mavg = context.history(40, '1d', 'price').mean()
    
        # Trading logic
        if short_mavg[context.symbol('AAPL')] > long_mavg[context.symbol('AAPL')]:
            # order_target orders as many shares as needed to
            # achieve the desired number of shares.
            context.order_target(context.symbol('AAPL'), 100)
        elif short_mavg[context.symbol('AAPL')] < long_mavg[context.symbol('AAPL')]:
            context.order_target(context.symbol('AAPL'), 0)
    
        # Save values for later inspection
        context.record(AAPL=data[context.symbol('AAPL')].price,
               short_mavg=short_mavg[context.symbol('AAPL')],
               long_mavg=long_mavg[context.symbol('AAPL')])
    
    def dumpDict(dictStr):
        """"""
        import json
        jsonDumpsIndentStr = json.dumps(dictStr, indent=4,skipkeys = False,default=str,sort_keys=True)
        print (jsonDumpsIndentStr) 





# Note: this function can be removed if running
# this algorithm on quantopian.com
def analyze(context=None, results=None):
    import matplotlib.pyplot as plt
    import logbook
    logbook.StderrHandler().push_application()
    log = logbook.Logger('Algorithm')

    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    results.portfolio_value.plot(ax=ax1)
    ax1.set_ylabel('Portfolio value (USD)')

    ax2 = fig.add_subplot(212)
    ax2.set_ylabel('Price (USD)')

    # If data has been record()ed, then plot it.
    # Otherwise, log the fact that no data has been recorded.
    if ('AAPL' in results and 'short_mavg' in results and
            'long_mavg' in results):
        results['AAPL'].plot(ax=ax2)
        results[['short_mavg', 'long_mavg']].plot(ax=ax2)

        trans = results.ix[[t != [] for t in results.transactions]]
        buys = trans.ix[[t[0]['amount'] > 0 for t in
                         trans.transactions]]
        sells = trans.ix[
            [t[0]['amount'] < 0 for t in trans.transactions]]
        ax2.plot(buys.index, results.short_mavg.ix[buys.index],
                 '^', markersize=10, color='m')
        ax2.plot(sells.index, results.short_mavg.ix[sells.index],
                 'v', markersize=10, color='k')
        plt.legend(loc=0)
    else:
        msg = 'AAPL, short_mavg & long_mavg data not captured using record().'
        ax2.annotate(msg, xy=(0.1, 0.5))
        log.info(msg)

    plt.show()


# Note: this if-block should be removed if running
# this algorithm on quantopian.com
if __name__ == '__main__':
    from datetime import datetime
    import pytz
    from zipline.algorithm import TradingAlgorithm
    from zipline.utils.factory import load_from_yahoo

    # Set the simulation start and end dates.
    start = datetime(2014, 1, 1, 0, 0, 0, 0, pytz.utc)
    end = datetime(2014, 11, 1, 0, 0, 0, 0, pytz.utc)
    # Load price data from yahoo.
    data = load_from_yahoo(stocks=['AAPL', 'IBM', 'CSCO'], 
                           indexes={}, 
                           start=start,
                           end=end)

    '''    '''

    algo = DualEmaTalib(instant_fill=True,
                        capital_base=50000,
                        env=None,
                        sim_params = None,  # 设置有此参数时，start和end不能再设置，否则，显得多余也会运行assert错误
                        #start = algo['start'],
                        #end = algo['end'],
                        data_frequency = 'daily',
                        identifiers=['AAPL', 'IBM', 'CSCO'])   


    # Create and run the algorithm.
    #algo = DualEmaTalib()
    results = algo.run(data).dropna()

    # Plot the portfolio and asset data.
    analyze(results=results)