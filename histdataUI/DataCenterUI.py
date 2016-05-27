# -*- coding: utf-8 -*-
'''mid
此文件为数据管理程序主界面
用于对历史数据进行检查核对

功能：
    1.展示本地数据KLine图形
    2.下载远程数据到本地
窗口布局：
    1.数据展示主窗口
        左侧为本地数据列表
        右侧为KLine
        左下侧为本地数据操作命令按钮
    2.数据下载管理子窗口
        左侧为代码表
        右侧为待下载代码
程序结构：
    为了能够方便的被各种窗体调用嵌入，各个窗体都定义为layout
'''
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from PyQt4 import QtGui,QtCore
from datetime import datetime
import os,sys
import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.dates as mpd
import matplotlib.pyplot as plt

if sys.version > '3':
    PY3 = True
else:
    PY3 = False    
    
xpower = os.path.abspath(os.path.join(os.path.dirname(__file__),'Widgets'))
sys.path.append(xpower)
xpower = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,'histdata','mongodb'))
sys.path.append(xpower)
xpower = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,'histdata'))
sys.path.append(xpower)

import feedsForCandle as feedsForCandle
from data.mongodb.DataSourceMongodb import Mongodb
from Widgets.pgCandleWidgetCross import pgCandleWidgetCross
from Views.HistoryCandleView import HistoryCandleView
from Views.HistoryTableView import HistoryTableView

