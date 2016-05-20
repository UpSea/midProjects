# -*- coding: utf-8 -*-
from PyQt4 import QtGui,QtCore
import numpy as np
import pandas as pd
from datetime import datetime
import datetime as dt
import os,sys
xpower = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,'histdata','mongodb'))
sys.path.append(xpower)
xpower = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,'histdata'))
sys.path.append(xpower)

import feedsForCandle as feedsForCandle
from data.mongodb.DataSourceMongodb import Mongodb
import matplotlib.dates as mpd
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

from Views.HistoryCandleView import HistoryCandleView
from Views.HistoryTableView import HistoryTableView
class DataManagerDialog(QtGui.QDialog):
    def __init__(self,parent=None):
        super(DataManagerDialog,self).__init__(parent)
        self.setWindowTitle(self.tr("DataManager"))
        self.initUI()
        # 显示文本内容，并根据文本长度调整标签控件的大小
        import os,sys
        dataRoot = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,os.pardir,'histdata'))        
        sys.path.append(dataRoot)        
        import dataCenter as dataCenter
        #mid data
        self.dataCenter = dataCenter.dataCenter()        
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
        self.dfSymbolsToDownload = pd.DataFrame(columns=['name','c_name','dateFrom','dateTo'])        
        
        QtGui.QMessageBox.information(self,codesType + ' codesTable data.',  'from '+sourceType+' gotten.')    

        self.updateLocalSymbolsTable()  
        self.updateSymbolsToDownloadTable() 
        
    def initTopCodesSelector(self,topLeft01Top):
        # 01)topLeft01------------------
        # 01.01 mid codes type
        codesTypeLable = QtGui.QLabel(self.tr("codes type:"))  
        codesTypeComboBox=QtGui.QComboBox()
        self.codesTypeComboBox = codesTypeComboBox
        codesTypeComboBox.insertItem(0,self.tr("tushare"))
        codesTypeComboBox.insertItem(1,self.tr("sina"))        
        codesTypeComboBox.insertItem(2,self.tr("datayes"))        
        codesTypeComboBox.insertItem(3,self.tr("yahoo"))        
        codesTypeComboBox.activated[str].connect(self.onActivate)        
        # 01.02 mid source type
        codesSourceLable = QtGui.QLabel(self.tr("source type:")) 
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
    #----------------------------------------------------------------------   
    def onVerSectionClicked(self,index):
        print (index)
    def onHorSectionClicked(self,index):
        print (index) 
        #self.tableLocalSymbols.resizeColumnsToContents()#根据内容调整行的宽度
        #self.tableLocalSymbols.resizeRowToContents()#根据内容调整列的宽度度
        #self.tableLocalSymbols.item(row,col).setTextAlignment(Qt.AlignCenter)#设置字体居中        
              
    def onDoubleClicked(self , row,column ):
        print ('******row : ' , row , ' column : ' , column , ' ***********')
        codesColumnIndex = 0
        codesItem = self.tableLocalSymbols.item(row,codesColumnIndex)
        print (codesItem.text())        
        print (self.tableLocalSymbols.currentItem().text())
    def onClicked(self  ):
        print ('******row : ' , self.tableLocalSymbols.currentRow(), ' ***********')
        
        rows = self.tableLocalSymbols.rowCount()

        #for rows_index in range(rows):
            ##print items[item_index].text()
            #print (self.tableLocalSymbols.item(rows_index,0).text())    
    def initTopUI(self,topLayout):
        topLeft01 = QtGui.QVBoxLayout(self)
        topLeft01Top = QtGui.QHBoxLayout(self)
        topLeft02 = QtGui.QVBoxLayout(self)
        topLeft03 = QtGui.QVBoxLayout(self)
        topLeft03Bottom = QtGui.QHBoxLayout(self)
        topLeft04 = QtGui.QVBoxLayout(self)   
        

        self.initTopCodesSelector(topLeft01Top)
        topLeft01.addLayout(topLeft01Top)
        
        self.tableLocalSymbols=QtGui.QTableWidget()
        self.tableLocalSymbols.horizontalHeader().setStretchLastSection(True)                   #mid 可以设置最后一览大小自适应
        topLeft01.addWidget(self.tableLocalSymbols)
        self.tableLocalSymbols.verticalHeader().sectionClicked.connect(self.onVerSectionClicked)#表头单击信号
        self.tableLocalSymbols.horizontalHeader().sectionClicked.connect(self.onHorSectionClicked)#表头单击信号     
        
        #self.connect(self.tableLocalSymbols, QtCore.SIGNAL("itemClicked(QTableWidgetItem* item)"), self.testRow2)
        # QtCore.QObject.connect(self.table, QtCore.SIGNAL("cellActivated ( int row, int column )"), self.testRow)
        #self.connect(self.tableLocalSymbols, QtCore.SIGNAL("cellDoubleClicked ( int row, int column )"), self.testRow)
        # QtCore.QObject.connect(self.table, QtCore.SIGNAL("cellDoubleClicked ( int row, int column )"), self.testRow)        # 02)topLeft02--------------------
        self.tableLocalSymbols.itemClicked.connect(self.onClicked)
        self.tableLocalSymbols.cellDoubleClicked.connect(self.onDoubleClicked)
        
        AddOneButton=QtGui.QPushButton(self.tr(">"))
        AddAllButton=QtGui.QPushButton(self.tr(">>>"))  
        DeleteOneButton=QtGui.QPushButton(self.tr("<"))
        DeleteAllButton=QtGui.QPushButton(self.tr("<<<"))  
        topLeft02.addWidget(AddOneButton)
        topLeft02.addWidget(AddAllButton)
        topLeft02.addWidget(DeleteOneButton)
        topLeft02.addWidget(DeleteAllButton)
        self.connect(AddOneButton,QtCore.SIGNAL("clicked()"),self.slotAddOne)
        self.connect(AddAllButton,QtCore.SIGNAL("clicked()"),self.slotAddAll)
        self.connect(DeleteOneButton,QtCore.SIGNAL("clicked()"),self.slotDeleteOne)
        self.connect(DeleteAllButton,QtCore.SIGNAL("clicked()"),self.slotDeleteAll)
        
        # 03topLeft03-------------------
        labelNewToDownload = QtGui.QLabel(self.tr('New Symbol:'))
        self.editSymbolToAdd = QtGui.QLineEdit()
        addNewSymbol = QtGui.QPushButton(self.tr('Add'))   
        topLeft03Bottom.addWidget(labelNewToDownload)
        topLeft03Bottom.addWidget(self.editSymbolToAdd)
        topLeft03Bottom.addWidget(addNewSymbol)   
    
        labelSymbolsToDownload=QtGui.QLabel(self.tr("SymbolsToDownload:"))
        self.tableSymbolsToDownload=QtGui.QTableWidget()
    
        topLeft03.addWidget(labelSymbolsToDownload)
        topLeft03.addWidget(self.tableSymbolsToDownload)   
        topLeft03.addLayout(topLeft03Bottom)
    
        self.connect(addNewSymbol,QtCore.SIGNAL("clicked()"),self.slotAddNewSymbol)
        # 04)topLeft04----------------------
        DownloadOneButton=QtGui.QPushButton(self.tr("DownloadOne"))
        DownloadAllButton=QtGui.QPushButton(self.tr("DownloadAll")) 
        lablePeriod = QtGui.QLabel(self.tr("Period")) 
        lableTimeStart = QtGui.QLabel(self.tr("Time start")) 
        timeStart = QtGui.QCalendarWidget()
        timeStart=QtGui.QDateTimeEdit()
        timeStart.setDateTime(QtCore.QDateTime.currentDateTime())
        timeStart.setDisplayFormat("yyyy-MM-dd hh:mm:ss")
        timeStart.setCalendarPopup(True)  
        lableTimeEnd = QtGui.QLabel(self.tr("Time end"))  
        timeEnd=QtGui.QDateTimeEdit()
        timeEnd.setDateTime(QtCore.QDateTime.currentDateTime())
        timeEnd.setDisplayFormat("yyyy-MM-dd hh:mm:ss")
        timeEnd.setCalendarPopup(True)        
        periodComboBox=QtGui.QComboBox()
        periodComboBox.insertItem(0,self.tr("D"))
        periodComboBox.insertItem(1,self.tr("min"))
    
        topLeft04.addWidget(lablePeriod)
        topLeft04.addWidget(periodComboBox)
        topLeft04.addWidget(lableTimeStart)
        topLeft04.addWidget(timeStart)
        topLeft04.addWidget(lableTimeEnd)
        topLeft04.addWidget(timeEnd)
        topLeft04.addWidget(DownloadOneButton)
        topLeft04.addWidget(DownloadAllButton)      
    
        self.connect(DownloadOneButton,QtCore.SIGNAL("clicked()"),self.slotDownloadOne)
        self.connect(DownloadAllButton,QtCore.SIGNAL("clicked()"),self.slotDownloadAll)        
        
        # top---------------------------------------------------------------------
        topLayout.addLayout(topLeft01)
        topLayout.addLayout(topLeft02)
        topLayout.addLayout(topLeft03)
        topLayout.addLayout(topLeft04)    
    def initBottomUI(self,bottomLayout):
        bottomLeft01 = QtGui.QVBoxLayout(self)  
        bottomLeft02 = QtGui.QVBoxLayout(self)  
    
        # 05)bottomLeft01----------------------
        label7=QtGui.QLabel(self.tr("Current local symbol description"))
        descTextEdit=QtGui.QTextEdit()        
        bottomLeft01.addWidget(label7)
        bottomLeft01.addWidget(descTextEdit)        
        # 05)bottomLeft02---------------------
        label7=QtGui.QLabel(self.tr("Current symbol to download description:"))
        descTextEdit=QtGui.QTextEdit() 
        bottomLeft02.addWidget(label7)
        bottomLeft02.addWidget(descTextEdit)
    
    
        # 06)bottomLeft03
        bottomLeft03 = QtGui.QVBoxLayout(self)
    
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
    
        # bottom--------------------------------------------------------------------
        bottomLayout.addLayout(bottomLeft01)
        bottomLayout.addLayout(bottomLeft02)
        bottomLayout.addLayout(bottomLeft03)           
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
        topLayout = QtGui.QHBoxLayout(self)     #mid remote data 
        
        bottomLayout = QtGui.QHBoxLayout(self)  #mid local data
        self.initTopUI(topLayout)
        self.initBottomUI(bottomLayout)
        # all----------------------------------------------------------------------
        mainLayout.addLayout(topLayout)
        mainLayout.addLayout(bottomLayout)
        #mainLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)        
    #----------------------------------------------------------------------
    def updateLocalSymbolsTable(self):
        """"""
        self.tableLocalSymbols.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)  
        self.tableLocalSymbols.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)  
        self.tableLocalSymbols.setSelectionBehavior(QtGui.QTableWidget.SelectRows)  
        self.tableLocalSymbols.setSelectionMode(QtGui.QTableWidget.SingleSelection)  
        self.tableLocalSymbols.setAlternatingRowColors(True)         
        
        
        self.tableLocalSymbols.clear()
        header = ["code","name","class","listed date","stop date","trade days"]
        self.tableLocalSymbols.setColumnCount(len(header))
        self.tableLocalSymbols.setRowCount(len(self.dfLocalSymbols))
        self.tableLocalSymbols.setHorizontalHeaderLabels(header)     #mid should be after .setColumnCount()
        
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
        ''''''
        self.tableSymbolsToDownload.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)  
        self.tableSymbolsToDownload.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)  
        self.tableSymbolsToDownload.setSelectionBehavior(QtGui.QTableWidget.SelectRows)  
        self.tableSymbolsToDownload.setSelectionMode(QtGui.QTableWidget.SingleSelection)  
        self.tableSymbolsToDownload.setAlternatingRowColors(True)         
        
        
        self.tableSymbolsToDownload.clear()
        header = ["sybol","name","start","end"]
        self.tableSymbolsToDownload.setColumnCount(len(header))
        self.tableSymbolsToDownload.setRowCount(len(self.dfSymbolsToDownload))
        self.tableSymbolsToDownload.setHorizontalHeaderLabels(header)     #mid should be after .setColumnCount()
        
        for row in np.arange(0,len(self.dfSymbolsToDownload)):
            symbol = self.dfSymbolsToDownload.index[row]
            name = str(self.dfSymbolsToDownload.loc[symbol,'name'])
            c_name = str(self.dfSymbolsToDownload.loc[symbol,'c_name'])
            
            timeStart = QtGui.QCalendarWidget()
            timeStart=QtGui.QDateTimeEdit()
            timeStart.setDateTime(QtCore.QDateTime.currentDateTime())
            timeStart.setDisplayFormat("yyyy-MM-dd hh:mm:ss")
            timeStart.setCalendarPopup(True)  
            lableTimeEnd = QtGui.QLabel(self.tr("Time end"))  
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
            
            
            self.dfSymbolsToDownload.loc[code,'name'] = name
            self.dfSymbolsToDownload.loc[code,'c_name'] = c_name
            
            self.updateSymbolsToDownloadTable()
    def slotAddAll(self):
        pass
    def slotDeleteOne(self):
        pass
    def slotDeleteAll(self):
        pass
    #----------------------------------------------------------------------
    def slotAddNewSymbol(self):
        """"""
        text = self.editSymbolToAdd.text()
        if(len(text)==0 and (not text.isnumeric())):
            symbol = 'none to download.'
            QtGui.QMessageBox.information(self,"Information",self.tr(symbol))   
        else:
            self.dfSymbolsToDownload.loc[text] = None
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
        rowSelected = self.tableLocalSymbols.currentRow()
        if((rowSelected<0) and (self.tableLocalSymbols.rowCount()>0)):
            rowSelected = 0
            
        if(rowSelected>=0):   #a row selected or table is not empty.
            symbolToDownload = self.tableLocalSymbols.item(rowSelected,0).text()
            # 1)connect to Mongodb 
            connect = Mongodb('192.168.0.212', 27017)
            connect.use('Tushare')    #database            
            # 2)retrive data from specified collection
            strStart = u'2013-12-01'
            dateEnd = dt.datetime.now()
            strEnd = dateEnd.strftime('%Y-%m-%d')  
            frequency = 'D'
            connect.setCollection(frequency)    #table
            history = connect.retrive(symbolToDownload,strStart,strEnd,frequency)
            dataForCandle = feedsForCandle.DataFrameToCandle(history)            
            
            self.myWindow = MyDialog(dataForCandle=dataForCandle)  
            self.myWindow.show()                        
        else:   #none selected and empty table
            symbol = 'none to download.'
            QtGui.QMessageBox.information(self,"Information",self.tr(symbol)) 

