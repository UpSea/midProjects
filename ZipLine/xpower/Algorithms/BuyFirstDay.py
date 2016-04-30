import zipline as zp
class BuyFirstDay(zp.TradingAlgorithm):       
    def __init__(self, *args, **kwargs):
        self.first = True
        super(BuyFirstDay, self).__init__(*args, **kwargs)
    def initialize(self):
        print("---> initialize")
        print(self)
        print("<--- initialize")
    def handle_data(self, data):
        if self.first:
            self.order(self.symbol('AAPL'), 1)                      #mid open 1 long position.
            self.first = False            
        self.record(AAPL=data[self.symbol('AAPL')].price)    #mid add one column named 'AAPL' to returns of Algorithm.run()                   
if __name__ == '__main__':
    import sys
    sys.path.append('/home/mid/PythonProjects/xpower')      
    
    import zipline.utils.factory as zpf
    from datetime import datetime
    import matplotlib.pyplot as plt
    
    data = zpf.load_from_yahoo(stocks=['AAPL'],
                               indexes={},
                               start=datetime(1997, 1, 1),
                               end=datetime(1998, 6, 1),
                               adjusted=True)
    algo = BuyFirstDay(instant_fill=True,
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