class DataManagerDialog(QtGui.QDialog):
    def __init__(self,parent=None):
        super(DataManagerDialog,self).__init__(parent)
        import os,sys
        dataRoot = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,os.pardir,'histdata'))        
        sys.path.append(dataRoot)        
        import dataCenter as dataCenter
        #mid data
        self.dataCenter = dataCenter.dataCenter()   
        self.dfLocalSymbols = pd.DataFrame(columns=['code','name','c_name'])
        self.dfSymbolsToDownload = pd.DataFrame(columns=['code','name','c_name'])
        
        self.setWindowTitle(self.tr("DataManager"))
        self.initUI()    
    def onLocalSymbolSelectorActivate(self,text):
        self.updateLocalAvailableSymbolsTable()
    #----------------------------------------------------------------------    
    def onActivate(self, text):
        #mid feedFormat = tushareCsv|tushare|yahooCsv|yahoo|generic
        #self.feed = fd.getFeeds(feedFormat = text,instrument = self.instrument)
        #---------------------------------------------------------------------
        codesType = self.codesTypeComboBox.currentText()
        sourceType = self.sourceTypeComboBox.currentText()
        if(codesType == 'tushare'):
            self.dfLocalSymbols = self.dataCenter.getCodes(codesType,sourceType)
        else:
            QtGui.QMessageBox.information(self,codesType + ' codesTable data.',  'from '+sourceType+'\nis not prepared.')
            return
        #self.dfLocalSy     mbols = ts.get_stock_basics()        
        #QtGui.QMessageBox.information(self,codesType + ' codesTable data.',  'from '+sourceType+' gotten.')    

        self.updateLocalSymbolsTable()  
        self.updateSymbolsToDownloadTable() 
        
    def initTopCodesSourceSelector(self,topLeft01):
        # 01)topLeft01------------------
        topLeft01Top = QtGui.QHBoxLayout(self)        
        # 01.01 mid codes type
        codesTypeLable = QtGui.QLabel(self.tr("codes source type:"))  
        codesTypeComboBox=QtGui.QComboBox()
        self.codesTypeComboBox = codesTypeComboBox
        codesTypeComboBox.insertItem(0,self.tr("tushare"))
        codesTypeComboBox.insertItem(1,self.tr("sina"))        
        codesTypeComboBox.insertItem(2,self.tr("datayes"))        
        codesTypeComboBox.insertItem(3,self.tr("yahoo"))        
        codesTypeComboBox.activated[str].connect(self.onActivate)        
        # 01.02 mid source type
        codesSourceLable = QtGui.QLabel(self.tr("storage type:")) 
        sourceTypeComboBox=QtGui.QComboBox()
        self.sourceTypeComboBox = sourceTypeComboBox
        sourceTypeComboBox.insertItem(0,self.tr("mongodb"))        
        sourceTypeComboBox.insertItem(1,self.tr("remote"))
        sourceTypeComboBox.insertItem(2,self.tr("csv"))
        sourceTypeComboBox.activated[str].connect(self.onActivate)        
        
        # 01.03 mid codes table last refreshed time
        codesRefreshedTimeLable = QtGui.QLabel(self.tr("last refreshed:"))           
    
        codesRefreshedTimeEdit = QtGui.QLineEdit()
        codesRefreshedTimeEdit.setEnabled(False)
        codesRefreshedTimeEdit.setText('2015.16.18 00:00:00')
    
        topLeft01Top.addWidget(codesTypeLable)
        topLeft01Top.addWidget(codesTypeComboBox)
        topLeft01Top.addWidget(codesSourceLable)
        topLeft01Top.addWidget(sourceTypeComboBox)
        topLeft01Top.addWidget(codesRefreshedTimeLable)
        topLeft01Top.addWidget(codesRefreshedTimeEdit)     
        
        topLeft01.addLayout(topLeft01Top)
    #----------------------------------------------------------------------   
    def onVerSectionClicked(self,index):
        print (index)
    def onHorSectionClicked(self,index):
        print (index) 
        #self.tableLocalSymbols.resizeColumnsToContents()#根据内容调整行的宽度
        #self.tableLocalSymbols.resizeRowToContents()#根据内容调整列的宽度度
        #self.tableLocalSymbols.item(row,col).setTextAlignment(Qt.AlignCenter)#设置字体居中        
    def onTableSymbolsToDownloadDoubleClicked(self, rowSelected,column ):
        self.slotDeleteOne()
    def onTableLocalSymbolsDoubleClicked(self , rowSelected,column ):
        self.slotAddOne()   
    def onClicked(self  ):
        print ('******row : ' , self.tableLocalSymbols.currentRow(), ' ***********')
        
        rows = self.tableLocalSymbols.rowCount()

        #for rows_index in range(rows):
            ##print items[item_index].text()
            #print (self.tableLocalSymbols.item(rows_index,0).text())    
    def initCodesTable(self,topLeft01):        
        self.tableLocalSymbols=QtGui.QTableWidget()
        self.tableLocalSymbols.horizontalHeader().setStretchLastSection(True)                   #mid 可以设置最后一览大小自适应
        self.tableLocalSymbols.verticalHeader().sectionClicked.connect(self.onVerSectionClicked)#表头单击信号
        self.tableLocalSymbols.horizontalHeader().sectionClicked.connect(self.onHorSectionClicked)#表头单击信号     
        
        #self.connect(self.tableLocalSymbols, QtCore.SIGNAL("itemClicked(QTableWidgetItem* item)"), self.testRow2)
        # QtCore.QObject.connect(self.table, QtCore.SIGNAL("cellActivated ( int row, int column )"), self.testRow)
        #self.connect(self.tableLocalSymbols, QtCore.SIGNAL("cellDoubleClicked ( int row, int column )"), self.testRow)
        # QtCore.QObject.connect(self.table, QtCore.SIGNAL("cellDoubleClicked ( int row, int column )"), self.testRow)        # 02)topLeft02--------------------
        self.tableLocalSymbols.itemClicked.connect(self.onClicked)
        self.tableLocalSymbols.cellDoubleClicked.connect(self.onTableLocalSymbolsDoubleClicked)
        
        topLeft01.addWidget(self.tableLocalSymbols)
    def initLayoutCodeMover(self):
        layoutCodeMover = QtGui.QVBoxLayout(self)        
        
        AddOneButton=QtGui.QPushButton(self.tr(">"))
        AddAllButton=QtGui.QPushButton(self.tr(">>>"))  
        DeleteOneButton=QtGui.QPushButton(self.tr("<"))
        DeleteAllButton=QtGui.QPushButton(self.tr("<<<"))  
        
        self.connect(AddOneButton,QtCore.SIGNAL("clicked()"),self.slotAddOne)
        self.connect(AddAllButton,QtCore.SIGNAL("clicked()"),self.slotAddAll)
        self.connect(DeleteOneButton,QtCore.SIGNAL("clicked()"),self.slotDeleteOne)
        self.connect(DeleteAllButton,QtCore.SIGNAL("clicked()"),self.slotDeleteAll)
        
        layoutCodeMover.addWidget(AddOneButton) 
        layoutCodeMover.addWidget(DeleteOneButton)
        layoutCodeMover.addWidget(AddAllButton)
        layoutCodeMover.addWidget(DeleteAllButton)
        return layoutCodeMover
    
    def initLayoutDataSourceSelector(self):
        # 01)topLeft01------------------
        topLeft01Top = QtGui.QHBoxLayout(self)        
        # 01.01 mid codes type
        codesTypeLable = QtGui.QLabel(self.tr("remote data source type:"))  
        dataSourceTypeComboBox=QtGui.QComboBox()
        self.remoteDataSourceTypeComboBox = dataSourceTypeComboBox
        self.dataSourceTypeComboBox = dataSourceTypeComboBox
        dataSourceTypeComboBox.insertItem(0,self.tr("tushare"))
        dataSourceTypeComboBox.insertItem(1,self.tr("sina"))        
        dataSourceTypeComboBox.insertItem(2,self.tr("datayes"))        
        dataSourceTypeComboBox.insertItem(3,self.tr("yahoo"))        
        # 01.02 mid source type
        codesSourceLable = QtGui.QLabel(self.tr("local storage type:")) 
        sourceTypeComboBox=QtGui.QComboBox()
        self.localStorageTypeComboBox = sourceTypeComboBox
        sourceTypeComboBox.insertItem(0,self.tr("mongodb"))        
        sourceTypeComboBox.insertItem(1,self.tr("csv"))
    
        topLeft01Top.addWidget(codesTypeLable)
        topLeft01Top.addWidget(dataSourceTypeComboBox)
        topLeft01Top.addWidget(codesSourceLable)   
        topLeft01Top.addWidget(sourceTypeComboBox)
        
        return topLeft01Top
    def initLayoutCodesTableToDownload(self):
        layoutCodesToDownload = QtGui.QVBoxLayout(self)
        
        initLayoutDataSourceSelector = self.initLayoutDataSourceSelector()
        layoutCodesToDownload.addLayout(initLayoutDataSourceSelector)
        
        self.tableSymbolsToDownload=QtGui.QTableWidget()
        layoutCodesToDownload.addWidget(self.tableSymbolsToDownload)   
        self.tableSymbolsToDownload.cellDoubleClicked.connect(self.onTableSymbolsToDownloadDoubleClicked)
                
        return layoutCodesToDownload
    def initDownloaderParams(self):
        layoutDownloadParams = QtGui.QVBoxLayout(self)           
        
        layoutAddNewSymbol = QtGui.QHBoxLayout(self)
        
        labelNewToDownload = QtGui.QLabel(self.tr('New symbol to download:'))
        self.editSymbolToAdd = QtGui.QLineEdit()
        addNewSymbol = QtGui.QPushButton(self.tr('Add'))   
        layoutAddNewSymbol.addWidget(labelNewToDownload)
        layoutAddNewSymbol.addWidget(self.editSymbolToAdd)
        layoutAddNewSymbol.addWidget(addNewSymbol)         
        self.connect(addNewSymbol,QtCore.SIGNAL("clicked()"),self.slotAddNewSymbol)        
        
        
        layoutParameters = QtGui.QGridLayout(self)
        
        lablePeriod = QtGui.QLabel(self.tr("Period:")) 
        periodComboBox=QtGui.QComboBox()
        self.periodComboBox = periodComboBox
        periodComboBox.insertItem(0,self.tr("D"))
        periodComboBox.insertItem(1,self.tr("min"))
        
        lableTimeStart = QtGui.QLabel(self.tr("Time start:")) 
        timeStart = QtGui.QCalendarWidget()
        timeStart=QtGui.QDateTimeEdit()
        self.timeStartTimeEdit = timeStart
        timeStart.setDateTime(QtCore.QDateTime.fromString('2010-01-01 02:00:00','yyyy-MM-dd hh:mm:ss'))
        timeStart.setDisplayFormat("yyyy-MM-dd hh:mm:ss")
        timeStart.setCalendarPopup(True)  
        lableTimeEnd = QtGui.QLabel(self.tr("Time end"))  
        timeEnd=QtGui.QDateTimeEdit()
        self.timeEndTimeEdit = timeEnd
        timeEnd.setDateTime(QtCore.QDateTime.currentDateTime())
        
        timeEnd.setDisplayFormat("yyyy-MM-dd hh:mm:ss")
        timeEnd.setCalendarPopup(True)                
        
        layoutParameters.addWidget(lablePeriod,1,0)
        layoutParameters.addWidget(periodComboBox,1,1)  
        layoutParameters.addWidget(lableTimeStart,2,0)  
        layoutParameters.addWidget(timeStart,2,1)  
        layoutParameters.addWidget(lableTimeEnd,3,0)  
        layoutParameters.addWidget(timeEnd,3,1)          
        
        DownloadOneButton=QtGui.QPushButton(self.tr("DownloadSelected"))
        DownloadAllButton=QtGui.QPushButton(self.tr("DownloadAll")) 
        self.connect(DownloadOneButton,QtCore.SIGNAL("clicked()"),self.slotDownloadSelected)
        self.connect(DownloadAllButton,QtCore.SIGNAL("clicked()"),self.slotDownloadAll)


        layoutDownloadParams.addLayout(layoutParameters)

        layoutDownloadParams.addLayout(layoutAddNewSymbol)
        layoutDownloadParams.addWidget(DownloadOneButton)
        layoutDownloadParams.addWidget(DownloadAllButton)
        
        return layoutDownloadParams
    def initLayoutCodesSource(self):
        layoutCodesSource = QtGui.QVBoxLayout(self)
        self.initTopCodesSourceSelector(layoutCodesSource)
        self.initCodesTable(layoutCodesSource)  
        return layoutCodesSource
    def initTopUI(self):
        topLayout = QtGui.QHBoxLayout(self)     #mid remote data 
        
        #mid 1) codesSource 
        layoutCodesSource = self.initLayoutCodesSource()   
        #mid 2) 
        layoutCodeMover =  self.initLayoutCodeMover()
        #mid 3)
        layoutCodesToDownload = self.initLayoutCodesTableToDownload()
        #mid 4)
        layoutDownloadParams = self.initDownloaderParams()        

        #mid asignment
        topLayout.addLayout(layoutCodesSource)
        topLayout.addLayout(layoutCodeMover)
        topLayout.addLayout(layoutCodesToDownload)
        topLayout.addLayout(layoutDownloadParams)    
        
        return topLayout
    def initLayoutSymbolsSelector(self):
        layoutSymbolsSelector = QtGui.QHBoxLayout(self)

        label7=QtGui.QLabel(self.tr("locally available symbols:"))
        labelSourceType = QtGui.QLabel('source Type:')
        labelStorageType = QtGui.QLabel(self.tr("storage type:"))
        labelPeriodType = QtGui.QLabel(self.tr("period type:"))
        
        datasourceComboBox = QtGui.QComboBox()
        self.localDatasourceComboBox = datasourceComboBox
        datasourceComboBox.insertItem(0,'tushare')
        datasourceComboBox.insertItem(1,'sina')
        datasourceComboBox.insertItem(2,'yahoo')
        
        storageComboBox = QtGui.QComboBox()
        self.localSymbolsStorageComboBox = storageComboBox
        storageComboBox.insertItem(0,self.tr("mongodb"))
        storageComboBox.insertItem(1,self.tr("csv")) 
        storageComboBox.insertItem(2,self.tr("all")) 
        
        periodComboBox=QtGui.QComboBox()
        self.localSymbolsPeriodComboBox = periodComboBox
        periodComboBox.insertItem(0,self.tr("D"))
        periodComboBox.insertItem(1,self.tr("min"))  
        periodComboBox.insertItem(2,self.tr("all"))  
        
        datasourceComboBox.activated[str].connect(self.onLocalSymbolSelectorActivate)        
        storageComboBox.activated[str].connect(self.onLocalSymbolSelectorActivate)        
        periodComboBox.activated[str].connect(self.onLocalSymbolSelectorActivate)        
        
        
        
        
        layoutSymbolsSelector.addWidget(label7)
        
        layoutSymbolsSelector.addWidget(labelSourceType)
        layoutSymbolsSelector.addWidget(datasourceComboBox)
        
        layoutSymbolsSelector.addWidget(labelStorageType)
        layoutSymbolsSelector.addWidget(storageComboBox)      
        
        layoutSymbolsSelector.addWidget(labelPeriodType)
        layoutSymbolsSelector.addWidget(periodComboBox)        
        
        return layoutSymbolsSelector
    def initLayoutLocalDataSource(self):      
        bottomLeft01 = QtGui.QVBoxLayout(self)  
        # 05)symbols selector
        layoutSymbolsSelector = self.initLayoutSymbolsSelector()
        
        self.tableLocalAvailableSymbols = QtGui.QTableWidget()

        # 06)bottomLeft03
        bottomLeft03 = QtGui.QHBoxLayout(self)
    
        DeleteOneFromDBButton=QtGui.QPushButton(self.tr("DeleteOneFromDB"))
        DeleteAllFromDBButton=QtGui.QPushButton(self.tr("DeleteAllFromDB"))      
        ShowInTableButton=QtGui.QPushButton(self.tr("ShowInTable"))
        ShowInGraphButton=QtGui.QPushButton(self.tr("ShowInGraph"))           
    
        bottomLeft03.addWidget(DeleteOneFromDBButton)
        bottomLeft03.addWidget(DeleteAllFromDBButton)
        bottomLeft03.addWidget(ShowInTableButton)
        bottomLeft03.addWidget(ShowInGraphButton)
        self.connect(ShowInTableButton,QtCore.SIGNAL("clicked()"),self.slotShowInTable)
        self.connect(ShowInGraphButton,QtCore.SIGNAL("clicked()"),self.slotShowInCandleGraph) 
                
        bottomLeft01.addLayout(layoutSymbolsSelector)
        bottomLeft01.addWidget(self.tableLocalAvailableSymbols)
        bottomLeft01.addLayout(bottomLeft03)
        return bottomLeft01
    def initLayoutLocalDataVisualizer(self):
        bottomLeft02 = QtGui.QVBoxLayout(self)  
    
        # 05)bottomLeft02---------------------
        label7=QtGui.QLabel(self.tr("Current symbol graphview:"))
        
        dataForCandle = self.dataCenter.retriveCandleData(datasource = 'tushare',storageType = 'mongodb',symbol = '600028')     
        candle = pgCandleWidgetCross(dataForCandle=dataForCandle)          
        
        
        
        bottomLeft02.addWidget(label7)
        bottomLeft02.addWidget(candle)  
        
        return bottomLeft02
    def initBottomUI(self):
        bottomLayout = QtGui.QHBoxLayout(self)  #mid local data
      
        #mid 1) local data selector
        layoutLocalDataSource = self.initLayoutLocalDataSource()
        
        layoutLocalDataVisualizer = self.initLayoutLocalDataVisualizer()

        # bottom--------------------------------------------------------------------
        bottomLayout.addLayout(layoutLocalDataSource)
        bottomLayout.addLayout(layoutLocalDataVisualizer)
        bottomLayout.setStretch(0, 1)
        bottomLayout.setStretch(1, 2)          
        return bottomLayout
    #----------------------------------------------------------------------
    def initUI(self):
        """mid
        界面整体分为上下结构
        上部为网络数据管理
        1.不同数据源切换(combo)
	2.代码表更新(button),需要显示更新时间
	3.代码表(table)
	4.待下载symbols的代码表(table)
	5.批量下载(按钮)
        下部为本地数据管理
	1.不同仓库切换(combo)
	2.当前仓库已有symbols数据概要展示(symbol,来源，更新日期，barCounts，startDate，endDate)
	3.本地数据操作(删除，更新)
	4.本地数据展示(table,graph)
        """
        mainLayout = QtGui.QVBoxLayout(self)   
        topLayout = self.initTopUI()
        bottomLayout = self.initBottomUI()
        # all----------------------------------------------------------------------
        #mainLayout.addLayout(topLayout)
        mainLayout.addLayout(bottomLayout)
        #mainLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)   
        self.setLayout(mainLayout)
    #----------------------------------------------------------------------
    def updateLocalAvailableSymbolsTable(self):
        """mid
        dfLocalSymbols.index = 'code'
        dfLocalSymbols.columns = ['code','name','c_name',...]
        """
        datasource = self.localDatasourceComboBox.currentText()
        storageType = self.localStorageTypeComboBox.currentText()
        period = self.localSymbolsPeriodComboBox.currentText()        
        
        dfLocalSymbols = self.dataCenter.getLocalAvailableDataSymbols(dataType = datasource,storageType = storageType,periodType = period)

        
        self.tableLocalAvailableSymbols.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)  
        self.tableLocalAvailableSymbols.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)  
        self.tableLocalAvailableSymbols.setSelectionBehavior(QtGui.QTableWidget.SelectRows)  
        self.tableLocalAvailableSymbols.setSelectionMode(QtGui.QTableWidget.SingleSelection)  
        self.tableLocalAvailableSymbols.setAlternatingRowColors(True)         
        
        
        self.tableLocalAvailableSymbols.clear()
        header = ["code","counts","date from","date to"]
        self.tableLocalAvailableSymbols.setColumnCount(len(header))
        
        if(dfLocalSymbols is None):
            self.tableLocalAvailableSymbols.setRowCount(0)
            return        
        
        self.tableLocalAvailableSymbols.setRowCount(len(dfLocalSymbols))
        self.tableLocalAvailableSymbols.setHorizontalHeaderLabels(header)     #mid should be after .setColumnCount()
        
        
        if(True):
            for row in range(len(dfLocalSymbols.index)):
                for column in range(len(dfLocalSymbols.columns)):
                    self.tableLocalAvailableSymbols.setItem(row,column,QtGui.QTableWidgetItem(str(dfLocalSymbols.iget_value(row, column))))        
        else: #mid the above codes have better performance than the below.
            for row in np.arange(0,len(dfLocalSymbols)):
                code = dfLocalSymbols.index[row]
                
                #symbol = QtGui.QLabel(self.tr(code))
                symbol = str(code)
                codeName = dfLocalSymbols.loc[code,'name']
                codeClass = dfLocalSymbols.loc[code,'c_name']
                                   
                #self.tableLocalSymbols.setCellWidget(row,0,symbol)
                self.tableLocalAvailableSymbols.setItem(row,0,QtGui.QTableWidgetItem(symbol))
                self.tableLocalAvailableSymbols.setItem(row,1,QtGui.QTableWidgetItem(codeName))
                self.tableLocalAvailableSymbols.setItem(row,2,QtGui.QTableWidgetItem(codeClass))    
    #----------------------------------------------------------------------
    def updateLocalSymbolsTable(self):
        """mid
        dfLocalSymbols.index = 'code'
        dfLocalSymbols.columns = ['code','name','c_name',...]
        """
        self.tableLocalSymbols.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)  
        self.tableLocalSymbols.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)  
        self.tableLocalSymbols.setSelectionBehavior(QtGui.QTableWidget.SelectRows)  
        self.tableLocalSymbols.setSelectionMode(QtGui.QTableWidget.SingleSelection)  
        self.tableLocalSymbols.setAlternatingRowColors(True)         
        
        
        self.tableLocalSymbols.clear()
        header = ["code","name","class","listed date","stop date","trade days"]
        self.tableLocalSymbols.setColumnCount(len(header))
        
        if(self.tableLocalSymbols is None):
            self.tableLocalSymbols.setRowCount(0)
            return  
        
        self.tableLocalSymbols.setRowCount(len(self.dfLocalSymbols))
        self.tableLocalSymbols.setHorizontalHeaderLabels(header)     #mid should be after .setColumnCount()
        
        if (PY3 == True):#mid 这种填充方式虽然快，但是，当item有中文编码时，在py2下会出现问题
            for row in range(len(self.dfLocalSymbols.index)):
                for column in range(len(self.dfLocalSymbols.columns)):
                    strItem = str(self.dfLocalSymbols.iget_value(row, column))
                    self.tableLocalSymbols.setItem(row,column,QtGui.QTableWidgetItem(strItem))        
        else: #mid the above codes have better performance than the below.
            for row in np.arange(0,len(self.dfLocalSymbols)):
                code = self.dfLocalSymbols.index[row]
                
                #symbol = QtGui.QLabel(self.tr(code))
                symbol = str(code)
                codeName = self.dfLocalSymbols.loc[code,'name']
                codeClass = self.dfLocalSymbols.loc[code,'c_name']
                                   
                #self.tableLocalSymbols.setCellWidget(row,0,symbol)
                self.tableLocalSymbols.setItem(row,0,QtGui.QTableWidgetItem(symbol))
                self.tableLocalSymbols.setItem(row,1,QtGui.QTableWidgetItem(codeName))
                self.tableLocalSymbols.setItem(row,2,QtGui.QTableWidgetItem(codeClass))
    def updateSymbolsToDownloadTable(self):
        """mid
        dfSymbolsToDownload.index = 'code'
        dfSymbolsToDownload.columns = ['code','name','c_name',...]
        """        
        self.tableSymbolsToDownload.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)  
        self.tableSymbolsToDownload.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)  
        self.tableSymbolsToDownload.setSelectionBehavior(QtGui.QTableWidget.SelectRows)  
        self.tableSymbolsToDownload.setSelectionMode(QtGui.QTableWidget.SingleSelection)  
        self.tableSymbolsToDownload.setAlternatingRowColors(True)         
        
        
        self.tableSymbolsToDownload.clear()
        header = ["code","name","class"]
        self.tableSymbolsToDownload.setColumnCount(len(header))
        self.tableSymbolsToDownload.setRowCount(len(self.dfSymbolsToDownload))
        self.tableSymbolsToDownload.setHorizontalHeaderLabels(header)     #mid should be after .setColumnCount()
        
        if (PY3 == True):#mid 这种填充方式虽然快，但是，当item有中文编码时，在py2下会出现问题
            for row in range(len(self.dfSymbolsToDownload.index)):
                for column in range(len(self.dfSymbolsToDownload.columns)):
                    self.tableSymbolsToDownload.setItem(row,column,QtGui.QTableWidgetItem(str(self.dfSymbolsToDownload.iget_value(row, column))))                         
        else: #mid the above codes have better performance than the below.        
            for row in np.arange(0,len(self.dfSymbolsToDownload)):
                symbol = self.dfSymbolsToDownload.index[row]
                name = self.dfSymbolsToDownload.loc[symbol,'name']
                c_name = self.dfSymbolsToDownload.loc[symbol,'c_name']
                
                timeStart = QtGui.QCalendarWidget()
                timeStart=QtGui.QDateTimeEdit()
                timeStart.setDateTime(QtCore.QDateTime.currentDateTime())
                timeStart.setDisplayFormat("yyyy-MM-dd hh:mm:ss")
                timeStart.setCalendarPopup(True)  
                timeEnd=QtGui.QDateTimeEdit()
                timeEnd.setDateTime(QtCore.QDateTime.currentDateTime())
                timeEnd.setDisplayFormat("yyyy-MM-dd hh:mm:ss")
                timeEnd.setCalendarPopup(True)               
                                   
                self.tableSymbolsToDownload.setItem(row,0,QtGui.QTableWidgetItem(symbol))
                self.tableSymbolsToDownload.setItem(row,1,QtGui.QTableWidgetItem(name))
                self.tableSymbolsToDownload.setItem(row,2,QtGui.QTableWidgetItem(c_name))
                self.tableSymbolsToDownload.setCellWidget(row,3,timeStart)
                self.tableSymbolsToDownload.setCellWidget(row,4,timeEnd)    
    #----------------------------------------------------------------------
    def slotAddOne(self):
        rowSelected = self.tableLocalSymbols.currentRow()
        if((rowSelected<0) and (self.tableLocalSymbols.rowCount()>0)):
            rowSelected = 0
            
        if(rowSelected>=0):   #a row selected or table is not empty.
            code = self.tableLocalSymbols.item(rowSelected,0).text()
            name = self.tableLocalSymbols.item(rowSelected,1).text()
            c_name = self.tableLocalSymbols.item(rowSelected,2).text()
            
            code = str(code)
            
            self.dfSymbolsToDownload.loc[code,'code'] = code            
            self.dfSymbolsToDownload.loc[code,'name'] = name
            self.dfSymbolsToDownload.loc[code,'c_name'] = c_name
            
            self.updateSymbolsToDownloadTable()

    def slotDeleteOne(self):
        rowSelected = self.tableSymbolsToDownload.currentRow()
        if((rowSelected<0) and (self.tableSymbolsToDownload.rowCount()>0)):
            rowSelected = 0
            
        if(rowSelected>=0):   #a row selected or table is not empty.
            
            code = self.tableSymbolsToDownload.item(rowSelected,0).text()
            self.dfSymbolsToDownload.drop(code,inplace=True)
            
            self.updateSymbolsToDownloadTable()
    def slotDeleteAll(self):
        pass
    def slotAddAll(self):
        pass    
    #----------------------------------------------------------------------
    def slotAddNewSymbol(self):
        """"""
        code = self.editSymbolToAdd.text()
        if(len(code)==0 and (not code.isnumeric())):
            symbol = 'none to download.'
            QtGui.QMessageBox.information(self,"Information",self.tr(symbol))   
        else:
            self.dfSymbolsToDownload.loc[code,'code'] = code
            #self.dfSymbolsToDownload.loc[text] = None
            self.updateSymbolsToDownloadTable()
        #QtGui.QMessageBox.information(self,"Information",self.tr("You are right!"+text))
    #----------------------------------------------------------------------
    def slotShowInTable(self):
        """
        show currrent selected symbol in table
        """
        def getRawDataFromMongodb():
            # 1)connect to Mongodb 
            connect = Mongodb('192.168.0.212', 27017)
            connect.use('Tushare')    #database
            
            # 2)retrive data from specified collection
            symbol = '600028'
            strStart = '2015-01-01'
            dateEnd = dt.datetime.now()
            strEnd = dateEnd.strftime('%Y-%m-%d')  
            frequency = 'D'
            connect.setCollection(frequency)    #table
            return connect.retrive(symbol,strStart,strEnd,frequency)        
            
        data = getRawDataFromMongodb()
        self.tableHistory=HistoryTableView(rawData=data)
        self.tableHistory.setWindowTitle("history")
        self.tableHistory.show()        
    def slotShowInCandleGraph(self):
        rowSelected = self.tableLocalAvailableSymbols.currentRow()
        if((rowSelected<0) and (self.tableLocalAvailableSymbols.rowCount()>0)):
            rowSelected = 0
            
        if(rowSelected>=0):   #a row selected or table is not empty.
            datasource = self.localDatasourceComboBox.currentText()
            storageType = self.localStorageTypeComboBox.currentText()
            symbolToDownload = self.tableLocalAvailableSymbols.item(rowSelected,0).text()
            period = self.localSymbolsPeriodComboBox.currentText()
            #history = self.dataCenter.retriveHistData(symbolToDownload)
            
            dataForCandle = self.dataCenter.retriveCandleData(datasource = datasource,storageType = storageType,symbol = symbolToDownload)     
            self.__showCandle__(dataForCandle)
            #self.myWindowfff = MyDialog(dataForCandle=dataForCandle)  
            #self.myWindowfff.show()                        
        else:   #none selected and empty table
            symbol = 'none to download.'
            QtGui.QMessageBox.information(self,"Information",self.tr(symbol)) 
    def __showCandle__(self,dataForCandle):
        dialog = QtGui.QDialog()
        self.pgCandleView = dialog
        layout = QtGui.QHBoxLayout()
        layoutLeft = QtGui.QVBoxLayout()
        layout.addLayout(layoutLeft)
        dialog.setLayout(layout)        
        dialog.setWindowTitle(('ComboView'))
        # 2) creates widgets 
        editor = QtGui.QTextEdit()
        editor.setText("<span style='font-size: 15pt' style='color: red'>x = %0.1f,y = %0.1f</span>"% (2.0,2.0))
    
        candle = pgCandleWidgetCross(dataForCandle=dataForCandle)  
        #candle = pgCrossAddition()
        # 3)arrange widgets
        #layout.addWidget(editor)
        layout.addWidget(candle)
        dialog.showMaximized()           
    def messageBoxAfterDownloaded(self,dataDict):
        countsDownloaded = len(dataDict)
        if(countsDownloaded<=0):
            QtGui.QMessageBox.information(self,"Information",self.tr('None downloaded.')) 
        else:
            strCodesDownloaded = '\n'
            for code in dataDict:
                strCodesDownloaded = strCodesDownloaded + code + '\n'
            QtGui.QMessageBox.information(self,"Information",self.tr(str(countsDownloaded)+' downloaded.'+'\ncodes list:'+strCodesDownloaded))         
