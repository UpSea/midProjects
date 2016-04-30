

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
class DualEmaTalib(zp.TradingAlgorithm):       
    def __init__(self, *args, **kwargs):
        super(DualEmaTalib, self).__init__(*args, **kwargs)    #mid 采用super(child,self).method()格式调用某个类的父类的方法。
    # This algorithm contains the basic framework for backtesting and
    # deploying a live algorithm with Robinhood. This does 3 things:
    # (1) Simulates a T+3 wait while cash is settling, not placing
    #     any trades in the meanwhile. This should only be used
    #     for backtesting.
    # (2) Use the `set_long_only()` trading guard to insure that any
    #     algorithm deployed with Robinhood only contains long
    #     positions
    # (3) Include `do_unsettled_funds_exist` that will replicate the
    #     functionality found in (1) but only for Live Trading. Once
    #     you're ready to deploy, you can comment out all mentions of
    #     `check_last_sale` and `cash_settlement_date` and use
    #     `do_unsettled_funds_exist` instead!
    
    def initialize(context):
        # Set a trading guard that will prevent any short positions
        # from being placed. This is to insure that algorithms that
        # depend on short positions are not accidently deployed.
        context.set_long_only()
    
        # Keeping track of the last sale that you have.
        context.last_sale = None
        
        # Just a simple variable to demonstrate `context.last_sale`,
        # `cash_settlement_date`, and `check_last_sale`
        context.trading_days = 0
    
    def handle_data(context, data):
        # Because most Robinhood accounts are cash accounts,
        # trades(and most other brokerages) settle 
        # on a T+3 settlement date. This snippet of code prevents
        # a trade from happening when you still have unsettled cash
        # by checking if total cash (settled & unsettled) matches your
        # settled cash amount.
    
        # [IMPORTANT] During backtests, `settled_cash` will always equal
        # `cash`. In order to simulate a similar check, please also 
        # incorporate `simulate_cash_settlement` in handle data as you will
        # see in this algorithm.
        if context.do_unsettled_funds_exist():
            # For live trading only
            return
    
        # `cash_settlement_date` simulates a T+3 settlement date. This
        # should be used at the beginning of any handle_data or method
        # used for schedule_function that places orders. At the end of
        # of that method should be `check_last_sale`. Only for
        # backtesting purposes!
        if context.cash_settlement_date():
            log.info("Unsettled Cash Simulated")
        else:
            # You can see the simulation in prgoress here.
            # On day 0, it will order 5 shares of AAPL
            # On day 1, it will order -1 shares and the proceeds
            # from the sale will be unsettled till day 4.
            # On day 4, you will be able to place another sale.
            sid = context.symbol('CERN')
            if context.trading_days == 0:
                log.info("Day 0")
                context.order(sid, 5)
            if context.trading_days == 1:
                log.info("Day 1")
                context.order(sid, -1)
            if context.trading_days == 2:
                # Day 2 should not log.
                log.info("Day 2")
                context.order(sid, -1)
            if context.trading_days == 4:
                log.info("Day 4")
                context.order(sid, -1)
      
        context.trading_days += 1
        
        # `check_last_sale` is what `cash_settlement_date` needs in
        # order to work properly. Only for backtesting purposes!
        context.check_last_sale()   
    def do_unsettled_funds_exist(context):
        """
        For Robinhood users. In order to prevent you from attempting
        to trade on unsettled cash (settlement dates are T+3) from
        sale of proceeds. You can use this snippet of code which
        checks for whether or not you currently have unsettled funds
        
        To only be used for live trading!
        """
        if context.portfolio.cash != context.account.settled_cash:
            return True
    
    def check_last_sale(context):
        """
        To be used at the end of each bar. This checks if there were
        any sales made and sets that to `context.last_sale`.
        `context.last_sale` is then used in `cash_settlement_date` to
        simulate a T+3 Cash Settlement date
        
        To only be used for backtesting!
        """
        open_orders = context.get_open_orders()
        most_recent_trade = []
        # If there are open orders check for the most recent sale
        if open_orders:
            for sec, order in open_orders.items():
                for oo in order:
                    if oo.amount < 0:
                        most_recent_trade.append(oo.created)
        if len(most_recent_trade) > 0:
            context.last_sale = max(most_recent_trade)
        
    def cash_settlement_date(context):
        """
        This will simulate Robinhood's T+3 cash settlement. If the 
        most recent sale is less than 3 trading days from the current
        day, assume we have unsettled funds and exit
        
        To only be used for backtesting!
        """
        if context.last_sale and (context.get_datetime() - context.last_sale).days < 3:
            return True    
    def dumpDict(self,dictStr):
        """"""
        import json
        jsonDumpsIndentStr = json.dumps(dictStr, indent=4,skipkeys = False,default=str,sort_keys=True)
        print (jsonDumpsIndentStr) 
if __name__ == '__main__':
    import sys,os
    xpower = '/home/mid/PythonProjects/xpower'  
    xpower = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir))
    sys.path.append(xpower)
    import zipline.utils.factory as zpf
    from datetime import datetime
    import matplotlib.pyplot as plt
    
    data = zpf.load_from_yahoo(stocks=['CERN', 'DLTR'],
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

    def analyze(data,  results):
        fig = plt.figure()
        ax1 = fig.add_subplot(211, ylabel='Price in $')
        data.plot(ax=ax1, color='r', lw=2.)
        '''
        results[['perc_stock_0', 'perc_stock_1']].plot(ax=ax1, lw=2.)
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
    results = algo.run(data)
    analyze(data,results)
    plt.show()
