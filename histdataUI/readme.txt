Views文件夹下的文件涉及matplotlib嵌入qt窗体，在py3下可以，在py2下有些问题

Widgets文件夹下的不涉及以上嵌入问题，在py3和py2下都能运行。

Layouts文件夹下的文件为一些基本的layout组件

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

DataCenterUI为数据管理程序的界面
当前有三个版本

最新的版本号大

1.0版本使用了新加入独立的Loyouts，使程序界面更容易自定义