#----------------------------------------------------------------------
    def slotDownloadAll(self):
        """"""
        if(len(self.dfSymbolsToDownload)>0):
            symbols = self.dfSymbolsToDownload['code']
            codeList=symbols.tolist()

            remoteDataSourceType = self.remoteDataSourceTypeComboBox.currentText()
            localStorageType = self.localStorageTypeComboBox.currentText()            
            
            periodType = self.periodComboBox.currentText()
            
            
            timeStart = self.timeStartTimeEdit.dateTime().toPyDateTime()
            strStart = timeStart.strftime('%Y-%m-%d')
            
            timeEnd = datetime.now()
            strEnd = timeEnd.strftime('%Y-%m-%d')  
                        
            # 2)download history data
            dataDict = self.dataCenter.downloadHistData(providerType=remoteDataSourceType,storageType=localStorageType,periodType=periodType,
                                                        codeList=codeList,timeStart=strStart,timeEnd=strEnd)
            self.messageBoxAfterDownloaded(dataDict)   
            
        else:
            symbol = 'none to download.'
            QtGui.QMessageBox.information(self,"Information",self.tr(symbol))
        self.updateLocalAvailableSymbolsTable()
        
    #----------------------------------------------------------------------
    def slotDownloadSelected(self):
        """"""
        rowSelected = self.tableSymbolsToDownload.currentRow()
        if((rowSelected<0) and (self.tableSymbolsToDownload.rowCount()>0)):
            rowSelected = 0
        if(rowSelected>=0):   #a row selected or table is not empty.
            symbolToDownload = self.tableSymbolsToDownload.item(rowSelected,0).text()
            codeList=[symbolToDownload]

            remoteDataSourceType = self.remoteDataSourceTypeComboBox.currentText()
            localStorageType = self.localStorageTypeComboBox.currentText()            
            
            periodType = self.periodComboBox.currentText()
            
            timeStart = self.timeStartTimeEdit.dateTime().toPyDateTime()
            strStart = timeStart.strftime('%Y-%m-%d')
            
            timeEnd = datetime.now()
            strEnd = timeEnd.strftime('%Y-%m-%d')  
                        
            # 2)download history data
            dataDict = self.dataCenter.downloadHistData(providerType=remoteDataSourceType,storageType=localStorageType,periodType=periodType,
                                                        codeList=codeList,timeStart=strStart,timeEnd=strEnd)
            self.messageBoxAfterDownloaded(dataDict)
        else:   #none selected and empty table
            symbol = 'none to download.'
            QtGui.QMessageBox.information(self,"Information",self.tr(symbol))     
