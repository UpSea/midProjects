# -*- coding: utf-8 -*-
import zipline as zp
class BuyEveryDay(zp.TradingAlgorithm):       
    def __init__(self, *args, **kwargs):
        super(BuyEveryDay, self).__init__(*args, **kwargs)
        print('BuyEveryDay.__init__()')
    def initialize(self):
        print("<---BuyEveryDay.initialize() start")
        print(self)
        self.sid = self.symbol('AAPL')      #mid 传入algo的dataFrame必须要有此处symbol中所指定的symbol列，即必须要有AAPL列
        self.amount = 100
        self.data = []
        print("--->BuEveryDay.initialize() end")
    def handle_data(self,data):
        print('----BuyEveryDay.handle_data().',data[0]['dt'])
        self.data.append(data[0]['dt'])             #mid collect all data
        self.order(self.sid,self.amount)            #mid open 1 long position.
        self.record(AAPL=data[self.sid].price)      #mid add one column named 'AAPL' to returns of Algorithm.run()                   
if __name__ == '__main__':
    import zipline.utils.factory as zpf
    from datetime import datetime
    import matplotlib.pyplot as plt
    
    data = zpf.load_from_yahoo(stocks=['AAPL'],
                               indexes={},
                               start=datetime(1997, 1, 1),
                               end=datetime(1998, 6, 1),
                               adjusted=True)
    algo = BuyEveryDay(instant_fill=True,
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
    algo.dumpDict = dumpDict
    result = algo.run(data)
    result['pnl'].plot()
    #result['portfolio_value'].plot()
    plt.show()