# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 15:35:16 2015

@author: mid
"""
import zipline as zp
class DualMovingAverage(zp.TradingAlgorithm):
    def initialize(context):
        # we need to track two moving averages, so we will set
        #these up in the context the .add_transform method 
        # informs zipline to execute a transform on every day 
        # of trading
        
        # the following will set up a MovingAverge transform, 
        # named short_mavg, accessing the .price field of the 
        # data, and a length of 100 days
        context.add_transform(zp.transforms.MovingAverage, 
                              'short_mavg', ['price'],
                              window_length=100)

        # and the following is a 400 day MovingAverage
        context.add_transform(zp.transforms.MovingAverage,
                              'long_mavg', ['price'],
                              window_length=400)

        # this is a flag we will use to track the state of 
        # whether or not we have made our first trade when the 
        # means cross.  We use it to identify the single event 
        # and to prevent further action until the next cross
        context.invested = False

    def handle_data(self, data):
        # access the results of the transforms
        short_mavg = data['AAPL'].short_mavg['price']
        long_mavg = data['AAPL'].long_mavg['price']
        
        # these flags will record if we decided to buy or sell
        buy = False
        sell = False

        # check if we have crossed
        if short_mavg > long_mavg and not self.invested:
            # short moved across the long, trending up
            # buy up to 100 shares
            self.order_target('AAPL', 100)
            # this will prevent further investment until 
            # the next cross
            self.invested = True
            buy = True # records that we did a buy
        elif short_mavg < long_mavg and self.invested:
            # short move across the long, tranding down
            # sell it all!
            self.order_target('AAPL', -100)
            # prevents further sales until the next cross
            self.invested = False
            sell = True # and note that we did sell

        # add extra data to the results of the simulation to 
        # give the short and long ma on the interval, and if 
        # we decided to buy or sell
        self.record(short_mavg=short_mavg,
                    long_mavg=long_mavg,
                    buy=buy,
                    sell=sell)
                    
import zipline.utils.factory as zpf
from datetime import datetime
import matplotlib.pyplot as plt

data = zpf.load_from_yahoo(stocks=['AAPL'],
                           indexes={},
                           start=datetime(1990, 1, 1),
                           end=datetime(2014, 1, 1),
                           adjusted=False)

sub_data = data['1990':'2002-01-01']

results = DualMovingAverage().run(sub_data)

# draw plots of the results
def analyze(data, perf):
    fig = plt.figure() # create the plot
    
    # the top will be a plot of long/short ma vs price
    ax1 = fig.add_subplot(211,  ylabel='Price in $')
    data['AAPL'].plot(ax=ax1, color='r', lw=2.)
    perf[['short_mavg', 'long_mavg']].plot(ax=ax1, lw=2.)

    # the following puts an upward triangle at each point 
    # we decided to buy
    ax1.plot(perf.ix[perf.buy].index, perf.short_mavg[perf.buy],
             '^', markersize=10, color='m')
    # and the following a downward triangle where we sold
    ax1.plot(perf.ix[perf.sell].index, perf.short_mavg[perf.sell],
             'v', markersize=10, color='k')

    # bottom plot is the portfolio value
    ax2 = fig.add_subplot(212, ylabel='Portfolio value in $')
    perf.portfolio_value.plot(ax=ax2, lw=2.)

    # and also has the marks for buy and sell points
    ax2.plot(perf.ix[perf.buy].index, 
             perf.portfolio_value[perf.buy],
             '^', markersize=10, color='m')
    ax2.plot(perf.ix[perf.sell].index, 
             perf.portfolio_value[perf.sell],
             'v', markersize=10, color='k')

    # and set the legend position and size of the result
    plt.legend(loc=0)
    plt.gcf().set_size_inches(14, 10)
    plt.savefig('5104OS_07_19.png', bbox_inches='tight', dpi=300)
    
# visually analyze the results
analyze(sub_data, results)
