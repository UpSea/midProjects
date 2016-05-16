这个文件夹是数据中心，各文件夹功能说明如下：
/data
	各种数据源历史数据的本地磁盘文件储存
	一级按来源划分：yahoo，tushare，sina
	二级按格式划分：csv，其他
/mongodb
	处理mongodb的程序
/tusharedb
	处理tushare数据的程序

dataManagerUI.py
	对历史数据进行管理和展示的程序

feedsForPAT.py
    此文件集中处理各种数据源，并为PyAlgoTrade集中提供feeds

feedsForZipline.py
    此文件集中处理各种数据源，并为Zipline集中提供feeds