params={}
dataSource={}
algo={}

dataSource['ip']='192.168.1.100'
dataSource['port']=27017
dataSource['database']='Tushare'

dataSource['symbol']='000001'
dataSource['dateStart']='2013-02-19'
dataSource['dateEnd']='2015-12-31'
dataSource['frequency']='D'

algo['instant_fill']=True
algo['capital_base']=1000


params['dataSource'] = dataSource
params['algo'] = algo
