# -*- coding: utf-8 -*-
if __name__ == '__main__':
    import sys,os
    from PyQt4 import QtCore, QtGui
    app = QtGui.QApplication(sys.argv) 
    
    xpower = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir))
    sys.path.append(xpower)
    
    params={}
    Globals=[]
    dataSource={}
    algo={}
    #-------------------------------------------------------------------------------------------
    # 0)自定义数据获取参数
    dataSource['ip']='192.168.0.212'
    dataSource['port']=27017
    dataSource['database']='Tushare'
    
    dataSource['symbol']='600028'
    dataSource['dateStart']='2015-12-21'
    dataSource['dateEnd']='2015-12-24'
    dataSource['frequency']='D'
    
    # 1)自定义zipline运行参数
    # 1.1)简单类型参数
    # 1.1.1)用户未自定义sim_params对象参数时，系统内部将以以下三参数作为参数生成sim_params
    #       如果用户有自定义sim_params对象参数，系统内部将使用sim_params的定义，而丢弃以下三值
    from datetime import datetime
    import pytz
    import pandas as pd
    algo['capital_base']=1000
    algo['start'] = datetime(2015, 12, 27,1,30 ,tzinfo=pytz.timezone('utc')) # set Shanghai to utc time
    algo['end'] = datetime(2015, 12, 30,7,0, tzinfo=pytz.timezone('utc'))
    
    algo['instant_fill']=True
    algo['data_frequency'] = 'daily'  #data_frequency == 'minute'
    # 1.2)交易日历指定
    from TradingCalendar import shTradingCalendar
    tradingcalendar = shTradingCalendar
    def load_market_data(trading_day=tradingcalendar.trading_day,
                         trading_days=tradingcalendar.trading_days,
                         bm_symbol='^GSPC'):
        """
        Load benchmark returns and treasury yield curves for the given calendar and
        benchmark symbol.
    
        Benchmarks are downloaded as a Series from Yahoo Finance.  Treasury curves
        are US Treasury Bond rates and are downloaded from 'www.federalreserve.gov'
        by default.  For Canadian exchanges, a loader for Canadian bonds from the
        Bank of Canada is also available.
    
        Results downloaded from the internet are cached in
        ~/.zipline/data. Subsequent loads will attempt to read from the cached
        files before falling back to redownload.
    
        Parameters
        ----------
        trading_day : pandas.CustomBusinessDay, optional
            A trading_day used to determine the latest day for which we
            expect to have data.  Defaults to an NYSE trading day.
        trading_days : pd.DatetimeIndex, optional
            A calendar of trading days.  Also used for determining what cached
            dates we should expect to have cached. Defaults to the NYSE calendar.
        bm_symbol : str, optional
            Symbol for the benchmark index to load.  Defaults to '^GSPC', the Yahoo
            ticker for the S&P 500.
    
        Returns
        -------
        (benchmark_returns, treasury_curves) : (pd.Series, pd.DataFrame)
    
        Notes
        -----
    
        Both return values are DatetimeIndexed with values dated to midnight in UTC
        of each stored date.  The columns of `treasury_curves` are:
    
        '1month', '3month', '6month',
        '1year','2year','3year','5year','7year','10year','20year','30year'
        """
        first_date = trading_days[0]
        now = pd.Timestamp.utcnow()
    
        # We expect to have benchmark and treasury data that's current up until
        # **two** full trading days prior to the most recently completed trading
        # day.
        # Example:
        # On Thu Oct 22 2015, the previous completed trading day is Wed Oct 21.
        # However, data for Oct 21 doesn't become available until the early morning
        # hours of Oct 22.  This means that there are times on the 22nd at which we
        # cannot reasonably expect to have data for the 21st available.  To be
        # conservative, we instead expect that at any time on the 22nd, we can
        # download data for Tuesday the 20th, which is two full trading days prior
        # to the date on which we're running a test.
    
        # We'll attempt to download new data if the latest entry in our cache is
        # before this date.
        last_date = trading_days[trading_days.get_loc(now, method='ffill') - 2]
        return None,None
        br = ensure_benchmark_data(
            bm_symbol,
            first_date,
            last_date,
            now,
            # We need the trading_day to figure out the close prior to the first
            # date so that we can compute returns for the first date.
            trading_day,
        )
        tc = ensure_treasury_data(
            bm_symbol,
            first_date,
            last_date,
            now,
        )
        benchmark_returns = br[br.index.slice_indexer(first_date, last_date)]
        treasury_curves = tc[tc.index.slice_indexer(first_date, last_date)]
        return benchmark_returns, treasury_curves
    
    # 1.3)交易环境指定
    '''mid
    TradingEnvironment()类定义交易的环境，包括：
    1.交易日历(哪天交易，哪天不交易)
    2.交易基准数据，包括指数回报，国债回报
    3.交易所时区
    
    这些环境数据若不自定义，系统会默认使用纽交所的数据，而且是实时下载，数据来源有两个，
    若有一个连接不可用时，会导致无限等待。
    所以，这个东西有必要自定义
    另外，若要应用到中国市场，这些数据也必须要自定义
    '''
    from zipline.finance.trading import TradingEnvironment
    algo['env']=TradingEnvironment(load=load_market_data,
                                   #bm_symbol='000001',
                                   exchange_tz="Asia/Shanghai",
                                   max_date=None,
                                   env_trading_calendar = tradingcalendar,
                                   asset_db_path=':memory:') 
   
    # 1.4)参数对象设定
    from zipline.utils.factory import create_simulation_parameters
    algo['sim_params'] = create_simulation_parameters(year=2015,             # start and end overwrites year
                                                      capital_base=1000,
                                                      start = algo['start'],
                                                      end=algo['end'],       # mid end overwrites num_days
                                                      env=algo['env'],
                                                      #num_days=None,
                                                      data_frequency='daily',
                                                      emission_rate='daily'
                                                      )
    #-------------------------------------------------------------------------------------------    
    params['dataSource'] = dataSource
    params['algo'] = algo  
