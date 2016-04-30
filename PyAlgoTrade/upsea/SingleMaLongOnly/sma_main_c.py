from pyalgotrade import plotter
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.stratanalyzer import returns
import sma_crossover
def analyzer(strategy):
    SPlotter = plotter.StrategyPlotter(strategy)
    def aaa():#mid这个市有问题的，不知有何功能
        IPlotter = plotter.InstrumentSubplot("orcl",True)
        IPlotter.addDataSeries("SssssssMA", strategy.getSMA())
    aaa()
    SPlotter.getInstrumentSubplot("orcl").addDataSeries("SMA", strategy.getSMA())
    # Plot the simple returns on each bar.
    SPlotter.getOrCreateSubplot("returns").addDataSeries("Simple returns", returnsAnalyzer.getReturns())
    def addCallBack():
        # mid 使用默认绘图类绘制自定义数据,此处是LineMarker
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

# 1)策略配置----------------------------------------------------------------------------------
# 1.1) 准备数据
feed = getData()
# 1.2) 定义策略
myStrategy = sma_crossover.SMACrossOver(feed, "orcl", 20)
# 1.3) 策略结果接收数据结构定义
returnsAnalyzer = returns.Returns()
myStrategy.attachAnalyzer(returnsAnalyzer)
# 1.4) 策略结果图形化关联
spPlooter = analyzer(myStrategy)

# 2)策略运行----------------------------------------------------------------------------------
myStrategy.run()

# 3)运行结果展示------------------------------------------------------------------------------
myStrategy.info("Final portfolio value: $%.2f" % myStrategy.getResult())
# Plot the strategy.
if(True):#自定义方式获取figure，并对其进行设置
    import matplotlib.pyplot as plt
    fig = spPlooter.buildFigure()
    fig.tight_layout()    
    plt.show()
else:#使用pyalgo的方式绘制
    spPlooter.plot()