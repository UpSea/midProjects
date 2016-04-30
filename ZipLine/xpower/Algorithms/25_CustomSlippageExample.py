import zipline.transforms.ta as ta
import zipline.utils.events as zpEvents
import zipline.finance.commission as zpCommission
import zipline.finance.slippage as zpSlippage
import zipline as zp
import logbook
import datetime
import pandas as pd
import logging

def getLog():
    log = logging.getLogger("mid'logger")# 创建一个logger
    log.setLevel(logging.DEBUG)
    fh = logging.FileHandler('test.log')# 创建一个handler，用于写入日志文件
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()# 再创建一个handler，用于输出到控制台
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')# 定义handler的输出格式
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    log.addHandler(fh)# 给logger添加handler
    log.addHandler(ch)
    log.info('A new backtest starts')# 记录一条日志
    return log
log = getLog()
# Our custom slippage model
class PerStockSpreadSlippage(zpSlippage.SlippageModel):

    # We specify the constructor so that we can pass state to this class, but this is optional.
    def __init__(self, spreads):
        # Store a dictionary of spreads, keyed by sid.
        self.spreads = spreads

    def process_order(self, trade_bar, my_order):
        spread = self.spreads[my_order.sid]
   
        # In this model, the slippage is going to be half of the spread for 
        # the particular stock
        slip_amount = spread / 2
        # Compute the price impact of the transaction. Size of price impact is 
        # proprotional to order size. 
        # A buy will increase the price, a sell will decrease it. 
        new_price = trade_bar.price + (slip_amount * my_order.direction)

        log.info('executing order ' + str(trade_bar.sid) + ' stock bar price: ' + \
                 str(trade_bar.price) + ' and trade executes at: ' + str(new_price))

        # Create the transaction using the new price we've calculated.
        return zpSlippage.create_transaction(
            trade_bar,
            my_order,
            new_price,
            my_order.amount
        )
class DualEmaTalib(zp.TradingAlgorithm):       
    def __init__(self, *args, **kwargs):
        super(DualEmaTalib, self).__init__(*args, **kwargs)    #mid 采用super(child,self).method()格式调用某个类的父类的方法。
    def initialize(context):
        # Provide the bid-ask spread for each of the securities in the universe.
        '''
        以下两种方式，是对已有数据的不同获取方式
        symbol方式通过名称获取
        sid方式通过序号获取
        security = context.symbol('XLY')
        security = context.sid(0)
        '''
        spreads = {context.symbol('XLY'): 0.05,context.symbol('XLF'): 0.08}
        # Initialize slippage settings given the parameters of our model
        context.set_slippage(PerStockSpreadSlippage(spreads))
    def handle_data(context, data):
        # We want to own 100 shares of each stock in our universe
        for sid in data:
            stock = context.sid(sid)
            stockSymbol = stock.symbol
            stockPrice = data[sid].price
            
            context.order_target(stock, 100)
            log.info('placing market order for ' + str(stockSymbol) + ' at price ' \
                         + str(stockPrice))       
if __name__ == '__main__':
    import sys
    sys.path.append('/home/mid/PythonProjects/xpower')      
    
    import zipline.utils.factory as zpf
    from datetime import datetime
    import matplotlib.pyplot as plt
    
    data = zpf.load_from_yahoo(stocks=['XLY',
                                       'XLF'],
                               indexes={},
                               start=datetime(2015, 1, 1),
                               end=datetime(2016, 3, 5),
                               adjusted=True)
    algo = DualEmaTalib(instant_fill=False,
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
        data.plot(ax=ax1, color='r', lw=2.)
        '''
        results[['stock_price', 'average_price']].plot(ax=ax1, lw=2.)
        ax1.plot( results.ix[ results.buy].index,  results.average_price[ results.buy],
                 '^', markersize=10, color='m')
        ax1.plot( results.ix[ results.sell].index,  results.average_price[ results.sell],
                 'v', markersize=10, color='k')
        '''
        ax2 = fig.add_subplot(212, ylabel='Portfolio value in $')        
        results.portfolio_value.plot(ax=ax2, lw=2.)
        '''
        ax2.plot( results.ix[ results.buy].index,
                  results.portfolio_value[ results.buy],
                 '^', markersize=10, color='m')
        ax2.plot( results.ix[ results.sell].index,
                  results.portfolio_value[ results.sell],
                 'v', markersize=10, color='k')        
        '''
        plt.legend(loc=0)
        plt.gcf().set_size_inches(14, 10)    
    algo.dumpDict = dumpDict
    results = algo.run(data)
    analyze(data,results)
    plt.show()
