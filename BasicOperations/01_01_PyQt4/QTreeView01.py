import sys

from PyQt4 import QtCore, QtGui

if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)

    model = QtGui.QDirModel() #系统给我们提供的

    tree = QtGui.QTreeView()

    tree.setModel(model)

    tree.setWindowTitle(tree.tr("Dir View"))

    tree.resize(640, 480)

    tree.show()

    sys.exit(app.exec_())