from PyQt4 import QtGui,QtCore
import numpy as np
import pandas as pd
from datetime import datetime
import datetime as dt
from DataSources.DataConverter import DataConverter
from DataSources.DataSourceMongodb import Mongodb
import matplotlib.dates as mpd
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

from Views.HistoryCandleView import HistoryCandleView
from Views.HistoryTableView import HistoryTableView
class DataManagerDialog(QtGui.QDialog):
    def __init__(self,parent=None):
        super(DataManagerDialog,self).__init__(parent)
        self.setWindowTitle(self.tr("DataManager"))
        self.initData()
        self.initUI()
    #---------------------------------------------------------------------
    def initData(self):
        """"""
        # 1)connect to Mongodb 
        connect = Mongodb('192.168.1.100', 27017)
        connect.use('Tushare')    #database
        frequency = 'D'
        connect.setCollection(frequency)    #table
        
        self.dfLocalSymbols = connect.retriveSymbolsAll()        
        #self.dfLocalSymbols = ts.get_stock_basics()
        self.dfSymbolsToDownload = pd.DataFrame(columns=['name','dateStart','dateEnd'])
    #----------------------------------------------------------------------
    def initUI(self):
        """"""
        mainLayout = QtGui.QVBoxLayout(self)
        topLayout = QtGui.QHBoxLayout(self)
        bottomLayout = QtGui.QHBoxLayout(self)
        topLeft01 = QtGui.QVBoxLayout(self)
        topLeft01Bottom = QtGui.QHBoxLayout(self)
        topLeft02 = QtGui.QVBoxLayout(self)
        topLeft03 = QtGui.QVBoxLayout(self)
        topLeft03Bottom = QtGui.QHBoxLayout(self)
        topLeft04 = QtGui.QVBoxLayout(self)      
        bottomLeft01 = QtGui.QVBoxLayout(self)  
        bottomLeft02 = QtGui.QVBoxLayout(self)  
        # 01)topLeft01------------------
        DeleteOneFromDBButton=QtGui.QPushButton(self.tr("DeleteOneFromDB"))
        DeleteAllFromDBButton=QtGui.QPushButton(self.tr("DeleteAllFromDB"))      
        ShowInTableButton=QtGui.QPushButton(self.tr("ShowInTable"))
        ShowInGraphButton=QtGui.QPushButton(self.tr("ShowInGraph"))           
        
        topLeft01Bottom.addWidget(DeleteOneFromDBButton)
        topLeft01Bottom.addWidget(DeleteAllFromDBButton)
        topLeft01Bottom.addWidget(ShowInTableButton)
        topLeft01Bottom.addWidget(ShowInGraphButton)
        
        labelLocalData=QtGui.QLabel(self.tr("LocalData:"))
        self.tableLocalSymbols=QtGui.QTableWidget()
        self.updateLocalSymbolsTable()   
        
        topLeft01.addWidget(labelLocalData)
        topLeft01.addWidget(self.tableLocalSymbols)
        topLeft01.addLayout(topLeft01Bottom)
        
        self.connect(ShowInTableButton,QtCore.SIGNAL("clicked()"),self.slotShowInTable)
        self.connect(ShowInGraphButton,QtCore.SIGNAL("clicked()"),self.slotShowInCandleGraph)
        # 02)topLeft02--------------------
        AddOneButton=QtGui.QPushButton(self.tr(">"))
        AddAllButton=QtGui.QPushButton(self.tr(">>>"))  
        DeleteOneButton=QtGui.QPushButton(self.tr("<"))
        DeleteAllButton=QtGui.QPushButton(self.tr("<<<"))  
        topLeft02.addWidget(AddOneButton)
        topLeft02.addWidget(AddAllButton)
        topLeft02.addWidget(DeleteOneButton)
        topLeft02.addWidget(DeleteAllButton)
        # 03topLeft03-------------------
        labelNewToDownload = QtGui.QLabel(self.tr('New Symbol:'))
        self.editSymbolToAdd = QtGui.QLineEdit()
        addNewSymbol = QtGui.QPushButton(self.tr('Add'))   
        topLeft03Bottom.addWidget(labelNewToDownload)
        topLeft03Bottom.addWidget(self.editSymbolToAdd)
        topLeft03Bottom.addWidget(addNewSymbol)   
        
        labelSymbolsToDownload=QtGui.QLabel(self.tr("SymbolsToDownload:"))
        self.tableSymbolsToDownload=QtGui.QTableWidget()
        self.updateSymbolsToDownloadTable()
        
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
        # top---------------------------------------------------------------------
        topLayout.addLayout(topLeft01)
        topLayout.addLayout(topLeft02)
        topLayout.addLayout(topLeft03)
        topLayout.addLayout(topLeft04)
        # bottom--------------------------------------------------------------------
        bottomLayout.addLayout(bottomLeft01)
        bottomLayout.addLayout(bottomLeft02)
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
        header = ["sybol","name","counts","start","end"]
        self.tableLocalSymbols.setColumnCount(len(header))
        self.tableLocalSymbols.setRowCount(len(self.dfLocalSymbols))
        self.tableLocalSymbols.setHorizontalHeaderLabels(header)     #mid should be after .setColumnCount()
        
        for row in np.arange(0,len(self.dfLocalSymbols)):
            code = self.dfLocalSymbols.index[row]
            symbol = QtGui.QLabel(self.tr(code))
            counts = str(self.dfLocalSymbols.loc[code,'counts'])
            dateStart = self.dfLocalSymbols.loc[code,'dateStart']
            dateEnd = self.dfLocalSymbols.loc[code,'dateEnd']
                               
            self.tableLocalSymbols.setItem(row,0,QtGui.QTableWidgetItem(code))
            self.tableLocalSymbols.setCellWidget(row,1,symbol)
            self.tableLocalSymbols.setItem(row,2,QtGui.QTableWidgetItem(counts))
            self.tableLocalSymbols.setItem(row,3,QtGui.QTableWidgetItem(dateStart))
            self.tableLocalSymbols.setItem(row,4,QtGui.QTableWidgetItem(dateEnd))
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
            self.tableSymbolsToDownload.setCellWidget(row,2,timeStart)
            self.tableSymbolsToDownload.setCellWidget(row,3,timeEnd)    
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
        self.tableHistory=HistoryTableView()
        self.tableHistory.setWindowTitle("history")
        self.tableHistory.show()        
    def slotShowInCandleGraph(self):
        rowSelected = self.tableLocalSymbols.currentRow()
        if((rowSelected<0) and (self.tableLocalSymbols.rowCount()>0)):
            rowSelected = 0
            
        if(rowSelected>=0):   #a row selected or table is not empty.
            symbolToDownload = self.tableLocalSymbols.item(rowSelected,0).text()
            dataConverter = DataConverter()
            # 1)connect to Mongodb 
            connect = Mongodb('192.168.1.100', 27017)
            connect.use('Tushare')    #database            
            # 2)retrive data from specified collection
            strStart = '2013-12-01'
            dateEnd = dt.datetime.now()
            strEnd = dateEnd.strftime('%Y-%m-%d')  
            frequency = 'D'
            connect.setCollection(frequency)    #table
            history = connect.retrive(symbolToDownload,strStart,strEnd,frequency)
            dataForCandle = dataConverter.DataFrameToCandle(history)            
            
            self.myWindow = MyDialog(dataForCandle=dataForCandle)  
            self.myWindow.show()                        
        else:   #none selected and empty table
            symbol = 'none to download.'
            QtGui.QMessageBox.information(self,"Information",self.tr(symbol)) 
    '''
    #----------------------------------------------------------------------
    def slotShowInCandleGraphBak(self):
        """
        单独窗口嵌入matplotlib图形,未使用，作为有用算法留存
        """
        rowSelected = self.tableLocalSymbols.currentRow()
        if((rowSelected<0) and (self.tableLocalSymbols.rowCount()>0)):
            rowSelected = 0
            
        if(rowSelected>=0):   #a row selected or table is not empty.
            symbolToDownload = self.tableLocalSymbols.item(rowSelected,0).text()
            dataConverter = DataConverter()
            # 1)connect to Mongodb 
            connect = Mongodb('192.168.1.100', 27017)
            connect.use('Tushare')    #database            
            # 2)retrive data from specified collection
            strStart = '2013-12-01'
            dateEnd = dt.datetime.now()
            strEnd = dateEnd.strftime('%Y-%m-%d')  
            frequency = 'D'
            connect.setCollection(frequency)    #table
            history = connect.retrive(symbolToDownload,strStart,strEnd,frequency)
            dataForCandle = dataConverter.DataFrameToCandle(history)            
            
            mainLayout = QtGui.QHBoxLayout(self)
            
            self.historyView = QtGui.QMainWindow()
            self.historyView.setWindowTitle(self.tr(symbolToDownload))
            canvas = HistoryCandleView(dataForCandle=dataForCandle, width=5, height=4, dpi=100)
            self.historyView.setCentralWidget(canvas)

            self.historyView.show()                       
        else:   #none selected and empty table
            symbol = 'none to download.'
            QtGui.QMessageBox.information(self,"Information",self.tr(symbol))                   
    '''
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
        #fig.subplots_adjust(top=0.98,bottom=0.05,left=0.15,right=0.99,hspace =0.1,wspace = 0.1) 
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
        button01 = QtGui.QPushButton('OK01')   
        button02 = QtGui.QPushButton('OK02')
        layoutLeft.addWidget(button01)
        layoutLeft.addWidget(button02)        
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
'''
class MyDialogBackupOnly(QtGui.QDialog):   # mid not used
    def __init__(self,dataForCandle=None, parent=None):  
        super(MyDialog, self).__init__(parent)  
        # 1) set mainlayout
        layout = QtGui.QHBoxLayout()  
        self.setLayout(layout)     
        # 2) creates layoutLeft and add it to mainlayout
        layoutLeft = QtGui.QVBoxLayout()  
        layout.addLayout(layoutLeft)  
        # 3) add table to mainlayout
        self.MyTable = QtGui.QTableWidget(4,3)  
        self.MyTable.setHorizontalHeaderLabels(['姓名','身高','体重'])  
        newItem = QtGui.QTableWidgetItem("松鼠")  
        newItem = QtGui.QTableWidgetItem("10cm")          
        newItem = QtGui.QTableWidgetItem("60g")     
        self.MyTable.setItem(0, 0, newItem)  
        self.MyTable.setItem(0, 1, newItem) 
        self.MyTable.setItem(0, 2, newItem)
        layout.addWidget(self.MyTable)   
        # 4) add button to layoutLeft
        button01 = QtGui.QPushButton('OK01')   
        button02 = QtGui.QPushButton('OK02')
        layoutLeft.addWidget(button01)
        layoutLeft.addWidget(button02)        
        # 5) add candleView to mainlayout
        canvas = HistoryCandleView(dataForCandle=dataForCandle)        
        layout.addWidget(canvas)
        # 6) connect
        self.connect(button01,QtCore.SIGNAL("clicked()"),self.slotOK01)
        self.connect(button02,QtCore.SIGNAL("clicked()"),self.slotOK02)
    #----------------------------------------------------------------------
    def slotOK01(self):
        """"""
        self.mainWindow=QtGui.QMainWindow()
        self.mainWindow.setWindowTitle(self.tr("GraphView"))
    
        graphView = QtGui.QWidget(self.mainWindow)
        layout = QtGui.QVBoxLayout(graphView)
        
        
        
        
        

        symbolToDownload = '000001'
        dataConverter = DataConverter()
        # 1)connect to Mongodb 
        connect = Mongodb('192.168.1.100', 27017)
        connect.use('Tushare')    #database            
        # 2)retrive data from specified collection
        strStart = '2015-12-01'
        dateEnd = dt.datetime.now()
        strEnd = dateEnd.strftime('%Y-%m-%d')  
        frequency = 'D'
        connect.setCollection(frequency)    #table
        history = connect.retrive(symbolToDownload,strStart,strEnd,frequency)
        dataForCandle = dataConverter.DataFrameToCandle(history)                    
        graph = HistoryCandleView(dataForCandle=dataForCandle)
        
        
        
        
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
        
        plt.show()
'''