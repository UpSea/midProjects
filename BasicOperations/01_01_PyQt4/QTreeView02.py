import sys

from PyQt4 import QtCore, QtGui

if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)

    model = TreeModel(需要处理的数据)

    view = QtGui.QTreeView()

    view.setModel(model)

    view.setWindowTitle("Simple Tree Model")

    view.show()

sys.exit(app.exec_())