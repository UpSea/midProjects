mid pandas.Timestamp is a subclass of datetime.datetime
a = historyDf.index[0]
b = historyDf.index[5]
historyDf[a:b]
    open  high  close   low      volume       amount
date                                                                       
2016-05-30 00:00:00+00:00  4.67  4.71   4.69  4.66  56734323.0  269110193.0
2016-05-27 00:00:00+00:00  4.68  4.69   4.68  4.65  35837639.0  169548212.0
2016-05-26 00:00:00+00:00  4.65  4.71   4.69  4.65  58177990.0  276166625.0
2016-05-25 00:00:00+00:00  4.62  4.66   4.65  4.62  61234533.0  288046549.0
2016-05-24 00:00:00+00:00  4.62  4.63   4.62  4.55  48986406.0  227405304.0
2016-05-23 00:00:00+00:00  4.63  4.66   4.64  4.61  37043194.0  173623800.0
import datetime
c = datetime.datetime(2016,5,30)
d = datetime.datetime(2016,5,23)
a,b,c,d
(Timestamp('2016-05-30 00:00:00+0000', tz='UTC'), Timestamp('2016-05-23 00:00:00+0000', tz='UTC'), datetime.datetime(2016, 5, 30, 0, 0), datetime.datetime(2016, 5, 23, 0, 0))
c = pd.Timestamp(d)
c
Timestamp('2016-05-23 00:00:00')
d = pd.Timestamp(c)
c,d
(Timestamp('2016-05-23 00:00:00'), Timestamp('2016-05-23 00:00:00'))
c = pd.Timestamp(datetime.datetime(2016,5,30))
d = pd.Timestamp(datetime.datetime(2016,5,23))
c,d
(Timestamp('2016-05-30 00:00:00'), Timestamp('2016-05-23 00:00:00'))
a,b
(Timestamp('2016-05-30 00:00:00+0000', tz='UTC'), Timestamp('2016-05-23 00:00:00+0000', tz='UTC'))
historyDf[c:d]
    open  high  close   low      volume       amount
date                                                                       
2016-05-30 00:00:00+00:00  4.67  4.71   4.69  4.66  56734323.0  269110193.0
2016-05-27 00:00:00+00:00  4.68  4.69   4.68  4.65  35837639.0  169548212.0
2016-05-26 00:00:00+00:00  4.65  4.71   4.69  4.65  58177990.0  276166625.0
2016-05-25 00:00:00+00:00  4.62  4.66   4.65  4.62  61234533.0  288046549.0
2016-05-24 00:00:00+00:00  4.62  4.63   4.62  4.55  48986406.0  227405304.0
2016-05-23 00:00:00+00:00  4.63  4.66   4.64  4.61  37043194.0  173623800.0
historyDf[a:b]
    open  high  close   low      volume       amount
date                                                                       
2016-05-30 00:00:00+00:00  4.67  4.71   4.69  4.66  56734323.0  269110193.0
2016-05-27 00:00:00+00:00  4.68  4.69   4.68  4.65  35837639.0  169548212.0
2016-05-26 00:00:00+00:00  4.65  4.71   4.69  4.65  58177990.0  276166625.0
2016-05-25 00:00:00+00:00  4.62  4.66   4.65  4.62  61234533.0  288046549.0
2016-05-24 00:00:00+00:00  4.62  4.63   4.62  4.55  48986406.0  227405304.0
2016-05-23 00:00:00+00:00  4.63  4.66   4.64  4.61  37043194.0  173623800.0
d = pd.Timestamp(datetime.datetime(2016,5,25))
historyDf[c:d]
    open  high  close   low      volume       amount
date                                                                       
2016-05-30 00:00:00+00:00  4.67  4.71   4.69  4.66  56734323.0  269110193.0
2016-05-27 00:00:00+00:00  4.68  4.69   4.68  4.65  35837639.0  169548212.0
2016-05-26 00:00:00+00:00  4.65  4.71   4.69  4.65  58177990.0  276166625.0
2016-05-25 00:00:00+00:00  4.62  4.66   4.65  4.62  61234533.0  288046549.0
