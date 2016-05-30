# -*- coding: utf-8 -*-
from PyQt4 import QtGui,QtCore
import datetime as dt
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
        
        if(True):
            dfLocalSymbols = self.dfLocalSymbols
            for row in range(len(dfLocalSymbols.index)):
                for column in range(len(dfLocalSymbols.columns)):
                    self.setItem(row,column,QtGui.QTableWidgetItem(str(dfLocalSymbols.iget_value(row, column))))             
        else:       
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
    
    def getRawDataDataCenter():
        import os,sys
        dataRoot = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,os.pardir,'histdata'))        
        sys.path.append(dataRoot)        
        import dataCenter as dataCenter          
        dataSource={}        
        dataSource['dataProvider'] = 'tushare'
        dataSource['storageFormat']='mongodb'
        dataSource['dataPeriod']='D'
        dataSource['symbol']='600028'
        dataSource['dateStart']='2015-03-19'
        dataSource['dateEnd']='2015-12-31'  
        dataSource['alone'] = True
        dataSource['overlay'] = False            
        
        dataCenter = dataCenter.dataCenter()
        
        data = dataCenter.retriveHistData(params = dataSource)   
        
        return data
        
    data = getRawDataDataCenter()
    tableHistory=HistoryTableView(rawData=data)
    tableHistory.setWindowTitle("history")
    tableHistory.showMaximized()  
    
    sys.exit(app.exec_())            
            
            
            