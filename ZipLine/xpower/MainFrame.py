# -*- coding: utf-8 -*-
from PyQt4 import QtGui,QtCore
import sys
import os
import datetime

import matplotlib.pyplot as plt
import os,sys        
xpower = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,os.pardir,'histdataUI'))
sys.path.append(xpower)

from DataCenterUI_1 import MainWindow
from Views.EditorView import EditorView

QtCore.QTextCodec.setCodecForTr(QtCore.QTextCodec.codecForName("utf8"))           
class DeleteFileDialog(QtGui.QFileDialog):
    #----------------------------------------------------------------------
    def __init__(self):
        """"""
        super(DeleteFileDialog,self).__init__()
        self.resize(600,400)                         
    def keyPressEvent(self, event):  
        keyEvent = QKeyEvent(event)  
        if (event.key() == QtCore.Qt.Key_Delete):  
            print('delete file')
class EmittingStream(QtCore.QObject):
    slotFunction = QtCore.pyqtSignal(str)
    i=0
    def write(self, text):
        if(text == '\n'):
            self.slotFunction.emit(str(text))
        else:
            self.slotFunction.emit(str(self.i) + '-----:' + str(text))
            self.i= self.i+1
class MainFrame(QtGui.QMainWindow):
    def __init__(self,parent=None):
        super(MainFrame,self).__init__(parent)
        self.Globals=[]
        sys.stdout = EmittingStream(slotFunction=self.slotOutputProcessor)
        sys.stder = EmittingStream(slotFunction=self.slotOutputProcessor)        

        self.setWindowTitle(self.tr("XPower"))
        # mid 0)dockable area
        self.createDockablePaneStrategyTreeView()
        self.createDockableInfo()             
        # mid 1)client area
        self.workSpace=QtGui.QWorkspace()
        self.setCentralWidget(self.workSpace)        
        self.creatEditorView()
        # mid 2)init menu,tool,status.
        self.initActions()
        self.initMenuBar()
        self.initToolBar()
        self.initStatusBar()
        
        self.signalMaps()  
    def __del__(self):
        # Restore sys.stdout
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__          
    def slotOutputProcessor(self, text):
        """Append text to the QTextEdit."""
        # Maybe QTextEdit.append() works as well, but this is how I do it:
        cursor = self.editInfo.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.editInfo.setTextCursor(cursor)
        self.editInfo.ensureCursorVisible()
    def modification_changed(self, state=None, index=None, editor_id=None):
        """
        Current editor's modification state has changed
        --> change tab title depending on new modification state
        --> enable/disable save/save all actions
        """
        if editor_id is not None:
            #for index, _finfo in enumerate(self.data):
                #if id(_finfo.editor) == editor_id:
                    #break
                
            for editor in self.workSpace.windowList():
                if(id(editor)==editor_id):
                    editor.setWindowTitle('dffdasdfa')
                    break
        # This must be done before refreshing save/save all actions:
        # (otherwise Save/Save all actions will always be enabled)
        self.emit(QtCore.SIGNAL('opened_files_list_changed()'))
        # --
        #if index is None:
            #index = self.get_stack_index()
        #if index == -1:
            #return
        #finfo = self.data[index]
        if state is None:
            state = finfo.editor.document().isModified()
        #self.set_stack_title(index, state)
        # Toggle save/save all actions state
        #self.save_action.setEnabled(state)
        self.actionFileSave.setEnabled(state)
        #self.emit(SIGNAL('refresh_save_all_action()'))
        # Refreshing eol mode
        #eol_chars = finfo.editor.get_line_separator()
        #os_name = sourcecode.get_os_name_from_eol_chars(eol_chars)
        #self.emit(SIGNAL('refresh_eol_chars(QString)'), os_name)
     
    #----------------------------------------------------------------------
    def slotFileNew(self):
        """"""
        editorView = EditorView(self)
        #from spyderlib.widgets.sourcecode.codeeditor import CodeEditor
        #editorView = CodeEditor(self)
        self.workSpace.addWindow(editorView) 
        editorView.show()
        
        self.connect(editorView, QtCore.SIGNAL('modificationChanged(bool)'),
                     lambda state: self.modification_changed(state,editor_id=id(editorView)))        
    #----------------------------------------------------------------------
    def slotFileSave(self):
        """
        已存在此文件，直接保存
        不存在时，取得保存文件名，之后保存
        """
        text = self.workSpace.activeWindow().toPlainText()
        fileName = self.workSpace.activeWindow().getFileName()
        fileNameToSave = ''
        if(fileName != None and os.path.isfile(fileName)):  # mid exists
            strategyFolder = os.path.dirname(fileName)
            templateFileNames=os.listdir(strategyFolder)
            bExists = False
            for templateFileName in templateFileNames: 
                if(templateFileName == fileName):
                    fileNameToSave = fileName
                    bExists = True
                    break
            if(not bExists):
                fileNameToSave = fileName
        else:                                               #mid not exists
            strategyFolder = os.getcwd()+'/Strategies'
            fileNameToSave = QtGui.QFileDialog.getSaveFileName(self, "save as", strategyFolder,"All Files (*);;Text Files (*.py)")  
        
        
        if(len(fileNameToSave)>0):
            file=open(fileNameToSave,'w')    # r只读，w可写，a追加
            #filename=open(file,'w')
            #filename.write('asdfasdfasdfadfasdf')
            #filename.close()            
            file.write(text)
            file.close()
        self.refreshStrategyTreeContent()
    #----------------------------------------------------------------------
    def slotFileClose(self):
        """"""
        self.workSpace.closeActiveWindow()
    #----------------------------------------------------------------------
    def slotFileCloseAll(self):
        """"""
        self.workSpace.closeAllWindows()
    #----------------------------------------------------------------------
    def slotOpenFolder(self):
        """"""
        #self.fileNameToSave = DeleteFileDialog()
        ##self.setGeometry(300, 300, 250, 150)
        #self.fileNameToSave.setWindowTitle('Strategy Files')
        #strategyFolder = os.getcwd()+'/Strategies'
        #self.fileNameToSave.setDirectory(strategyFolder)
        #self.fileNameToSave.setFilter("All Files (*);;Text Files (*.py)")

        urls = []
        strategyFolder = os.getcwd()+'/Strategies'
        urls.append(QtCore.QUrl.fromLocalFile(strategyFolder))
        urls.append(QtCore.QUrl.fromLocalFile(os.getcwd()))

        dialog = DeleteFileDialog()
        dialog.setWindowTitle('Strategy Files')
        dialog.setDirectory(strategyFolder)
        dialog.setFilter("All Files (*);;Text Files (*.py)")        
        dialog.setSidebarUrls(urls);
        dialog.setFileMode(QtGui.QFileDialog.AnyFile);
        if(dialog.exec()):
            pass
        self.refreshStrategyTreeContent()
    #----------------------------------------------------------------------
    def slotRun(self):
        """需要由俩文件组合之后运行，所以，单文件运行功能取消
        if(self.workSpace.activeWindow() != None):
            self.workSpace.activeWindow().slotRun()        
        """
        # 1)确定模板窗口和参数窗口
        #打开editor时，应设置父子关系
        #template没有parent，params有parent
        #运行时，判断是否有parent，无则提示不能运行
        #有则获得其parent的text并组合运行之        
        # 2)获得模板文本和参数文本
        paramsEditor = self.workSpace.activeWindow()
        templateEditor = paramsEditor.getParentEditor()
        if(templateEditor == None):
            message = QtGui.QMessageBox.information(self,"Information",self.tr('Please choose a params file to run.'))      
            message.exec_()
        else:
            '''mid
            两个文件。
            一个参数文件，一个是策略文件
            exec()执行的第一个参数是python程序，第二个参数是一个变量，可提供参数给被执行的文件

            1.执行参数生成程序，传入一个全局变量，参数生成程序会写入参数
            2.执行策略程序，此程序会读入参数程序生成的参数，并做计算      
            在templateText执行过程中需要__file__参数
            作为文本执行的程序是没有此参数的（IDE下执行打开的文件会有次参数）
            所以主动生成次占位参数

            在IDE中执行时，使用此参数的语句是有实际功能的
            使用exec()方式执行时次参数无用，但为了在两个环境分别执行时不修改代码，特如此修改
            IDE中如下语句用到__file__
            import os,sys        
            xpower = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,os.pardir,os.pardir,'histdata'))
            sys.path.append(xpower)
            '''
            templateText = templateEditor.toPlainText()
            paramsText = paramsEditor.toPlainText()
            # 3)自参数文本获取参数
            global_namespace = {'__file__':__file__,'params':{},'Globals':self.Globals}
            exec(paramsText, global_namespace)
            #print('params set:',global_namespace['params'])        
            ## 4)传参数入模板，形成策略并运行       
            exec(templateText,global_namespace)
    #----------------------------------------------------------------------
    def creatEditorView(self):
        """"""  
        # 0) mid should open the default file
        editorView = EditorView(None)
        self.workSpace.addWindow(editorView) 
        editorView.showMaximized()    
    #----------------------------------------------------------------------
    def initStatusBar(self):
        """"""
        # status bar
        self.statusBar()
    #----------------------------------------------------------------------
    def initActions(self):
        """mid 
        1) 创建动作
        2) 设置动作的快捷键
        3) 设置动作的图标(将在toolbar显示)
        4) 关联动作和某个函数
        """
        # 0.0) mid program control
        exit = QtGui.QAction(QtGui.QIcon('icons/actions/exit.png'), 'Exit', self)
        exit.setShortcut('Ctrl+Q')
        exit.setStatusTip('Exit application')
        self.connect(exit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))    
        self.actionExit = exit
        # 0.1) strategy control
        run = QtGui.QAction(QtGui.QIcon('icons/editor/run.png'), 'Run', self)
        run.setShortcut('F5')
        run.setStatusTip('Exit application')
        self.connect(run, QtCore.SIGNAL('triggered()'), self.slotRun)    
        self.actionRun = run        
        
        stop = QtGui.QAction(QtGui.QIcon('icons/actions/stop.png'), 'Exit', self)
        stop.setShortcut('Ctrl+Q')
        stop.setStatusTip('Exit application')
        self.connect(stop, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))    
        self.actionStop = stop
        # 1) mid dataManager
        dataManager = QtGui.QAction(QtGui.QIcon('icons/genprefs.png'), 'dataManager', self)
        dataManager.setShortcut('Ctrl+Q')
        dataManager.setStatusTip('dataManager') 
        self.connect(dataManager, QtCore.SIGNAL('triggered()'), self.slotDownFromTushare)  
        self.actionDataManager = dataManager            
        # 2)mid layout arrangement
        arrange=QtGui.QAction(self.tr("Arrange"),self)
        self.connect(arrange,QtCore.SIGNAL("triggered()"),self.workSpace,QtCore.SLOT("arrangeIcons()"))
        self.actionArrange = arrange
        
        tile=QtGui.QAction(self.tr("Tile"),self)
        self.connect(tile,QtCore.SIGNAL("triggered()"),self.workSpace,QtCore.SLOT("tile()"))        
        self.actionTile = tile
        
        cascade=QtGui.QAction(self.tr("Cascade"),self)
        self.connect(cascade,QtCore.SIGNAL("triggered()"),self.workSpace,QtCore.SLOT("cascade()"))        
        self.actionCascade = cascade
        # 3)mid workSpace navigation
        scrollAct=QtGui.QAction(self.tr("Scroll"),self)
        self.connect(scrollAct,QtCore.SIGNAL("triggered()"),self.slotScroll)        
        self.actionScrollWindow = scrollAct
        
        nextAct=QtGui.QAction(self.tr("Next"),self)
        self.connect(nextAct,QtCore.SIGNAL("triggered()"),self.workSpace,QtCore.SLOT("activateNextWindow()")) 
        self.actionNextWindow = nextAct
        
        previousAct=QtGui.QAction(self.tr("Previous"),self)
        self.connect(previousAct,QtCore.SIGNAL("triggered()"),self.workSpace,QtCore.SLOT("activatePreviousWindow()"))        
        self.actionPreviousWindow = previousAct
        # 4)mid file management
        fileSave = QtGui.QAction(QtGui.QIcon('icons/file/filesave.png'), 'fileSave', self)
        fileSave.setShortcut('Ctrl+s')
        fileSave.setStatusTip('fileSave') 
        self.connect(fileSave, QtCore.SIGNAL('triggered()'), self.slotFileSave)  
        self.actionFileSave = fileSave      
        
        saveAs = QtGui.QAction(QtGui.QIcon('icons/file/filesaveas.png'), 'saveas', self)
        #save.setShortcut('Ctrl+s')
        saveAs.setStatusTip('save as') 
        self.connect(saveAs, QtCore.SIGNAL('triggered()'), self.slotDownFromTushare)  
        self.actionFileSaveAs = saveAs              
        
        saveAll = QtGui.QAction(QtGui.QIcon('icons/file/save_all.png'), 'saveall', self)
        #save.setShortcut('Ctrl+s')
        saveAll.setStatusTip('save as') 
        self.connect(saveAll, QtCore.SIGNAL('triggered()'), self.slotDownFromTushare)  
        self.actionFileSaveAll = saveAll 
        
        filenew = QtGui.QAction(QtGui.QIcon('icons/file/filenew.png'), 'file new', self)
        #save.setShortcut('Ctrl+s')
        filenew.setStatusTip('file new') 
        self.connect(filenew, QtCore.SIGNAL('triggered()'), self.slotFileNew)  
        self.actionFileNew = filenew    
        
        fileclose = QtGui.QAction(QtGui.QIcon('icons/file/fileclose.png'), 'file close', self)
        #save.setShortcut('Ctrl+s')
        fileclose.setStatusTip('file close') 
        self.connect(fileclose, QtCore.SIGNAL('triggered()'), self.slotFileClose)  
        self.actionFileClose = fileclose         
    
        filecloseall = QtGui.QAction(QtGui.QIcon('icons/file/filecloseall.png'), 'close all', self)
        #save.setShortcut('Ctrl+s')
        filecloseall.setStatusTip('file close all') 
        self.connect(filecloseall, QtCore.SIGNAL('triggered()'), self.slotFileCloseAll)  
        self.actionFileCloseAll = filecloseall 
        
        
        folderOpen = QtGui.QAction(QtGui.QIcon('icons/projects/folder.png'), 'close all', self)
        #save.setShortcut('Ctrl+s')
        folderOpen.setStatusTip('file close all') 
        self.connect(folderOpen, QtCore.SIGNAL('triggered()'), self.slotOpenFolder)  
        self.actionFolderOpen = folderOpen         
    #----------------------------------------------------------------------
    def initToolBar(self):
        """"""
        # 1)mid save file
        fileToolBar = self.addToolBar('filetool')
        fileToolBar.addAction(self.actionFileNew)   
        fileToolBar.addAction(self.actionFileSave)
        fileToolBar.addAction(self.actionFileSaveAs)
        fileToolBar.addAction(self.actionFileSaveAll)
        fileToolBar.addAction(self.actionFileClose)          
        fileToolBar.addAction(self.actionFileCloseAll)    
        fileToolBar.addAction(self.actionFolderOpen)
        # 2)mid strategy control
        strategyToolBar = self.addToolBar('strategyControl')
        strategyToolBar.addAction(self.actionRun)
        strategyToolBar.addAction(self.actionStop)
        # 3) mid add dataManager icon
        dataManagerToolBar = self.addToolBar('dataManager')
        dataManagerToolBar.addAction(self.actionDataManager)    
        # 4) mid add window manager
        windowsManagerToolBar = self.addToolBar('windows manager')
        windowsManagerToolBar.addAction(self.actionArrange)
        windowsManagerToolBar.addAction(self.actionCascade)
        windowsManagerToolBar.addAction(self.actionTile)
        windowsManagerToolBar.addAction(self.actionPreviousWindow)
        windowsManagerToolBar.addAction(self.actionNextWindow)
        # 4) mid program control
        toolbar = self.addToolBar('sysCtrl')
        toolbar.addAction(self.actionExit)      
    #----------------------------------------------------------------------
    def initMenuBar(self):
        """mid
        1.创建子菜单
        2.将已创建的动作加入子菜单
        """
        # 1.1
        menubar = self.menuBar()
        # 1) file
        file = menubar.addMenu('&File')
        file.addAction(self.actionExit)
        file.addAction(self.actionFileNew)
        file.addAction(self.actionFileSave)
        file.addAction(self.actionFileSaveAs)
        file.addAction(self.actionFileClose)
        file.addAction(self.actionFileCloseAll)
        # 2) dataManager
        dataManager = menubar.addMenu('&DataManager')        
        dataManager.addAction(self.actionDataManager)
        # 3) layout
        layoutMenu=menubar.addMenu(self.tr("Layout"))
        layoutMenu.addAction(self.actionArrange)
        layoutMenu.addAction(self.actionTile)
        layoutMenu.addAction(self.actionCascade) 
        # 4) other
        otherMenu=menubar.addMenu(self.tr("Navigate"))
        otherMenu.addAction(self.actionScrollWindow)
        otherMenu.addSeparator()
        otherMenu.addAction(self.actionNextWindow)
        otherMenu.addAction(self.actionPreviousWindow)  
    #----------------------------------------------------------------------
    def refreshStrategyTreeContent(self):
        """"""
        self.treeStrategyView.clear()
        info=os.getcwd()
        strategyFolder = info+'/Strategies'
        templateFileNames=os.listdir(strategyFolder)
        for templateFileName in templateFileNames:  
            if templateFileName[-3:] == '.py' and templateFileName[0:2] != '__':
                # 0) add strategy template to tree
                templateItem= QtGui.QTreeWidgetItem(self.treeStrategyView)
                templateItem.setExpanded(True)
                templateItem.setFirstColumnSpanned(True)            
                templateFullFileName = strategyFolder+'/'+templateFileName
                templateItem.setData(0, QtCore.Qt.UserRole,templateFullFileName) #mid 这个序号不知用来做什么，可以这样存取就这样用了
                templateItem.setData(1,QtCore.Qt.UserRole,'')
                templateItem.setText(0,templateFileName[0:-3])       
                templateItem.setIcon(0,QtGui.QIcon('icons/projects/folder.png'))
                dataAdded = templateItem.data(0,QtCore.Qt.UserRole)
                self.treeStrategyView.addTopLevelItem(templateItem) 
                
                # 1) add sub parameters to the template
                paramsFolder = strategyFolder + '/' + templateFileName[0:-3]
                if(not os.path.isdir(paramsFolder)):
                    os.makedirs(paramsFolder)
                paramsFileNames = os.listdir(paramsFolder)
                for paramsFileName in paramsFileNames:
                    paramsItem = QtGui.QTreeWidgetItem(templateItem)
                    paramsFullFileName = paramsFolder+'/'+paramsFileName
                    paramsItem.setData(0, QtCore.Qt.UserRole,paramsFullFileName) #mid 这个序号不知用来做什么，可以这样存取就这样用了                    
                    paramsItem.setData(1,QtCore.Qt.UserRole,templateFullFileName)
                    paramsItem.setText(0,paramsFileName[0:-3])
                    
                    time_of_last_access = os.path.getatime(paramsFullFileName)
                    time_of_last_modification = os.path.getmtime(paramsFullFileName)
                    size = os.path.getsize(paramsFullFileName)                    
                    
                    paramsItem.setText(1,datetime.datetime.fromtimestamp(time_of_last_access).strftime("%Y-%m-%d %X"))      
                    paramsItem.setText(2,datetime.datetime.fromtimestamp(time_of_last_modification).strftime("%Y-%m-%d %X"))   
                    
                    paramsItem.setIcon(0,QtGui.QIcon('icons/console/python.png'))
                    paramsItem.setIcon(1,QtGui.QIcon('icons/console/run_small.png'))          
    #----------------------------------------------------------------------
    def createDockablePaneStrategyTreeView(self):
        dock1=QtGui.QDockWidget(self.tr("StrategiesTree"),self)
        dock1.setFeatures(QtGui.QDockWidget.DockWidgetMovable)
        dock1.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)

        self.treeStrategyView = QtGui.QTreeWidget()
        self.treeStrategyView.setColumnCount(3)
        self.treeStrategyView.setHeaderLabels(['Items','AccessTime','ModificationTime'])
        self.treeStrategyView.setColumnWidth(0,200)
        self.treeStrategyView.setColumnWidth(1,200)
        dock1.setWidget(self.treeStrategyView)
        dock1.setMaximumWidth(800)
        dock1.setMinimumWidth(300)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea,dock1)     
        
        self.refreshStrategyTreeContent()
    #----------------------------------------------------------------------
    def createDockableInfo(self):
        dock3=QtGui.QDockWidget(self.tr("Information View"),self)
        dock3.setFeatures(QtGui.QDockWidget.AllDockWidgetFeatures)
        self.editInfo=QtGui.QTextEdit(self.tr("Info:"))
        dock3.setWidget(self.editInfo)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea,dock3)  
    # 重新实现事件处理程序，但按下'Esc'键时，退出程序。
    def keyPressEvent(self, e):

        if e.key() == QtCore.Qt.Key_Escape:
            self.close()    
            
    # 通过调用sender()方法判断信号源。
    # 两个不同的信号源同时出发此过程，可判断信号发送者
    def buttonClicked(self):
        sender = self.sender()
        self.statusBar().showMessage(sender.text() + ' was pressed')    
    #----------------------------------------------------------------------
    def slotScroll(self):
        self.workSpace.setScrollBarsEnabled(not self.workSpace.scrollBarsEnabled())     
    #----------------------------------------------------------------------
    def signalMaps(self):
        """"""
        # signal and slot
        #self.connect(self.listWidget,QtCore.SIGNAL("currentRowChanged(int)"),self.stack,QtCore.SLOT("setCurrentIndex(int)"))
        self.connect(self.treeStrategyView,QtCore.SIGNAL('itemClicked(QTreeWidgetItem*, int)'), self.slotTreeClicked)
    def slotOpenedFileChanged(self,editor,strategyFile):
        customMsgBox=QtGui.QMessageBox(self)
        customMsgBox.setWindowTitle("Warning")
        saveButton=customMsgBox.addButton(self.tr("save changes"),QtGui.QMessageBox.ActionRole)
        reloadButton=customMsgBox.addButton(self.tr("reload"),QtGui.QMessageBox.ActionRole)
        cancelButton=customMsgBox.addButton("cancel",QtGui.QMessageBox.ActionRole)
        
        customMsgBox.setText(self.tr("file changed since open!"))
        customMsgBox.exec_()
        
        button=customMsgBox.clickedButton()
        if button==saveButton:
            with open(strategyFile, 'w') as file: 
                file.write(editor.toPlainText())
                editor.document().setModified(False)
            file.close()
        elif button==reloadButton:
            # open the clicked file in a existing editor
            with open(strategyFile, 'r') as file:
                editor.set_text(file.read())        
            file.close()
        elif button==cancelButton:
            pass   
    #----------------------------------------------------------------------
    def fnOpenFileInEditor(self,fullFileName = None,parentEditor = None):
        """
        if opend:
            return it
        else
            open file
            set parent
            return editor
        """
        if(fullFileName is not None):
            # if file opened and not changed,turn to its editor and set current active view.
            for editor in self.workSpace.windowList():
                fileNameOfCurrentEditor = editor.getFileName()
                if(fileNameOfCurrentEditor == fullFileName):
                    if(editor.document().isModified()):
                        self.slotOpenedFileChanged(editor,fullFileName)
                    else:
                        self.workSpace.setActiveWindow(editor)
                    return editor
            # open the clicked file in new editor
            editorView = EditorView(parent = parentEditor,fileName=fullFileName)
            
            if(parentEditor==None): # set editor title as file base name
                editorView.setWindowTitle('template-'+os.path.splitext(os.path.split(fullFileName)[1])[0])
            else:
                editorView.setWindowTitle('params-'+os.path.splitext(os.path.split(fullFileName)[1])[0])         
            self.workSpace.addWindow(editorView) 
            with open(fullFileName, 'r') as file:
                editorView.set_text(file.read())
            file.close()
            editorView.show()
            return editorView
    #----------------------------------------------------------------------
    def slotTreeClicked(self, item, column):
        """
        根据某个item有无父文件确定其是template还是params
        有无父文件，在构造tree时设置
        """
        #不打开template而直接打开params时会有异常，其他正常
        parent=item.parent()   
        fullFileName = item.data(0,QtCore.Qt.UserRole)
        fullParentFillName = item.data(1,QtCore.Qt.UserRole)
        if(len(fullParentFillName)>0):
            parentEditor = self.fnOpenFileInEditor(fullFileName=fullParentFillName,parentEditor=None)
            self.fnOpenFileInEditor(fullFileName = fullFileName, parentEditor = parentEditor)
        else:
            self.fnOpenFileInEditor(fullFileName = fullFileName, parentEditor =None )
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
            index_top= self.treeStrategyView.indexOfTopLevelItem(item)
        else :               
            index_top =  self.treeStrategyView.indexOfTopLevelItem(parent) 
            index_row=parent.indexOfChild(item)##获得节点在父节点中的行号(从0开始)
    
        print(index_top,  index_row) 
        print (item.text(0)) 
    def slotDownFromTushare(self):
        """
        此处将dialog设置为实例变量是有原因的
        若为局部变量，调用后会自动清除，导致闪退
        """
        self.dialog=MainWindow()
        self.dialog.show()       