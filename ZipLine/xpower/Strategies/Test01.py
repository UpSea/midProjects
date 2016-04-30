# %% 00
import sys
sys.path.append('/home/mid/PythonProjects/xpower')

import matplotlib.pyplot as plt
from Algorithms.BuyEveryDay import BuyEveryDay
from Analyzers.Analyzer01 import Analyzer01
from Analyzers.Analyzer02 import Analyzer02
from DataSources.GetDataFromMongodb import GetDataFromMongodb

# %% 02
dataSource = params['dataSource']
algo = params['algo']

fig = plt.figure()   
dataForZipline,dataForCandle = GetDataFromMongodb(dataSource)
algo = BuyEveryDay(instant_fill=algo['instant_fill'],capital_base=algo['capital_base'])
result = algo.run(dataForZipline)
analyzer = Analyzer01(fig=fig)
analyzer.analyze(result,dataForCandle,bDrawText=False)
plt.show()