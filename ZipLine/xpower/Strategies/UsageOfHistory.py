import zipline.utils.factory as zpf
from datetime import datetime
import matplotlib.pyplot as plt

data = zpf.load_from_yahoo(stocks=['PEP', 'KO'],
                           indexes={},
                           start=datetime(1997, 1, 1),
                           end=datetime(1998, 6, 1),
                           adjusted=True)
#data.plot(figsize=(12,8))

#data['Spread'] = data.PEP - data.KO
#data['1997':].Spread.plot(figsize=(12,8))
#plt.ylabel('Spread')
#plt.axhline(data.Spread.mean())
#plt.show()

import sys
sys.path.append('/home/mid/PythonProjects/xpower')    
from Algorithms.UsageOfHistory import UsageOfHistory
from zipline.algorithm import TradingAlgorithm
algo = UsageOfHistory(instant_fill=True,
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