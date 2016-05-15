# -*- coding: utf-8 -*-
"""
    Trading Strategy using Fundamental Data
    
    1. Filter the top 50 companies by market cap 
    2. Find the top two sectors that have the highest average PE ratio
    3. Every month exit all the positions before entering new ones at the month
    4. Log the positions that we need 
"""
import numpy as np
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
    def initialize(context):
        # Dictionary of stocks and their respective weights
        context.stock_weights = {}
        # Count of days before rebalancing
        context.days = 0
        # Number of sectors to go long in
        context.sect_numb = 2
        
        # Sector mappings
        context.sector_mappings = {
           101.0: "Basic Materials",
           102.0: "Consumer Cyclical",
           103.0: "Financial Services",
           104.0: "Real Estate",
           205.0: "Consumer Defensive",
           206.0: "Healthcare",
           207.0: "Utilites",
           308.0: "Communication Services",
           309.0: "Energy",
           310.0: "Industrials",
           311.0: "Technology"
        }
        # Rebalance monthly on the first day of the month at market open
        context.schedule_function(context.rebalance,
                          date_rule=zpEvents.date_rules.month_start(),
                          time_rule=zpEvents.time_rules.market_open())    
    def before_trading_start(context, data): 
        """
          Called before the start of each trading day. 
          It updates our universe with the
          securities and values found from get_fundamentals.
        """
        
        num_stocks = 50
        
        # Setup SQLAlchemy query to screen stocks based on PE ratio
        # and industry sector. Then filter results based on 
        # market cap and shares outstanding.
        # We limit the number of results to num_stocks and return the data
        # in descending order.
        此程序get_fundamentals()函数需要本地自定义
        fundamental_df = get_fundamentals(
            query(
                # put your query in here by typing "fundamentals."
                fundamentals.valuation_ratios.pe_ratio,
                fundamentals.asset_classification.morningstar_sector_code
            )
            .filter(fundamentals.valuation.market_cap != None)
            .filter(fundamentals.valuation.shares_outstanding != None)
            .order_by(fundamentals.valuation.market_cap.desc())
            .limit(num_stocks)
        )
    
        # Find sectors with the highest average PE
        sector_pe_dict = {}
        for stock in fundamental_df:
            sector = fundamental_df[stock]['morningstar_sector_code']
            pe = fundamental_df[stock]['pe_ratio']
            
            # If it exists add our pe to the existing list. 
            # Otherwise don't add it.
            if sector in sector_pe_dict:
                sector_pe_dict[sector].append(pe)
            else:
                sector_pe_dict[sector] = []
        
        # Find average PE per sector
        sector_pe_dict = dict([(sectors, np.average(sector_pe_dict[sectors])) 
                                   for sectors in sector_pe_dict if len(sector_pe_dict[sectors]) > 0])
        
        # Sort in ascending order
        sectors = sorted(sector_pe_dict, key=lambda x: sector_pe_dict[x], reverse=True)[:context.sect_numb]
        
        # Filter out only stocks with that particular sector
        context.stocks = [stock for stock in fundamental_df
                          if fundamental_df[stock]['morningstar_sector_code'] in sectors]
        
        # Initialize a context.sectors variable
        context.sectors = [context.sector_mappings[sect] for sect in sectors]
    
        # Update context.fundamental_df with the securities (and pe_ratio) that we need
        context.fundamental_df = fundamental_df[context.stocks]
        
        
        update_universe(context.fundamental_df.columns.values)   
        
        
    def create_weights(context, stocks):
        """
            Takes in a list of securities and weights them all equally 
        """
        if len(stocks) == 0:
            return 0 
        else:
            weight = 1.0/len(stocks)
            return weight
            
    def handle_data(context, data):
        """
          Code logic to run during the trading day.
          handle_data() gets called every bar.
        """
    
        # track how many positions we're holding
        record(num_positions = len(context.portfolio.positions))
    def rebalance(self,context, data):
        # Exit all positions before starting new ones
        for stock in context.portfolio.positions:
            if stock not in context.fundamental_df and stock in data:
                order_target_percent(stock, 0)
        log.info("The two sectors we are ordering today are %r" % context.sectors)
        # Create weights for each stock
        weight = create_weights(context, context.stocks)
        # Rebalance all stocks to target weights
        for stock in context.fundamental_df:
            if stock in data:
                if weight != 0:
                    log.info("Ordering %0.0f%% percent of %s in %s" 
                             % (weight * 100, 
                                stock.symbol, 
                                context.sector_mappings[context.fundamental_df[stock]['morningstar_sector_code']]))
                order_target_percent(stock, weight)      
       
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
    
