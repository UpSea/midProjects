import sys   
from PyQt4 import QtCore, QtGui

class MyTreeItem(QtGui.QTreeWidgetItem):  
    def __init__(self, s, parent = None):  
        super(MyTreeItem, self).__init__(parent, [s])  
class MyTree(QtGui.QTreeWidget):  
    def __init__(self, parent = None):  
        super(MyTree, self).__init__(parent)  
        self.setMinimumWidth(200)  
        self.setMinimumHeight(200)  
        for s in ['foo', 'bar']:  
            MyTreeItem(s, self)  
        self.connect(self, QtCore.SIGNAL('itemClicked(QTreeWidgetItem*, int)'), self.onClick)  
    def onClick(self, item, column):  
        print (item.text(0))  
class MainWindow(QtGui.QMainWindow):  
    def __init__(self, parent = None):  
        super(MainWindow, self).__init__(parent)  
        self.tree = MyTree(self)  
def main():  
    app = QtGui.QApplication(sys.argv)  
    win = MainWindow()  
    win.show()  
    app.exec_()  
if __name__ == '__main__':  
    main()  