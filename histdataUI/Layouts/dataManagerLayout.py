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
dataRoot = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,os.pardir,'histdata'))        
sys.path.append(dataRoot)        
import dataCenter as dataCenter    
import feedsForCandle as feedsForCandle
from data.mongodb.DataSourceMongodb import Mongodb

windowsRoot = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir))
sys.path.append(windowsRoot)
from Widgets.pgCandleWidgetCross import pgCandleWidgetCross
from Views.HistoryCandleView import HistoryCandleView
from Views.HistoryTableView import HistoryTableView
class dataManagerLayout(QtGui.QHBoxLayout):
    def __init__(self,parent=None):
        self.parent = parent
        super(dataManagerLayout,self).__init__()       
        #mid data
        self.dataCenter = dataCenter.dataCenter()           
        
        
        self.dfSymbolsToDownload = pd.DataFrame(columns=['code','name','c_name'])
        
        
        
        
        #mid 1) codesSource 
        layoutCodesSource = self.initLayoutCodesSource()   
        #mid 2) 
        layoutCodeMover =  self.initLayoutCodeMover()
        #mid 3)
        layoutCodesToDownload = self.initLayoutCodesTableToDownload()
        #mid 4)
        layoutDownloadParams = self.initDownloaderParams()        

        #mid asignment
        self.addLayout(layoutCodesSource)
        self.addLayout(layoutCodeMover)
        self.addLayout(layoutCodesToDownload)
        self.addLayout(layoutDownloadParams)  
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
    def initLayoutCodeMover(self):
        layoutCodeMover = QtGui.QVBoxLayout()        
        
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
                                   
                if(symbol is not None):
                    self.tableSymbolsToDownload.setItem(row,0,QtGui.QTableWidgetItem(symbol))
                if(name is not None):
                    self.tableSymbolsToDownload.setItem(row,1,QtGui.QTableWidgetItem(name))
                if(c_name is not None):
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
        code = str(code)
        
        if(len(code)==0 and (not code.isnumeric())):
            symbol = 'none to download.'
            QtGui.QMessageBox.information(self,"Information",self.tr(symbol))   
        else:
            self.dfSymbolsToDownload.loc[code,'code'] = code
            self.dfSymbolsToDownload.loc[code,'name'] = ''
            self.dfSymbolsToDownload.loc[code,'c_name'] = ''
            self.updateSymbolsToDownloadTable()
        #QtGui.QMessageBox.information(self,"Information",self.tr("You are right!"+text))
    def onTableSymbolsToDownloadDoubleClicked(self, rowSelected,column ):
        self.slotDeleteOne()
    def onTableLocalSymbolsDoubleClicked(self , rowSelected,column ):
        self.slotAddOne()   
        
    def onClicked(self):
        print ('******row : ' , self.tableLocalSymbols.currentRow(), ' ***********')
        
        rows = self.tableLocalSymbols.rowCount()

        #for rows_index in range(rows):
            ##print items[item_index].text()
            #print (self.tableLocalSymbols.item(rows_index,0).text())    
    
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
        
    def onVerSectionClicked(self,index):
        print (index)
    def onHorSectionClicked(self,index):
        print (index) 
        #self.tableLocalSymbols.resizeColumnsToContents()#根据内容调整行的宽度
        #self.tableLocalSymbols.resizeRowToContents()#根据内容调整列的宽度度
        #self.tableLocalSymbols.item(row,col).setTextAlignment(Qt.AlignCenter)#设置字体居中 
    def initTopCodesSourceSelector(self,topLeft01):
        # 01)topLeft01------------------
        topLeft01Top = QtGui.QHBoxLayout()        
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
    def initLayoutCodesSource(self):
        layoutCodesSource = QtGui.QVBoxLayout()
        self.initTopCodesSourceSelector(layoutCodesSource)
        self.initCodesTable(layoutCodesSource)  
        return layoutCodesSource    
    def initLayoutDataSourceSelector(self):
        # 01)topLeft01------------------
        topLeft01Top = QtGui.QHBoxLayout()        
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
        layoutCodesToDownload = QtGui.QVBoxLayout()
        
        initLayoutDataSourceSelector = self.initLayoutDataSourceSelector()
        layoutCodesToDownload.addLayout(initLayoutDataSourceSelector)
        
        self.tableSymbolsToDownload=QtGui.QTableWidget()
        layoutCodesToDownload.addWidget(self.tableSymbolsToDownload)   
        self.tableSymbolsToDownload.cellDoubleClicked.connect(self.onTableSymbolsToDownloadDoubleClicked)
                
        return layoutCodesToDownload
    def initDownloaderParams(self):
        layoutDownloadParams = QtGui.QVBoxLayout()           
        
        layoutAddNewSymbol = QtGui.QHBoxLayout()
        
        labelNewToDownload = QtGui.QLabel(self.tr('New symbol to download:'))
        self.editSymbolToAdd = QtGui.QLineEdit()
        addNewSymbol = QtGui.QPushButton(self.tr('Add'))   
        layoutAddNewSymbol.addWidget(labelNewToDownload)
        layoutAddNewSymbol.addWidget(self.editSymbolToAdd)
        layoutAddNewSymbol.addWidget(addNewSymbol)         
        self.connect(addNewSymbol,QtCore.SIGNAL("clicked()"),self.slotAddNewSymbol)        
        
        
        layoutParameters = QtGui.QGridLayout()
        
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
            QtGui.QMessageBox.information(self.parent,"Information",self.tr(symbol))        
    def messageBoxAfterDownloaded(self,dataDict):
        countsDownloaded = len(dataDict)
        if(countsDownloaded<=0):
            QtGui.QMessageBox.information(self.parent,"Information",self.tr('None downloaded.')) 
        else:
            strCodesDownloaded = '\n'
            for code in dataDict:
                strCodesDownloaded = strCodesDownloaded + code + '\n'
            QtGui.QMessageBox.information(self.parent,"Information",self.tr(str(countsDownloaded)+' downloaded.'+'\ncodes list:'+strCodesDownloaded))    
    def slotDownloadSelected(self):
        """"""
        rowSelected = self.tableSymbolsToDownload.currentRow()
        if((rowSelected<0) and (self.tableSymbolsToDownload.rowCount()>0)):
            rowSelected = 0
        if(rowSelected>=0):   #a row selected or table is not empty.
            symbolToDownload = self.tableSymbolsToDownload.item(rowSelected,0).text()
            codeList=[str(symbolToDownload)]

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


if __name__ == '__main__':
    class MainWindow(QtGui.QMainWindow):
        def __init__(self):
            super(MainWindow, self).__init__()
            cw = QtGui.QWidget()
            self.setCentralWidget(cw) 
            cw.setLayout(dataManagerLayout(self))   
    app = QtGui.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.showMaximized()
    sys.exit(app.exec_())