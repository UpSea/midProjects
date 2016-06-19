# -*- coding: utf-8 -*-
import socket
import struct
import sys
HOST='192.168.0.212'
PORT=5050

#建立socket对象  定义socket类型，网络通信，TCP
try:  
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
except socket.error, e:  
    print 'Strange error creating socket:%s' % e  
    sys.exit(1)  

#mid 创建连接  connect()连接成功后才返回，否则阻塞，无返回值
try:  
    s.connect((HOST,PORT))
except socket.gaierror, e:  
    print 'Address-related error connecting to server :%s' % e  
    sys.exit(1)  
except socket.error, e:  
    print 'Connection error:%s' % e  
    sys.exit(1)  

# 显示本机的IP地址和端口号  
print 'Connected from', s.getsockname()  
# 显示远端服务器的IP地址和端口号  
print 'Connected to ', s.getpeername()  

ReqTypeHistory = 0x01	    #mid 查询历史价格数据
reqHeader = struct.pack('B',ReqTypeHistory)
try:
    s.send(reqHeader)
except socket.error, e:  
    print 'Error sending data:%s' % e  
    sys.exit(1)  
def getBuffer(strIn):
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
broker = getBuffer('fxcm')
account = getBuffer('158992')
password = getBuffer('1233654')
symbol = getBuffer('XAUUSD')

nCount = struct.pack('i',300)
HistoryPeriodD1 = 0x09
ktype = struct.pack('i',HistoryPeriodD1)

login = broker+account+password
reqHistory = login + symbol + nCount + ktype

try:
    s.send(reqHistory)
except socket.error, e:  
    print 'Error sending data:%s' % e  
    sys.exit(1)  



sizeOfRspHistoryHeader = 64*1 + 4 + 4
rspHistoryHeader = s.recv(sizeOfRspHistoryHeader)
symbol,nRspCount,ktype = struct.unpack('64sii',rspHistoryHeader)

#mid 数据传输时按C语言定义的字节流传输
#mid int=4，double=8，long long =8
sizeOfMqlDateTime = 8 * 4
sizeOfRspHistory = sizeOfMqlDateTime + 4 * 8 + 8 + 8


def recvAll(s,size):
    #mid recv的数量超过一定数量之后，总会一次接收不完，所以需要如此循环接收并组装返回
    #mid 如此，原则上s.recv()不应再使用，都需用recvAll代替
    toRecv = totalToRecv= size
    totalReceived = 0
    received = ''
    data = ''
    while 1:
        s.settimeout(10)
        received = s.recv(toRecv)
        toRecv = toRecv - len(received)
        data += received    
        totalReceived = len(data)
        if totalReceived == totalToRecv:
            break
    return data

rspHistories = recvAll(s, sizeOfRspHistory * nRspCount)

histories = []
for i in range(nRspCount):
    start = i * sizeOfRspHistory
    end = (i + 1) * sizeOfRspHistory
    history = rspHistories[start:end]
    year,mon,day,hour,min,sec,day_of_week,day_of_year,dOpen,dHigh,dLow,dClose,dVolume,dAmount = struct.unpack('8i4dqd',history)
    
    kdata = [year,mon,day,hour,min,sec,day_of_week,day_of_year,dOpen,dHigh,dLow,dClose,dVolume,dAmount]
    histories.append(kdata)

for i,code in enumerate(histories):
    print i,'----',code

s.close()   #关闭连接




