# -*- coding: utf-8 -*-
这个文件夹是数据中心，包括以下功能：
1.储存所有历史数据到对应的数据源目录
2.对历史数据存取相关的程序

tusharedb\
    此目录储存来自tushare的数据，在本地一csv储存
yahoodb
    储存来自yahoo的数据
mongodb
    不储存数据，集中保存对mongodb数据库操作的相关程序


feedsForPAT.py
    此文件集中处理各种数据源，并为PyAlgoTrade集中提供feeds

feedsForZipline.py
    此文件集中处理各种数据源，并为Zipline集中提供feeds