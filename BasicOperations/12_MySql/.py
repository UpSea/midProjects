#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pymysql
import pymysql
try:
#获取一个数据库连接，注意如果是UTF-8类型的，需要制定数据库
    conn=pymysql.connect(host='qdm10645012.my3w.com',user='qdm10645012',passwd='asxxsw21',db='qdm10645012_db',port=3306,charset='utf8')    #
    
    cur = conn.cursor()
    
    select = 3
    if(select == 1):    #mid select string is not case senstive,all following three are right.
        cur.execute("SELECt VERSION()")
    elif(select == 2):
        cur.execute("select table_name from information_schema.tables")
    elif(select == 3):
        cur.execute("SELECT * FROM INFORMATION_SCHEMA.TABLES")

    select = 2
    if(select == 1):
        print (cur.description)
        r = cur.fetchall()
        print (r)
    elif(select == 2):
        for r in cur:
            print (r)
    
    cur.close()
    conn.close()
except  Exception :print("发生异常")