datetime的格式是：
datetime.datetime(2014, 1, 5, 16, 47, 49)

>>> import time
>>> import datetime

string转换为datetime：
>>> string = '2014-01-08 11:59:58'
>>> time1 = datetime.datetime.strptime(string,'%Y-%m-%d %H:%M:%S')
>>> print time1
2014-01-08 11:59:58

时间的加减：
>>> last = time1 - datetime.timedelta(hours = 24)
>>> next_dat = time1 + datetime.timedelta(hours = 24)
>>> print last
2014-01-07 11:59:58
>>> next_dat
datetime.datetime(2014, 1, 9, 11, 59, 58)
>>> print next_dat
2014-01-09 11:59:58
>>> str(last)
'2014-01-07 11:59:58'

datetime转为字符串：
>>> time1_str = datetime.datetime.strftime(time1,'%Y-%m-%d %H:%M:%S')
>>> time1_str
'2014-01-08 11:59:58'

python获取当前时间：
time.time() 获取当前时间戳
time.localtime() 当前时间的struct_time形式
time.ctime() 当前时间的字符串形式
>>> time.time()
1389243184.696
>>> time.localtime()
time.struct_time(tm_year=2014, tm_mon=1, tm_mday=9, tm_hour=12, tm_min=53, tm_sec=13, tm_wday=3, tm_yday=9, tm_isdst=0)
>>> time.ctime()
'Thu Jan 09 12:53:19 2014'

struct_time转换为字符串：
>>> time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
'2014-01-09 12:59:00'
>>> time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())
'Thu Jan 09 13:01:00 2014'

将格式字符串转换为时间戳：
>>> a = "Sat Mar 28 22:24:24 2009"
>>> b = time.mktime(time.strptime(a,"%a %b %d %H:%M:%S %Y"))
>>> b
1238250264.0

datetime转化为时间戳：
>>> time.mktime(datetime.datetime(2014,1,8,11,59,58).timetuple())
1389153598.0

详见：
http://www.2cto.com/kf/201109/102535.html




Python中关于时间和日期函数有time和datatime


1.获取当前时间的两种方法：

import datetime,time

now = time.strftime("%Y-%m-%d %H:%M:%S")

print now

now = datetime.datetime.now()

print now



2.获取上个月最后一天的日期(本月的第一天减去1天)

last = datetime.date(datetime.date.today().year,datetime.date.today().month,1)-datetime.timedelta(1)

print last



3.获取时间差(时间差单位为秒，常用于计算程序运行的时间)

starttime = datetime.datetime.now()

#long running

endtime = datetime.datetime.now()

print (endtime - starttime).seconds



4.计算当前时间向后10个小时的时间



d1 = datetime.datetime.now()

d3 = d1 + datetime.timedelta(hours=10)

d3.ctime()



其本上常用的类有：datetime和timedelta两个。它们之间可以相互加减。每个类都有一些方法和属性可以查看具体的值，如 datetime可以查看：天数(day)，小时数(hour)，星期几(weekday())等;timedelta可以查看：天数(days)，秒数 (seconds)等。





5.python中时间日期格式化符号：



%y 两位数的年份表示（00-99）

%Y 四位数的年份表示（000-9999）

%m 月份（01-12）

%d 月内中的一天（0-31）

%H 24小时制小时数（0-23）

%I 12小时制小时数（01-12） 

%M 分钟数（00=59）

%S 秒（00-59）



%a 本地简化星期名称

%A 本地完整星期名称

%b 本地简化的月份名称

%B 本地完整的月份名称

%c 本地相应的日期表示和时间表示

%j 年内的一天（001-366）

%p 本地A.M.或P.M.的等价符

%U 一年中的星期数（00-53）星期天为星期的开始

%w 星期（0-6），星期天为星期的开始

%W 一年中的星期数（00-53）星期一为星期的开始

%x 本地相应的日期表示

%X 本地相应的时间表示

%Z 当前时区的名称

%% %号本身linux