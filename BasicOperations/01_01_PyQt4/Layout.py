from PyQt4 import QtGui,QtCore
import sys

#----------------------------------------------------------------------
def popOut():
    """"""
    # 1) creates layout
    childFrame = QtGui.QDialog()
    layout = QtGui.QVBoxLayout()
    layoutTop = QtGui.QHBoxLayout()
    layout.addLayout(layoutTop)
    childFrame.setLayout(layout)        
    childFrame.setWindowTitle(('ComboView'))
    
    # 2) creates widgets 
    EditStrategy = QtGui.QTextEdit()
    buttonSave = QtGui.QPushButton(('Save'))
    buttonRun = QtGui.QPushButton(('Run'))
    # 3)arrange widgets
    layoutTop.addWidget(buttonSave)
    layoutTop.addWidget(buttonRun)
    
    layout.addWidget(EditStrategy)
    
    childFrame.show()

qApp=QtGui.QApplication(sys.argv)
popOut()
sys.exit(qApp.exec_())