class MyDialog(QtGui.QDialog):  
    def __init__(self,dataForCandle=None, parent=None):  
        super(MyDialog, self).__init__(parent)  
        # 1) set mainlayout
        layout = QtGui.QHBoxLayout()  
        self.setLayout(layout)     
        # 2) creates layoutLeft and add it to mainlayout
        layoutLeft = QtGui.QVBoxLayout()  
        layout.addLayout(layoutLeft)  
        # 3) add table to layoutLeft
        barLable = QtGui.QLabel('Bar Info:')        
        self.MyTable = QtGui.QTableWidget(4,2)  
        self.MyTable.setHorizontalHeaderLabels(['Item','data'])  
        newItem = QtGui.QTableWidgetItem("datetime")  
        newItem = QtGui.QTableWidgetItem("2015-07-05 22:00:00")          
        self.MyTable.setItem(0, 0, newItem)  
        self.MyTable.setItem(0, 1, newItem) 
        layoutLeft.addWidget(barLable)
        layoutLeft.addWidget(self.MyTable)  
        # 4) add edit to layoutLeft
        infoLable = QtGui.QLabel('Symbol Info:')
        self.infoEdit=QtGui.QTextEdit()
        layoutLeft.addWidget(infoLable)
        layoutLeft.addWidget(self.infoEdit)
        # 5) add canvas to layoutLeft
        fig = plt.figure()
        fig.subplots_adjust(top=0.98,bottom=0.05,left=0.15,right=0.99,hspace =0.1,wspace = 0.1) 
        self.fig = fig
        ax1 = fig.add_subplot(1,1,1) 
        
        mu, sigma    =    100,    15
        x    =    mu    +    sigma    *    np.random.randn(10000)# the histogram of the data
        n, bins, patches =  plt.hist(x,50, normed=1, facecolor='g', alpha=0.75)
        ax1.set_xlabel('Smarts')
        ax1.set_ylabel('Probability')
        ax1.set_title('Histogram of IQ')
        ax1.text(60,.025,'$\mu=100,\\sigma=15$')
        ax1.axis([40,160,0,0.03])
        ax1.grid(True)        

        fig.tight_layout()
        detailCanvas = FigureCanvas(fig)
        layoutLeft.addWidget(detailCanvas)
        # 4) add button to layoutLeft
        button01 = QtGui.QPushButton('HistoryCandleView')   
        button02 = QtGui.QPushButton('3D')
        layoutLeft.addWidget(button01)
        layoutLeft.addWidget(button02)   
        self.connect(button01,QtCore.SIGNAL("clicked()"),self.slotOK01)
        self.connect(button02,QtCore.SIGNAL("clicked()"),self.slotOK02)        
        # 5) add candleView to mainlayout
        canvas = HistoryCandleView(dataForCandle=dataForCandle,fnUpdateBarInfoCallback=self.updateBarInfo)        
        layout.addWidget(canvas)
        
        layout.setStretchFactor(layoutLeft,10)
        layout.setStretchFactor(canvas,60)
    #----------------------------------------------------------------------
    def updateBarInfo(self,event):
        """"""
        #info = 'event.name:{}\nButton:{}\nFig x,y:{}, {}\nData x:{},\nData y:{}'.format(
            #event.name,event.button,event.x,event.y,mpd.num2date(event.xdata),event.ydata) 
        info = 'event.name:{}\nButton:{}\nFig x,y:{}, {}\nData x:{},\nData y:{}'.format(
            event.name,event.button,event.x,event.y,dt.datetime.strftime(mpd.num2date(event.xdata),'%Y-%m-%d %H:%M:%S')  ,event.ydata)        
        self.infoEdit.setText(info)    
    #----------------------------------------------------------------------
    def slotOK01(self):
        """"""
        self.mainWindow=QtGui.QMainWindow()
        self.mainWindow.setWindowTitle(self.tr("GraphView"))
    
        graphView = QtGui.QWidget(self.mainWindow)
        layout = QtGui.QVBoxLayout(graphView)
        
        def getCandleData():
            xpower = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,os.pardir,'histdata'))
            sys.path.append(xpower)
        
            import feedsForCandle as feedsForCandle
        
            dataSource={}
            dataSource['ip']='192.168.0.212'
            dataSource['port']=27017
            dataSource['database']='Tushare'
            dataSource['symbol']='600028'
            dataSource['dateStart']='2013-08-19'
            dataSource['dateEnd']='2015-08-31'
            dataSource['frequency']='D'
            dataForCandle = feedsForCandle.GetCandlesFromMongodb(dataSource)
            return dataForCandle    
        
        candleData = getCandleData()  
        
        graph = HistoryCandleView(dataForCandle=candleData)
        
        layout.addWidget(graph)
        self.mainWindow.setCentralWidget(graphView)          
        self.mainWindow.show()
    #----------------------------------------------------------------------
    def slotOK02(self):
        """"""
        from mpl_toolkits.mplot3d import Axes3D
        import matplotlib.pyplot as plt
        import numpy as np
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        x, y = np.random.rand(2, 100) * 4
        hist, xedges, yedges = np.histogram2d(x, y, bins=4)
        
        elements = (len(xedges) - 1) * (len(yedges) - 1)
        xpos, ypos = np.meshgrid(xedges[:-1] + 0.25, yedges[:-1] + 0.25)
        
        xpos = xpos.flatten()
        ypos = ypos.flatten()
        zpos = np.zeros(elements)
        dx = 0.5 * np.ones_like(zpos)
        dy = dx.copy()
        dz = hist.flatten()
        
        ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color='b', zsort='average')
        
        fig.show()

if __name__ == '__main__':
    qApp=QtGui.QApplication(sys.argv)
    dialog=DataManagerDialog()
    dialog.showMaximized()      
    sys.exit(qApp.exec_())    
