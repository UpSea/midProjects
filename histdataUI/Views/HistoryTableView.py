# -*- coding: utf-8 -*-
from PyQt4 import QtGui,QtCore
import datetime as dt
import os,sys
xpower = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,os.pardir,'histdata','mongodb'))
sys.path.append(xpower)
from data.mongodb.DataSourceMongodb import Mongodb
import numpy as np

class HistoryTableView(QtGui.QTableWidget):
    def __init__(self,rawData=None,parent=None):
        super(HistoryTableView,self).__init__(parent)
        
        self.dfLocalSymbols = rawData       
        
        self.showTable()
    #----------------------------------------------------------------------
    def showTable(self):
        """"""
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)  
        self.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)  
        self.setSelectionBehavior(QtGui.QTableWidget.SelectRows)  
        self.setSelectionMode(QtGui.QTableWidget.SingleSelection)  
        self.setAlternatingRowColors(True)         
        
        
        self.clear()
        header = ['datetime','open','high','low','close']
        self.setColumnCount(len(header))
        self.setRowCount(len(self.dfLocalSymbols))
        self.setHorizontalHeaderLabels(header)     #mid should be after .setColumnCount()
        
        for row in np.arange(0,len(self.dfLocalSymbols)):
            datetime = self.dfLocalSymbols.index[row]
            openPrice = str(self.dfLocalSymbols.loc[datetime,'open'])
            highPrice = str(self.dfLocalSymbols.loc[datetime,'high'])
            lowPrice = str(self.dfLocalSymbols.loc[datetime,'low'])
            closePrice = str(self.dfLocalSymbols.loc[datetime,'close'])
            
            self.setItem(row,0,QtGui.QTableWidgetItem(datetime))
            self.setCellWidget(row,1,QtGui.QLabel(self.tr(openPrice)))
            self.setItem(row,2,QtGui.QTableWidgetItem(highPrice))
            self.setItem(row,3,QtGui.QTableWidgetItem(lowPrice))
            self.setItem(row,4,QtGui.QTableWidgetItem(closePrice))                            
            
            
if __name__ == '__main__':
    import os,sys        
    app = QtGui.QApplication([])
    
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
    tableHistory=HistoryTableView(rawData=data)
    tableHistory.setWindowTitle("history")
    tableHistory.showMaximized()  
    
    sys.exit(app.exec_())            
            
            
            