#----------------------------------------------------------------------
    def slotDownloadAll(self):
        """"""
        if(len(self.dfSymbolsToDownload)>0):
            symbol = self.dfSymbolsToDownload.index[0]
        else:
            symbol = 'none to download.'
        QtGui.QMessageBox.information(self,"Information",self.tr(symbol))
    #----------------------------------------------------------------------
    def slotDownloadOne(self):
        """"""
        rowSelected = self.tableSymbolsToDownload.currentRow()
        if((rowSelected<0) and (self.tableSymbolsToDownload.rowCount()>0)):
            rowSelected = 0
            
        if(rowSelected>=0):   #a row selected or table is not empty.
            symbolToDownload = self.tableSymbolsToDownload.item(rowSelected,0).text()
    
            # 2)download history data
            strStart = '2010-01-01'
            dateEnd = datetime.now()
            strEnd = dateEnd.strftime('%Y-%m-%d')  
            frequency = 'D'
        
            # 1)connect to Tushare data collection
            connect = Mongodb('192.168.1.100', 27017)
            connect.use('Tushare')    #database
            connect.setCollection(frequency)    #table
        
            countsDownloaded = connect.downloadAndStoreHistory(symbolToDownload,strStart,strEnd,frequency)            
            
            if(countsDownloaded<=0):
                QtGui.QMessageBox.information(self,"Information",self.tr('None downloaded.')) 
            else:
                QtGui.QMessageBox.information(self,"Information",self.tr(str(countsDownloaded)+' downloaded.')) 
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
