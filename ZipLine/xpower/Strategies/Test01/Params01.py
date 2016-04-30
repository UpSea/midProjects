params={}
dataSource={}
algo={}

dataSource['ip']='192.168.1.100'
dataSource['port']=27017
dataSource['database']='Tushare'

dataSource['symbol']='600028'
dataSource['dateStart']='2015-06-01'
dataSource['dateEnd']='2015-07-01'
dataSource['frequency']='D'

algo['instant_fill']=True
algo['capital_base']=10


params['dataSource'] = dataSource
params['algo'] = algo



