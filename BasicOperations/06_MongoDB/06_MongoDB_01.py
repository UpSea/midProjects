#!/usr/bin/env python
#coding:utf-8
# Author:   --<qingfengkuyu>
# Purpose: MongoDB的使用
# Created: 2014/4/14
#32位的版本最多只能存储2.5GB的数据（NoSQLFan：最大文件尺寸为2G，生产环境推荐64位）

import pymongo
import datetime
import random

#创建连接
conn = pymongo.MongoClient('192.168.1.100',27017)
#连接数据库
db = conn.study
#db = conn['study']

#打印所有聚集名称，连接聚集
#print u'所有聚集:',db.collection_names()
posts = db.post
#posts = db['post']
#print posts

#插入记录
new_post = {"AccountID":22,"UserName":"Ubuntu.libing",'date':datetime.datetime.now()}
new_posts = [{"AccountID":22,"UserName":"liuw",'date':datetime.datetime.now()},
             {"AccountID":23,"UserName":"urling",'date':datetime.datetime.now()}]#每条记录插入时间都不一样

posts.insert(new_post)
#posts.insert(new_posts)#批量插入多条数据

#删除记录
#print u'删除指定记录:\n',posts.find_one({"AccountID":22,"UserName":"libing"})
#posts.remove({"AccountID":22,"UserName":"libing"})

#修改聚集内的记录
posts.update({"UserName":"urling"},{"$set":{'AccountID':random.randint(20,50)}})

#查询记录，统计记录数量
#print u'记录总计为：',posts.count(),posts.find().count()
#print u'查询单条记录:\n',posts.find_one()
#print posts.find_one({"UserName":"liuw"})

#查询所有记录
#print u'查询多条记录:'
#for item in posts.find():#查询全部记录
#for item in posts.find({"UserName":"urling"}):#查询指定记录
#for item in posts.find().sort("UserName"):#查询结果根据UserName排序，默认为升序
#for item in posts.find().sort("UserName",pymongo.ASCENDING):#查询结果根据UserName排序，ASCENDING为升序,DESCENDING为降序
for item in posts.find().sort([("UserName",pymongo.ASCENDING),('date',pymongo.DESCENDING)]):#查询结果根据多列排序
    print (item)

#查看查询语句的性能
#posts.create_index([("UserName", pymongo.ASCENDING), ("date", pymongo.DESCENDING)])#加索引
#print posts.find().sort([("UserName",pymongo.ASCENDING),('date',pymongo.DESCENDING)]).explain()["cursor"]#未加索引用BasicCursor查询记录
#print posts.find().sort([("UserName",pymongo.ASCENDING),('date',pymongo.DESCENDING)]).explain()["nscanned"]#查询语句执行时查询的记录数