import matplotlib.pyplot as plt
from Algorithms.BuyEveryDay import BuyEveryDay
from DataSources.GetDataFromMongodb import GetDataFromMongodb
from Analyzers.Analyzer01 import Analyzer01
from Analyzers.Analyzer02 import Analyzer02
from Analyzers.Analyzer03 import Analyzer03
from Analyzers.Analyzer04 import Analyzer04
from Analyzers.Analyzer05 import Analyzer05
from Analyzers.PriceScatter import PriceScatter
dataSource = params['dataSource']
algo = params['algo']
 
dataForZipline,dataForCandle = GetDataFromMongodb(dataSource)



def dumpDict(dictStr):
    """"""
    import json
    jsonDumpsIndentStr = json.dumps(dictStr, indent=4,skipkeys = False,default=str,sort_keys=True)
    print (jsonDumpsIndentStr) 
from zipline.algorithm import TradingAlgorithm
algo = BuyEveryDay(instant_fill=algo['instant_fill'],
                   capital_base=algo['capital_base'],
                   env=algo['env'],
                   sim_params = algo['sim_params'],  # 设置有此参数时，start和end不能再设置，否则，显得多余也会运行assert错误
                   #start = algo['start'],
                   #end = algo['end'],
                   data_frequency = algo['data_frequency'])
algo.dumpDict = dumpDict
#dataUtcTime = dataForZipline.tz_localize('Asia/Shanghai').tz_convert('utc')
dataUtcTime = dataForZipline.tz_localize('utc')

result = algo.run(dataUtcTime)
print('----start----result')
#dumpDict(result)
print('---- end ----result')
analyzer = Analyzer05(Globals=Globals)
analyzer.analyze(result,dataForCandle,bDrawText=False)


if __name__ == '__main__':
    sys.exit(app.exec_())