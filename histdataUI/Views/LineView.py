# -*- coding: utf-8 -*-
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt4 import QtGui,QtCore

class GraphBase2d(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)

        self.compute_initial_figure()

        #
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass
class GraphSin(GraphBase2d):
    """Simple canvas with a sine plot."""
    def compute_initial_figure(self):
        self.drawGraph()
        
    def drawGraph(self):
        from numpy import arange, sin, pi
        t = arange(0.0, 30.0, 0.01)
        s = sin(2*pi*t)
        self.axes.plot(t, s)
        
class MyDialog(QtGui.QDialog):  
    def __init__(self,dataForCandle=None, parent=None):  
        super(MyDialog, self).__init__(parent)  
        # 1) set mainlayout
        layout = QtGui.QHBoxLayout()  
        self.setLayout(layout)     
        # 5) add candleView to mainlayout
        canvas = GraphSin()        
        layout.addWidget(canvas)
if __name__ == '__main__':
    import os,sys        
    app = QtGui.QApplication([]) 
    myWindow = MyDialog()  
    myWindow.show()    
    
    sys.exit(app.exec_())
                 