from zipline.api import order, record, symbol
from datetime import datetime
from zipline.algorithm import TradingAlgorithm
from zipline.utils.factory import load_from_yahoo
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pytz

def initialize(context):
    pass
def handle_data(context, data):
    order(symbol('AAPL'), 10)
    record(AAPL=data[symbol('AAPL')].price)
def analyze(context=None, results=None):
    # Plot the portfolio and asset data.
    ax1 = plt.subplot(211)
    results.portfolio_value.plot(ax=ax1)
    ax1.set_ylabel('Portfolio value (USD)')
    ax2 = plt.subplot(212, sharex=ax1)
    results.AAPL.plot(ax=ax2)
    ax2.set_ylabel('AAPL price (USD)')

    # Show the plot.
    plt.gcf().set_size_inches(18, 8)
    plt.show()
    
# Set the simulation start and end dates
start = datetime(2014, 1, 1, 0, 0, 0, 0, pytz.utc)
end = datetime(2014, 11, 1, 0, 0, 0, 0, pytz.utc)

# Load price data from yahoo.
data = load_from_yahoo(stocks=['AAPL'], indexes={}, start=start,end=end)


# %% 根据字符串数组构造Datetime
strDate = ['2015-01-05', '2015-01-06', '2015-01-07', '2015-01-08', '2015-01-09',
           '2015-01-12', '2015-01-13', '2015-01-14', '2015-01-15', '2015-01-16']
date = pd.to_datetime(strDate)
data = pd.DataFrame(np.random.randn(10),index = date)
#%% 人工构建Datetime
longer_ts = pd.Series(np.random.randn(100),
                      index = pd.date_range('1/1/2000',periods = 100,tz = 'UTC',name = 'Date'),name='AAPL')

data = pd.DataFrame(longer_ts)

# Create and run the algorithm.
algo = TradingAlgorithm(initialize=initialize, handle_data=handle_data,identifiers=['AAPL'])
results = algo.run(data)
analyze(results=results)