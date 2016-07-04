import time as time
import datetime as dt

dateEnd = dt.datetime.now()
strEnd = dateEnd.strftime('%Y-%m-%d %H:%M:%S') 

print('now:'+strEnd)
'''mid
以下程序将一个确定期间字符串日期等分为若干段，之后分段输出字符串
'''
timeFrom = '2016-05-20 00:00:00'
timeTo = '2016-05-30 00:00:00'
phases = 3
print timeFrom,timeTo

#mid 1)str to pyTimeStamp
timeStampFrom = int(time.mktime(time.strptime(timeFrom, "%Y-%m-%d %H:%M:%S")))
timeStampTo   = int(time.mktime(time.strptime(timeTo, "%Y-%m-%d %H:%M:%S")))    

#mid 2)str to datetime
timeFrom = dt.datetime.strptime(timeFrom,'%Y-%m-%d %H:%M:%S')    
timeTo = dt.datetime.strptime(timeTo,'%Y-%m-%d %H:%M:%S')   

interval = (timeStampTo - timeStampFrom)/phases
startTimeStamp = timeStampFrom
for index in range(phases):
    endTimeStamp = startTimeStamp + interval
    
    #mid 3)pyTimeStamp to datetime
    timeFromDatetime = dt.datetime.utcfromtimestamp(startTimeStamp)
    timeToDatetime = dt.datetime.utcfromtimestamp(endTimeStamp)
    
    #mid 4)datetime to str
    strTimeFrom = timeFromDatetime.strftime("%Y-%m-%d %H:%M:%S")
    strTimeTo = timeToDatetime.strftime("%Y-%m-%d %H:%M:%S")
    print '------',strTimeFrom,strTimeTo
    startTimeStamp = endTimeStamp
    