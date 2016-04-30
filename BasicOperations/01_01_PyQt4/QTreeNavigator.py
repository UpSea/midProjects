from PyQt4 import QtCore, QtGui

class  Bar_Navigation(QtGui.QWidget):
    def  __init__(self):
        super(Bar_Navigation, self).__init__()
        self.setMinimumHeight(600);
        self.setMinimumWidth(800);

        ##layout_main.setMargin(5)
        ##layout_main.setSpace(5)
        self.creat_main_layout()
        self.creat_bar_navigation()
        self.creat_left_box()

    def get_bar_list(self):

        bar_list_item = []
        bar_list_1 = ["订货管理",
                      ["客户订货", "库存订货", "供货商订货"]
                      ]
        bar_list_2 = ["入库管理",
                      ["采购入库", "订货入库", "其它入库"]
                      ]
        bar_list_item.append(bar_list_1)
        bar_list_item.append(bar_list_2)
        return  bar_list_item

    def creat_main_layout(self): 
        self.layout_main = QtGui.QHBoxLayout()
        self.setLayout( self.layout_main)

    def creat_bar_list(self, data):

        for item in data:
            item_1 =  QtGui.QTreeWidgetItem( self.tree_Navigation);           
            ##item_1.setText(0,item[0])
            ## 设置节点的打开/关闭状态下的不同的图片
            icon = QtGui.QIcon()
            ##节点打开状态
            icon.addPixmap(QtGui.QPixmap("./logo2.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
            ##节点关闭状态　　
            icon.addPixmap(QtGui.QPixmap("./logo1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            item_1.setIcon(0, icon)

            for item_item in item[1]:
                item_1_1 =  QtGui.QTreeWidgetItem( item_1);           
                item_1_1.setText(0,item_item)  
            self.tree_Navigation.addTopLevelItem(item_1);
    def creat_bar_navigation(self):
        self.tree_Navigation = QtGui.QTreeWidget()    
        self.tree_Navigation.setHeaderLabel("左侧导航栏");           
        self.tree_Navigation.setColumnCount(1)
        self.tree_Navigation.setMaximumWidth(150);

        icon_size = QtCore.QSize(100, 30)
        self.tree_Navigation.setIconSize(icon_size)

        ##如果treewidget就一列，该列的宽度默认等于treewidget的宽度,两列以上的话才起作用.
        ##self.tree_Navigation.setColumnWidth(0,100);
        data = self.get_bar_list()
        self.creat_bar_list(data)
        self.layout_main.addWidget(self.tree_Navigation)
        ## QModelIndex
        ##self.tree_Navigation.doubleClicked.connect(self.showModelSelected)
        ## QTreeWidgetItem
        self.tree_Navigation.itemDoubleClicked.connect(self.showSelected)

    ## QModelIndex
    def showModelSelected(self, modelIndex):
        print( modelIndex.row(), modelIndex.column())

    ## itemObj:QTreeWidgetItem
    def showSelected(self, item, column):
        ##获得父节点
        parent=item.parent()   

        ## 注:本例的深度只有2,因此只有index_top,index_row两个变量表示路径
        ##根节点上的索引
        ## 合理值:非负整数
        index_top = 0
        ## 子节点上的索引
        ##如果为-1则标示是根节点上的项;如果不是-1则标示在子节点上
        ## 合理值:非负整数
        index_row = -1

        ## 如果是要判断是否为None，则：
        if parent is None:
            index_top= self.tree_Navigation.indexOfTopLevelItem(item)
        else :               
            index_top =  self.tree_Navigation.indexOfTopLevelItem(parent) 
            index_row=parent.indexOfChild(item)##获得节点在父节点中的行号(从0开始)

        print(index_top,  index_row)

    def creat_left_box(self):
        self.box_left = QtGui.QGroupBox('left party')  
        self.layout_main.addWidget(self.box_left)

if __name__ == "__main__":

    import sys

    app = QtGui.QApplication(sys.argv)
    window = Bar_Navigation()
    window.show()

    sys.exit(app.exec_())