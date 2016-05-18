Views文件夹下的文件涉及matplotlib嵌入qt窗体，在py3下可以，在py2下有些问题

Widgets文件夹下的不涉及以上嵌入问题，在py3和py2下都能运行。


DataManager.py是原先实验性质的在py3下编写的数据管理界面，图形化用了Views下面的东西，而且功能也不完善
计划这个文件原样保留，作为示例程序存在，另外再写一个主要使用Widgets下文件的管理界面

DataCenterUI.py
1.下载多个网络数据源数据到本地
	1.yahoo
	2.tushare
	3.sina
	4.datayes
	5....
2.保存数据至本地不同的数据库
	1.csv
	2.mongodb
	3....
3.检索本地不同数据源的数据并显示
	1.table方式
	2.Candle方式
