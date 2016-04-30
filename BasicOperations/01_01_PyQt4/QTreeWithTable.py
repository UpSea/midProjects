from PyQt4 import QtGui
import sys
class mainWindow(QtGui.QDialog):
    """"""
    def __init__(self):
        """Constructor"""
        super(mainWindow,self).__init__()
        self.treeWidget = QtGui.QTreeWidget()
        self.treeWidget.setColumnCount(3)
        self.treeWidget.setHeaderLabels(['Items','Name','Detail'])        
        
        treeItem01 = QtGui.QTreeWidgetItem()
        treeItem02 = QtGui.QTreeWidgetItem()
        treeItem01.setText(0,'aaa')
        treeItem01.setText(1,'bbb')
        treeItem02.setText(0,'aaa')
        treeItem02.setText(1,'bbb')    
        self.treeWidget.addTopLevelItem(treeItem01)
        self.treeWidget.addTopLevelItem(treeItem02)  
        
        treeSubItem01 = QtGui.QTreeWidgetItem()
        treeSubItem02 = QtGui.QTreeWidgetItem()
        treeItem01.addChild(treeSubItem01)
        treeItem02.addChild(treeSubItem02)
        
        self.treeWidget.setFirstItemColumnSpanned(treeSubItem01,True)
        self.treeWidget.setFirstItemColumnSpanned(treeSubItem02,True)
        
       
        table = self.getTable()
        self.treeWidget.setItemWidget(treeSubItem01,0,table)
        
        table = self.getTable()
        self.treeWidget.setItemWidget(treeSubItem02,0,table)
        
        
        layout = QtGui.QVBoxLayout()
        self.setLayout(layout)     
        layout.addWidget(self.treeWidget)
    #----------------------------------------------------------------------
    def getTable(self):
        """"""
        tableWidget = QtGui.QTableWidget()     
        tableWidget.setColumnCount(5)
        tableWidget.setRowCount(3)
        for row in range(3):     
            tableWidget.setItem(row,0,QtGui.QTableWidgetItem('datetime'))
            tableWidget.setCellWidget(row,1,QtGui.QLabel(self.tr('openPrice')))
            tableWidget.setItem(row,2,QtGui.QTableWidgetItem('highPrice'))
            tableWidget.setItem(row,3,QtGui.QTableWidgetItem('lowPrice'))
            tableWidget.setItem(row,4,QtGui.QTableWidgetItem('closePrice'))          
        
        return tableWidget
        
if __name__ == "__main__":
    qApp=QtGui.QApplication(sys.argv)
    window = mainWindow()
    window.show()
    sys.exit(qApp.exec_())