# -*- coding: utf-8 -*-
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
    def initialize(context):
        context.stocks = context.symbols('CERN', 'DLTR') 
    def handle_data(context, data):
        # This will order as many shares as needed to
        # achieve the desired portfolio allocation.
        # In our case, we end up with 20% allocation for
        # one stock and 80% allocation for the other stock.
        context.order_target_percent(context.symbol('CERN'), .2)
        context.order_target_percent(context.symbol('DLTR'), .8)
    
        # Plot portfolio allocations
        pv = float(context.portfolio.portfolio_value)
        portfolio_allocations = []
        for stock in context.stocks:
            pos = context.portfolio.positions[stock]
            portfolio_allocations.append(pos.last_sale_price * pos.amount / pv * 100)
    
        context.record(perc_stock_0=portfolio_allocations[0],
               perc_stock_1=portfolio_allocations[1])      
    def dumpDict(self,dictStr):
        """"""
        import json
        jsonDumpsIndentStr = json.dumps(dictStr, indent=4,skipkeys = False,default=str,sort_keys=True)
        print (jsonDumpsIndentStr) 
if __name__ == '__main__':
    import sys
    sys.path.append('/home/mid/PythonProjects/xpower')      
    
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
