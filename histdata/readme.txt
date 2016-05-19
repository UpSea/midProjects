这个文件夹是数据中心，各文件夹功能说明如下：
/data
	各种数据源历史数据的本地磁盘文件储存
	按存储形式划分：
	1.csv	
		1.1.tushare
		1.2.yahoo
		1.3.sina
		1.4....
	2.mongodb
		采用类是csv的方式，对不同来源的数据进行分库储存
	3.h5ds
	4....
	此处csv代表的是实际的文件，而mongodb只是代表了一种对文件的储存途经

/tusharedb
	集中处理tushare数据的程序，直接处理/data下各种数据及网络数据
	1.网络数据获取
	2.csv数据读写
	3.mongodb数据读写
/yahoodb
/sinadb
以上两个数据源功能同tusharedb

dataCenter.py
	此文件集中对不同数据源的数据进行操作，调用.tusharedb;.yahoodb;.sinadb
dataManagerUI.py
	对历史数据进行管理和展示的程序，调用dataCenter.py

feedsForPAT.py
    此文件通过调用dataCenter.py集中处理各种数据源，并为PyAlgoTrade集中提供feeds

feedsForZipline.py
    此文件通过调用dataCenter.py集中处理各种数据源，并为Zipline集中提供feeds

这样，数据使用的逻辑关系就构建清楚

dataCenterUI,PAT,zipline,vnpy....	(数据消费者)
	dataCenter			(数据调度中心)
tusharedb,yahoodb,sinadb		(数据源类型划分)
csv,mongodb,hdf5....			(数据物理储存格式)







