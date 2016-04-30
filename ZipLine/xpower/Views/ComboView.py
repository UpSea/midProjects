from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from Strategies.Strategy_01_BuyApple import prepareData
from Algorithms.Algorithm_BuyOneEveryDay import BuyOneEveryDay
import matplotlib.pyplot as plt
from Analyzers.Analyzer01 import Analyzer01
from Analyzers.Analyzer02 import Analyzer02

class ComboView(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        dataForZipline,dataForCandle = prepareData()

        algo = BuyOneEveryDay(instant_fill=True,capital_base=10)
        result = algo.run(dataForZipline)
        
        fig = plt.figure()
        analyzer = Analyzer01(fig=fig)
        analyzer.analyze(result,dataForCandle)        

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)