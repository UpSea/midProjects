from Mongo_00_Wrapper_Tushare import ClientTushare
from datetime import datetime

if __name__ == '__main__':
    # 1)connect to Tushare data collection
    connect = ClientTushare('192.168.1.100', 27017)
    connect.use('HistoryDataCenter')    #database
    connect.setCollection('Tushare')    #table
    
    # 2)download history data
    symbol = '600028'
    strStart = '2015-01-01'
    dateEnd = datetime.now()
    strEnd = dateEnd.strftime('%Y-%m-%d')  
    frequency = 'D'
    history = connect.retrive(symbol,strStart,strEnd,frequency)
    
    print('---------') 
    
    print(history.head(20))
    
    print('---------')
    print('ok')    
    
    
  