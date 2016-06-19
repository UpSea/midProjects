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

ReqTypeCode = 0x11
reqHeader = struct.pack('B',ReqTypeCode)
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

sizeOfRspCodeHeader = 64*2 + 4
rspCodeHeader = s.recv(sizeOfRspCodeHeader)
broker,account,nRspCount = struct.unpack('64s64si',rspCodeHeader)

sizeOfRspCode = 64*2+4
rspCodes = s.recv(sizeOfRspCode * nRspCount)

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

for i,code in enumerate(codes):
    print i,'----',code

s.close()   #关闭连接




