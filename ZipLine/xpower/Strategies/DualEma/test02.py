import sys,os
from PyQt4 import QtCore, QtGui
app = QtGui.QApplication(sys.argv) 

#xpower = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir))
#sys.path.append(xpower)

params={}
Globals=[]
dataSource={}
algo={}

dataSource['dataProvider']='tushare'
dataSource['storageFormat']='mongodb'
dataSource['symbol']='600028'
dataSource['dateStart']='2015-03-19'
dataSource['dateEnd']='2015-12-31'
dataSource['frequency']='D'

algo['instant_fill']=True
algo['capital_base']=1000

params['dataSource'] = dataSource
params['algo'] = algo  

from TradingCalendar import shTradingCalendar
tradingcalendar = shTradingCalendar    
from zipline.finance.trading import TradingEnvironment
from loaders.yahooLoader import load_market_data
algo['env']=TradingEnvironment(load=load_market_data,
                               #bm_symbol='000001',
                               exchange_tz="Asia/Shanghai",
                               max_date=None,
                               env_trading_calendar = tradingcalendar,
                               asset_db_path=':memory:')   
