# -*- coding: utf-8 -*-
from PyQt4 import QtGui,QtCore
import os
import matplotlib.pyplot as plt
from Views.HistoryCandleView import HistoryCandleView
from spyderlib.widgets.sourcecode.codeeditor import CodeEditor
class EditorView(CodeEditor):
    def __init__(self,parent=None,fileName=None):
        super(EditorView,self).__init__(parent)
        self.parentEditor = parent
        self.fileName = fileName
        self.setWindowTitle(self.tr("CoderEditor"))   
        # 3) setting Editor style 
        self.setup_editor(language = "python",font = QtGui.QFont("Courier New"))
        # 4) setting Editor shortcut(moved to mainframe)
        #run_sc = QtGui.QShortcut(QtGui.QKeySequence("F5"), self, self.slotRun)        
        #self.connect(self.buttonRun,QtCore.SIGNAL("clicked()"),self.slotRun)
    #----------------------------------------------------------------------
    def setParentEditor(self,editor):
        """"""
        self.parentEditor = editor
    #----------------------------------------------------------------------
    def getParentEditor(self):
        """"""
        return self.parentEditor
    #----------------------------------------------------------------------
    def getFileName(self):
        """"""
        return self.fileName
    #----------------------------------------------------------------------
    def slotRun(self):
        """"""
        #self.strategyFig = plt.figure()
        self.exec_text(self.toPlainText())    
    #----------------------------------------------------------------------
    def slotSaveAndRun(self):
        """        
        execute the file
        """
        strategyFile = os.getcwd()+'/test.py'
        self.exec_filePath(strategyFile)  
    #----------------------------------------------------------------------
    def exec_text(self,text):
        """"""
        global_namespace = {"__name__": __name__,'params':{}}
        exec(text, global_namespace)
        print(global_namespace['params'])
    #----------------------------------------------------------------------      
    def exec_filePath(self,filepath):
        global_namespace = {"__file__": filepath,"__name__": __name__}
        with open(filepath, 'rb') as file:
            exec(compile(file.read(), filepath, 'exec'), global_namespace)