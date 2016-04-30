# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 09:16:54 2015

@author: mid
"""
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 16:07:25 2015

@author: Administrator
综合操作

"""

#!/usr/bin/env python
import tushare as ts

tsquotes_all = ts.get_hist_data('000001', '2015-01-01', '2015-09-22',
                                'D')  # 一次性获取全部日k线数据
                                
# 显示(某列-某行)的元素，行序号也是字符串，以下两语句分别使用俩种方式访问
print(tsquotes_all['open']['2015-01-05'])
print(tsquotes_all['open'][0])

# %% 绘制收盘价格和某个均线的累积图，列筛选访问
tsquotes_all[['close', 'ma20']].cumsum().plot()
# %% 绘制筛选列的所有行
tsquotes_all[[1, 3]].plot()  # 按列号选择
tsquotes_all[['close', 'ma20']].plot()  # 按列名选择
# %% 绘制筛选列的某些行
tsquotes_all[['close', 'ma20']][1:30].plot()
# %% [column][row]
"""
    mid 201509221016
    
    follows are right 
        cos 1:5,[1,2,5] return a list
    a = tsquotes_all[1:5][1:10]
    b = tsquotes_all[[1, 2, 5]][1:10]
    
    follow is wrong
        cos 1, 2, 5 is not tsquotes_all's lable index
    b = tsquotes_all[1, 2, 5][1:10]
   
    
"""
a = tsquotes_all[1:5][1:10]
b = tsquotes_all[[1, 2, 5]][1:10]
c = tsquotes_all[['open','close']].loc[['2015-09-18','2015-09-21']]

sh = tsquotes_all