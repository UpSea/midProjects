from PyQt4.QtGui import *
from PyQt4.QtCore import *


class MyTabView(QTableView):
    def __init__(self, parent=None):
        super(MyTabView, self).__init__(parent)
        self.model = QStandardItemModel(4, 2)
        self.setModel(self.model)

    def mouseDoubleClickEvent(self, event):
        QTableView.mouseDoubleClickEvent(self, event)
        pos = event.pos()
        item = self.indexAt(pos)
        if item:
            print ("item clicked at ", item.row(), " ", item.column())


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    w = QWidget()
    w.resize(1024, 768)
    v = MyTabView(w)
    w.show()
    app.exec_()