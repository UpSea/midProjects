import pandas as pd
import numpy as np
import matplotlib.dates as mpd
import datetime as dt
'''
一个日期文本转换为TimStamp之后，默认是没有时区信息的
没有时区信息的timestamp转化为num之后，其值与将其设置为utc之后的num值是一样的，从#2看出

timestamp一旦设置为某个时区之后，其num值便固定。时区只是作为当地时间的调整出现。

2015-12-21 09:30:00
设置为Asia/Shanghai,之后，表示为2015-12-21 09:30:00+08:00
将上海时间转化为东京时间，之后，表示为2015-12-21 10:30:00+09:00
将上海时间转化为utc时间，之后，表示为2015-12-21 01:30:00+00:00

以上转化的意义是，上海当地时间9:30时，东京当地时间为10:30
上海当地时间9:30时，utc标准时间为01:30，utc标准时间为巴黎时间。
'''
# 1
history = ['2015-12-21 09:30:00'] 
history = ['2015-12-21'+' 09:30:00']
date = dt.datetime.strptime(history[0], '%Y-%m-%d %H:%M:%S')
dateNum = mpd.date2num(date)
print(type(date))
print(date)
print(dateNum)

date = pd.to_datetime(history[0], '%Y-%m-%d %H:%M:%S')
dateNum = mpd.date2num(date)
print('-----time with none timezone,')
print(type(date))
print(date)
print(dateNum)
date = date.tz_localize('Asia/Shanghai')
dateNum = mpd.date2num(date)
print('-----set time zone to shanghai')
print(type(date))
print(date)
print(dateNum)
date = date.tz_convert('utc')
dateNum = mpd.date2num(date)
print('-----time utc')
print(type(date))
print(date)
print(dateNum)
date = date.tz_convert('Asia/Tokyo')
dateNum = mpd.date2num(date)
print('----time us/eastern')
print(type(date))
print(date)
print(dateNum)
date = date.tz_convert('US/Eastern')
dateNum = mpd.date2num(date)
print('----time us/eastern')
print(type(date))
print(date)
print(dateNum)


# 2
import pandas as pd
import numpy as np
import matplotlib.dates as mpd
import datetime as dt

history = ['2015-12-21 09:30:00'] 

date = dt.datetime.strptime(history[0], '%Y-%m-%d %H:%M:%S')
dateNum = mpd.date2num(date)
print(type(date))
print(date)
print(dateNum)

date = pd.to_datetime(history[0], '%Y-%m-%d %H:%M:%S')
dateNum = mpd.date2num(date)
print('-----time with none timezone,')
print(type(date))
print(date)
print(dateNum)


date = pd.to_datetime(history[0], '%Y-%m-%d %H:%M:%S')
date = date.tz_localize('utc')
dateNum = mpd.date2num(date)
print('-----set time zone to utc')
print(type(date))
print(date)
print(dateNum)