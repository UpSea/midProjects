from pyalgotrade import plotter
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.stratanalyzer import returns
import sma_crossover
def analyzer(strategy):
    SPlotter = plotter.StrategyPlotter(strategy)
    def aaa():#mid�����������ģ���֪�кι���
        IPlotter = plotter.InstrumentSubplot("orcl",True)
        IPlotter.addDataSeries("SssssssMA", strategy.getSMA())
    aaa()
    SPlotter.getInstrumentSubplot("orcl").addDataSeries("SMA", strategy.getSMA())
    # Plot the simple returns on each bar.
    SPlotter.getOrCreateSubplot("returns").addDataSeries("Simple returns", returnsAnalyzer.getReturns())
    def addCallBack():
        # mid ʹ��Ĭ�ϻ�ͼ������Զ�������,�˴���LineMarker
        def midBars(bars):
            midOpen = bars["orcl"].getOpen()
            midClose = bars["orcl"].getClose()
            print midOpen
            return midOpen
        SPlotter.getOrCreateSubplot("orders").addCallback("mid's callback",midBars,plotter.LineMarker)    
    def addDataSeries():
        feedDataSeries = feed.getDataSeries()
        feedDataSerie = feedDataSeries.getCloseDataSeries()    
        SPlotter.getOrCreateSubplot("orders02").addDataSeries("mid's dataSeries",feedDataSerie,plotter.LineMarker)
    addCallBack()
    addDataSeries()
    return SPlotter
def getData():
    feed = yahoofeed.Feed()
    feed.addBarsFromCSV("orcl", "orcl-2000.csv")  
    return feed

# 1)��������----------------------------------------------------------------------------------
# 1.1) ׼������
feed = getData()
# 1.2) �������
myStrategy = sma_crossover.SMACrossOver(feed, "orcl", 20)
# 1.3) ���Խ���������ݽṹ����
returnsAnalyzer = returns.Returns()
myStrategy.attachAnalyzer(returnsAnalyzer)
# 1.4) ���Խ��ͼ�λ�����
spPlooter = analyzer(myStrategy)

# 2)��������----------------------------------------------------------------------------------
myStrategy.run()

# 3)���н��չʾ------------------------------------------------------------------------------
myStrategy.info("Final portfolio value: $%.2f" % myStrategy.getResult())
# Plot the strategy.
if(True):#�Զ��巽ʽ��ȡfigure���������������
    import matplotlib.pyplot as plt
    fig = spPlooter.buildFigure()
    fig.tight_layout()    
    plt.show()
else:#ʹ��pyalgo�ķ�ʽ����
    spPlooter.plot()