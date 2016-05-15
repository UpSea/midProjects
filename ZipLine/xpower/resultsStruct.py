# -*- coding: utf-8 -*-
'''
following program is in run()
'''
import matplotlib.pyplot as plt
import matplotlib.dates as mpd
import matplotlib.finance as mpf
import numpy as np
import datetime as dt
import pandas
from pandas import Timestamp
a = {
    'daily_perf': 
    {
        'shorts_count': 0, 
        'pnl': 0.0, 
        'ending_cash': 1000.0, 
        'short_value': 0, 
        'portfolio_value': 1000.0, 
        'orders': [], 
        'gross_leverage': 0.0, 
        'long_value': 0, 
        'period_close': Timestamp('2015-12-21 21:00:00+0000', tz='UTC'), 
        'transactions': [], 
        'ending_exposure': 0.0, 
        'period_open': Timestamp('2015-12-21 14:31:00+0000', tz='UTC'), 
        'positions': [], 
        'capital_used': 0.0, 
        'starting_exposure': 0.0, 
        'long_exposure': 0, 
        'returns': 0.0, 
        'starting_cash': 1000, 
        'net_leverage': 0.0, 
        'ending_value': 0.0, 
        'short_exposure': 0, 
        'longs_count': 0, 
        'starting_value': 0.0, 
        'recorded_vars': {}
    }, 
    'capital_base': 1000, 
    'progress': 0.125, 
    'period_start': Timestamp('2015-12-21 01:30:00+0000', tz='UTC'), 
    'cumulative_perf': 
    {
        'shorts_count': 0, 
        'ending_exposure': 0.0, 
        'pnl': 0.0, 
        'short_exposure': 0, 
        'short_value': 0, 
        'ending_cash': 1000.0, 
        'longs_count': 0, 
        'capital_used': 0.0, 
        'period_open': Timestamp('2015-12-21 01:30:00+0000', tz='UTC'), 
        'starting_exposure': 0.0, 
        'long_value': 0, 
        'long_exposure': 0, 
        'returns': 0.0, 
        'starting_cash': 1000, 
        'gross_leverage': 0.0, 
        'net_leverage': 0.0, 
        'ending_value': 0.0, 
        'portfolio_value': 1000.0, 
        'period_close': Timestamp('2015-12-31 01:30:00+0000', tz='UTC'), 
        'starting_value': 0.0}, 
        'period_end': Timestamp('2015-12-31 01:30:00+0000', tz='UTC'), 
        'cumulative_risk_metrics': 
        {
            'sortino': 0.0, 
            'algo_volatility': 0.0, 
            'max_drawdown': 0, 
            'alpha': -0.021999999999999999, 
            'treasury_period_return': 0.021999999999999999, 
            'algorithm_period_return': 0.0, 
            'excess_return': -0.021999999999999999, 
            'sharpe': None, 
            'max_leverage': 0.0, 
            'benchmark_period_return': 0.0077784022432041411, 
            'benchmark_volatility': 0.0, 
            'beta': 0.0, 
            'trading_days': 1, 
            'information': None, 
            'period_label': '2015-12'
        }
}
def dumpDict(dictStr):
    """"""
    import json
    jsonDumpsIndentStr = json.dumps(dictStr, indent=4,skipkeys = False,default=str,sort_keys=True)
    print (jsonDumpsIndentStr) 
dumpDict(a)

b = 8