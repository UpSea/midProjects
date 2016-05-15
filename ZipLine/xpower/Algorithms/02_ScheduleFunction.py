# -*- coding: utf-8 -*-
import zipline.transforms.ta as ta
import zipline.utils.events as zpEvents
import zipline.finance.commission as zpCommission
import zipline.finance.slippage as zpSlippage
import zipline as zp
import logbook
import datetime
import pandas as pd
''' mid 2016-3-16 18:27
此程序来自Quantopian同名程序
schedule_function是在handle_data之外另外增加一些事件处理程序
第一个参数指明处理函数
第二第三参数指明处理事件的时间
此程序的逻辑是：initialize()中确定一个目标比例
每周一按此比例对持仓进行重新调整，以与目标比例一致
'''
import logging
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

class DualEmaTalib(zp.TradingAlgorithm):       
    def __init__(self, *args, **kwargs):
        super(DualEmaTalib, self).__init__(*args, **kwargs)    #mid 采用super(child,self).method()格式调用某个类的父类的方法。
    def initialize(self):
        # This initialize function sets any data or variables 
        # that you'll use in your algorithm. 
        # You'll also want to define any parameters or values 
        # you're going to use.
    
        # In our example, we're looking at 9 sector ETFs.  
        self.secs = self.symbols('XLY',  # XLY Consumer Discrectionary SPDR Fund   
                               'XLF',  # XLF Financial SPDR Fund  
                               'XLK')  # XLU Utilities SPRD Fund
    
        # This variable is used to manage leverage
        self.weights = 0.99/len(self.secs)
    
        # These are the default commission and slippage settings.  Change them to fit your
        # brokerage fees. These settings only matter for backtesting.  When you trade this 
        # algorithm, they are moot - the brokerage and real market takes over.
        self.set_commission(zpCommission.PerTrade(cost=0.03))
        self.set_slippage(zpSlippage.VolumeShareSlippage(volume_limit=0.25, price_impact=0.1))
    
        # Rebalance every day (or the first trading day if it's a holiday).
        # At 11AM ET, which is 1 hour and 30 minutes after market open.
        # mid 
        '''
        示例中，rebalance()和has_orders()都是按独立函数的方式提供
        rebalance()需要两参数，has_orders()需要一个参数
        将其改编成成员函数之后，需要添加多一个参数self
        '''
        self.schedule_function(self.rebalance,
                            zpEvents.date_rules.week_start(days_offset=0),            #mid 每周的第days_offset出发一个调用rebalance的event
                            zpEvents.time_rules.market_open(hours = 1, minutes = 30)) #mid 市场开盘时间+hours+minutes出发event       
    def handle_data(self, data):
        pass
    def rebalance(self,context, data):
        # Do nothing if there are open orders:
        if self.has_orders(context):
            print('has open orders - doing nothing!')
            return
    
        # Do the rebalance. Loop through each of the stocks and order to the target
        # percentage.  If already at the target, this command doesn't do anything.
        # A future improvement could be to set rebalance thresholds.
        for sec in context.secs:
            context.order_target_percent(sec, context.weights, limit_price=None, stop_price=None)
    
        # Get the current exchange time, in the exchange timezone 
        exchange_time = pd.Timestamp(context.get_datetime()).tz_convert('US/Eastern')
        log.info("Rebalanced to target portfolio weights at %s" % str(exchange_time))   
    def has_orders(self,context):
        # Return true if there are pending orders.
        has_orders = False
        for sec in context.secs:
            orders = context.get_open_orders(sec)
            if orders:
                for oo in orders:                  
                    message = 'Open order for {amount} shares in {stock}'  
                    message = message.format(amount=oo.amount, stock=sec)  
                    logbook.log.info(message)
    
                has_orders = True
        return has_orders         
if __name__ == '__main__':
    import sys
    sys.path.append('/home/mid/PythonProjects/xpower')      
    
    import zipline.utils.factory as zpf
    from datetime import datetime
    import matplotlib.pyplot as plt
    
    data = zpf.load_from_yahoo(stocks=['XLY',
                                       'XLF',  
                                       'XLK'],
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