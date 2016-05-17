# -*- coding: utf-8 -*-
from PyQt4 import QtGui,QtCore
import os
import matplotlib.pyplot as plt
from Views.HistoryCandleView import HistoryCandleView

class StrategyEditorView(QtGui.QDialog):
    def __init__(self,parent=None):
        super(StrategyEditorView,self).__init__(parent)
        self.setWindowTitle(self.tr("DataManager"))
        # 1) creates     layout

        layout = QtGui.QVBoxLayout()
        layoutTop = QtGui.QHBoxLayout()
        layout.addLayout(layoutTop)
        self.setLayout(layout)        
        self.setWindowTitle(self.tr('ComboView'))
   
        # 2) creates widgets 
        self.EditStrategy = QtGui.QTextEdit()
        self.buttonSave = QtGui.QPushButton(self.tr('Save'))
        self.buttonRun = QtGui.QPushButton(self.tr('Run'))
        # 3)arrange widgets
        layoutTop.addWidget(self.buttonSave)
        layoutTop.addWidget(self.buttonRun)
   
        layout.addWidget(self.EditStrategy)
        self.connect(self.buttonRun,QtCore.SIGNAL("clicked()"),self.slotRun)
    #----------------------------------------------------------------------
    def setText(self,text):
        """"""
        self.EditStrategy.setText(text)
    #----------------------------------------------------------------------
    def slotRun(self):
        """"""
        self.strategyFig = plt.figure()
        self.exec_text(self.EditStrategy.toPlainText())    
    #----------------------------------------------------------------------
    def slotSaveAndRun(self):
        """        
        execute the file
        """
        self.strategyFig = plt.figure()
        strategyFile = os.getcwd()+'/test.py'
        self.exec_filePath(strategyFile)  
    #----------------------------------------------------------------------
    def exec_text(self,text):
        """"""
        global_namespace = {"__name__": "__main__","__fig__":self.strategyFig}
        exec(text, global_namespace)      
    #----------------------------------------------------------------------      
    def exec_filePath(self,filepath):
        global_namespace = {"__file__": filepath,"__name__": "__main__","__fig__":self.strategyFig}
        with open(filepath, 'rb') as file:
            exec(compile(file.read(), filepath, 'exec'), global_namespace)        
      