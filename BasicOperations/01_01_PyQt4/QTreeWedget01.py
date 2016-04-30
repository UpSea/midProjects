# !/usr/bin/python
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
class TreeWidget(QMainWindow):
    def __init__(self,parent=None):
        QWidget.__init__(self,parent)
        self.setWindowTitle('TreeWidget')
        self.tree = QTreeWidget()
        self.tree.setColumnCount(3)
        self.tree.setHeaderLabels(['Items','Name','Detail'])
        
        # tree root
        root= QTreeWidgetItem(self.tree)
        root.setText(0,'StrategyTemplates')
        # Template01 of tree root
        Template01 = QTreeWidgetItem(root)
        Template01.setText(0,'Template01')
        Template01.setText(1,'MV')
        # Template02 of tree root
        Template02 = QTreeWidgetItem(root)
        Template02.setText(0,'Template02')
        Template02.setText(1,'PairTrade')
        # Template03 of tree root
        Template03 = QTreeWidgetItem(root)
        Template03.setText(0,'Template03')
        Template03.setText(1,'OLMR')
        strategy01 = QTreeWidgetItem(Template03)
        strategy01.setText(0,'strategy01')
        strategy01.setText(1,'jjj')
        # add root to treeview
        self.tree.addTopLevelItem(root)
        
        # set treeview as centralwidget of window
        self.setCentralWidget(self.tree)             
app = QApplication(sys.argv)
tp = TreeWidget()
tp.show()
app.exec_()