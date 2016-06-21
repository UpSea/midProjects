# -*- coding: utf-8 -*-

import socket
import struct
import sys,os
import pandas as pd  

class remoteStorage():
    def __init__(self,HOST,PORT):
        self.HOST = HOST
        self.PORT = PORT
    def connectSocket(self):
        try:  
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        except socket.error, e:  
            print 'Strange error creating socket:%s' % e  
            sys.exit(1)  
        #mid 创建连接  connect()连接成功后才返回，否则阻塞，无返回值
        try:  
            self.s.connect((self.HOST,self.PORT))
        except socket.gaierror, e:  
            print 'Address-related error connecting to server :%s' % e  
            sys.exit(1)  
        except socket.error, e:  
            print 'Connection error:%s' % e  
            sys.exit(1)    
            
        # 显示本机的IP地址和端口号  
        print 'Connected from', self.s.getsockname()  
        # 显示远端服务器的IP地址和端口号  
        print 'Connected to ', self.s.getpeername()         
    def closeSocket(self):
        self.s.close()   #关闭连接      
    def __getBuffer(self,strIn):
        #mid 通过socket发送数据给mt5时，采用的是字节流方式，而且原先定义解析的是长为64的char*类型的字串，
        #mid 所以此处需要装配 
        listBuffer = 64*[0]
        for i, ch in enumerate(strIn):
            listBuffer[i] = ch
        
        strBuffer = ''
        for i,ch in enumerate(listBuffer):
            if type(ch) is str:
                strBuffer = strBuffer + struct.pack('c',ch)
            elif type(ch) is int:
                strBuffer = strBuffer + struct.pack('B',0)
        return strBuffer
    def __recvAll(self,size):
        #mid recv的数量超过一定数量之后，总会一次接收不完，所以需要如此循环接收并组装返回
        #mid 如此，原则上s.recv()不应再使用，都需用recvAll代替
        toRecv = totalToRecv= size
        totalReceived = 0
        received = ''
        data = ''
        while 1:
            self.s.settimeout(1)
            try:
                received = self.s.recv(toRecv)
            except socket.error,e:
                print 'Error receiving data:%s' % e
                break
            toRecv = toRecv - len(received)
            data += received    
            totalReceived = len(data)
            if totalReceived == totalToRecv:
                break
        return data 
    def downloadCodes(self):
        self.connectSocket()
        ReqTypeCode = 0x11
        reqHeader = struct.pack('B',ReqTypeCode)
        try:
            self.s.send(reqHeader)
        except socket.error, e:  
            print 'Error sending data:%s' % e  
            sys.exit(1)        
        sizeOfRspCodeHeader = 64*2 + 4
        rspCodeHeader = self.__recvAll(sizeOfRspCodeHeader)
        broker,account,nRspCount = struct.unpack('64s64si',rspCodeHeader)
        
        sizeOfRspCode = 64*2+4
        rspCodes = self.__recvAll(sizeOfRspCode * nRspCount)
        #mid 在同一个进程中，多次访问socket，由于mt5server是单连接的所以，每一次都需要获得数据后主动断开连接关闭连接   
        self.closeSocket()      
        
        null = struct.pack('B',0)
        
        codes = []
        for i in range(nRspCount):
            start = i * sizeOfRspCode
            end = (i + 1) * sizeOfRspCode
            code = rspCodes[start:end]
            szCode,szName,iDigits = struct.unpack('64s64si',code)
            szCode = szCode[0:szCode.find(null)]
            szName = szName[0:szName.find(null)]
            
            codes.append([szCode,szName,iDigits])
            
        import pandas as pd  
        df = pd.DataFrame(codes,columns=['symbol', 'name','digits'])       
        df = pd.DataFrame(codes,columns=['symbol', 'name','digits'],index=df['symbol'])       
        df.index.name='symbol'
        return df

    def downloadKData(self,symbol = "",periodType = 0x09,timeStart ="",timeEnd = ""):
        self.connectSocket()
        
        ReqTypeHistory = 0x01	    #mid 查询历史价格数据
        reqHeader = struct.pack('B',ReqTypeHistory)
        try:
            self.s.send(reqHeader)
        except socket.error, e:  
            print 'Error sending data:%s' % e  
            sys.exit(1)  

        broker = self.__getBuffer('fxcm')
        account = self.__getBuffer('158992')
        password = self.__getBuffer('1233654')
        symbol = self.__getBuffer(symbol)
        
        nCount = struct.pack('i',300)
        ktype = struct.pack('i',periodType)
        
        login = broker+account+password
        reqHistory = login + symbol + nCount + ktype
        
        try:
            self.s.send(reqHistory)
        except socket.error, e:  
            print 'Error sending data:%s' % e  
            sys.exit(1)  

        sizeOfRspHistoryHeader = 64*1 + 4 + 4
        rspHistoryHeader = self.__recvAll(sizeOfRspHistoryHeader)
        if (len(rspHistoryHeader)<sizeOfRspHistoryHeader):
            return pd.DataFrame()
        symbol,nRspCount,ktype = struct.unpack('64sii',rspHistoryHeader)
        
        #mid 数据传输时按C语言定义的字节流传输
        #mid int=4，double=8，long long =8
        sizeOfMqlDateTime = 8 * 4
        sizeOfRspHistory = sizeOfMqlDateTime + 4 * 8 + 8 + 8

        rspHistories = self.__recvAll(sizeOfRspHistory * nRspCount)
        
        #mid 在同一个进程中，多次访问socket，由于mt5server是单连接的所以，每一次都需要获得数据后主动断开连接关闭连接   
        self.closeSocket()      
        
        histories = []
        for i in range(nRspCount):
            start = i * sizeOfRspHistory
            end = (i + 1) * sizeOfRspHistory
            history = rspHistories[start:end]
            year,mon,day,hour,min,sec,day_of_week,day_of_year,dOpen,dHigh,dLow,dClose,dVolume,dAmount = struct.unpack('8i4dqd',history)
            
            dateTime = "%d-%02d-%02d %02d:%02d:%02d" % (year,mon,day,hour,min,sec)
            
            kdata = [dateTime,dOpen,dHigh,dLow,dClose]
            histories.append(kdata)   
            
        df = pd.DataFrame(histories,columns=['datetime','open','high','low','close'])   
        df = pd.DataFrame(histories,columns=['datetime','open','high','low','close'],index=df['datetime'])       
        return df        
         
if __name__ == "__main__":
    dataRoot = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir))        
    sys.path.append(dataRoot)  
    
    dataPath = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,'data','csv','mt5db'))                    
    mt5Center = remoteStorage('192.168.0.212',5050)   
    
    if(True):
        data = mt5Center.downloadKData('XAUUSD')
        
        
        if(data is not None):
            quotesDict = data.to_dict()           
        
        
        for i,code in enumerate(data.values):
            print i,'----',code
    if(True):
        dfCodes = mt5Center.downloadCodes()
        for code in dfCodes.values:
            print '----',code                  