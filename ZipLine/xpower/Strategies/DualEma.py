if __name__ == '__main__':
    import sys,os
    from PyQt4 import QtCore, QtGui
    app = QtGui.QApplication(sys.argv) 
    
    xpower = '/home/mid/PythonProjects/xpower'  
    xpower = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir))
    sys.path.append(xpower)  
    
    params={}
    Globals=[]
    dataSource={}
    algo={}
    
    dataSource['ip']='192.168.1.100'
    dataSource['port']=27017
    dataSource['database']='Tushare'
    
    dataSource['symbol']='000001'
    dataSource['dateStart']='2015-02-19'
    dataSource['dateEnd']='2015-12-31'
    dataSource['frequency']='D'
    
    algo['instant_fill']=True
    algo['capital_base']=1000
    
    params['dataSource'] = dataSource
    params['algo'] = algo  
    
import matplotlib.pyplot as plt
from Algorithms.DualEma_talib import DualEmaTalib
from DataSources.GetDataFromMongodb import GetDataFromMongodb
from Analyzers.Analyzer01 import Analyzer01
from Analyzers.Analyzer02 import Analyzer02
from Analyzers.Analyzer03 import Analyzer03
from Analyzers.Analyzer04 import Analyzer04
from Analyzers.Analyzer05 import Analyzer05

dataSource = params['dataSource']
algo = params['algo']

dataForZipline,dataForCandle = GetDataFromMongodb(dataSource)
dataUtcTime = dataForZipline.tz_localize('utc')
algo = DualEmaTalib(instant_fill=algo['instant_fill'],capital_base=algo['capital_base'])

def dumpDict(dictStr):
    """"""
    import json
    jsonDumpsIndentStr = json.dumps(dictStr, indent=4,skipkeys = False,default=str,sort_keys=True)
    print (jsonDumpsIndentStr) 
algo.dumpDict = dumpDict
result = algo.run(dataUtcTime)



fig = plt.figure()




analyzer = Analyzer02(fig=fig)
analyzer.analyze(result,dataForCandle,bDrawText=False)




if __name__ == '__main__':
    sys.exit(app.exec_())