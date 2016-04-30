from zipline.api import order, record, symbol
# Import exponential moving average from talib wrapper
from zipline.transforms.ta import EMA


def initialize(context):
    context.asset = symbol('AAPL')

    # Add 2 mavg transforms, one with a long window, one with a short window.
    context.short_ema_trans = EMA(timeperiod=20)
    context.long_ema_trans = EMA(timeperiod=40)

    # To keep track of whether we invested in the stock or not
    context.invested = False


def handle_data(context, data):
    short_ema = context.short_ema_trans.handle_data(data)
    long_ema = context.long_ema_trans.handle_data(data)
    if short_ema is None or long_ema is None:
        return

    buy = False
    sell = False

    if (short_ema > long_ema).all() and not context.invested:
        order(context.asset, 100)
        context.invested = True
        buy = True
    elif (short_ema < long_ema).all() and context.invested:
        order(context.asset, -100)
        context.invested = False
        sell = True

    record(AAPL=data[context.asset].price,
           short_ema=short_ema[context.asset],
           long_ema=long_ema[context.asset],
           buy=buy,
           sell=sell)


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
    if 'AAPL' in results and 'short_ema' in results and 'long_ema' in results:
        results[['AAPL', 'short_ema', 'long_ema']].plot(ax=ax2)

        ax2.plot(results.ix[results.buy].index, results.short_ema[results.buy],
                 '^', markersize=10, color='m')
        ax2.plot(results.ix[results.sell].index,
                 results.short_ema[results.sell],
                 'v', markersize=10, color='k')
        plt.legend(loc=0)
        plt.gcf().set_size_inches(18, 8)
    else:
        msg = 'AAPL, short_ema and long_ema data not captured using record().'
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
    data = load_from_yahoo(stocks=['AAPL'], indexes={}, start=start,
                           end=end)

    # Create and run the algorithm.
    algo = TradingAlgorithm(initialize=initialize, handle_data=handle_data,
                            identifiers=['AAPL'])
    results = algo.run(data).dropna()

    # Plot the portfolio and asset data.
    analyze(results=results)