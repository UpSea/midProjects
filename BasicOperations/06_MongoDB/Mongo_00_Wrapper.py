#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
mid 201512011843
此类用于操作通过PyMongo操作Mongodb

包含外部数据源操作时，建立新类，加入新数据源的操作方法。
如此，可针对每个外部数据源新建处理类，减少在此类中判断的复杂度。

1.填充数据到数据库
类实例被调用后，根据参数获得外部数据源（各种非本Mongodb的数据源），之后存入Mongodb

2.检索数据
检索得到的数据需要被打包成DataFrame格式返回给调用者。
'''
import pymongo

class Client(object):
    
    def __init__(self, host, port):
        #conn 类型<class 'pymongo.connection.Connection'>
        try:
            self.conn = pymongo.MongoClient(host, port)
        except  Error:
            print ('connect to %s:%s fail' %(host, port))
            exit(0)

    def __del__(self):
        self.conn.close()

    def use(self, dbname):
        # 这种[]获取方式同样适用于shell,下面的collection也一样
        #db 类型<class 'pymongo.database.Database'>
        self.db = self.conn[dbname]

    def setCollection(self, collection):
        if not self.db:
            print ('don\'t assign database')
            exit(0)
        else:
            self.coll = self.db[collection]

    def find(self, query = {}):
        #注意这里query是dict类型
        if type(query) is not dict:
            print ('the type of query isn\'t dict')
            exit(0)
        try:
            #result类型<class 'pymongo.cursor.Cursor'>
            if not self.coll:
                print ('don\'t assign collection')
            else:
                result = self.coll.find(query)
        except NameError:
            print ('some fields name are wrong in ',query)
            exit(0)
        return result

    def insert(self, data):
        if type(data) is not dict:
            print ('the type of insert data isn\'t dict')
            exit(0)
        #insert会返回新插入数据的_id
        self.coll.insert(data)

    def remove(self, data):
        if type(data) is not dict:
            print ('the type of remove data isn\'t dict')
            exit(0)
        #remove无返回值
        self.coll.remove(data)

    def update(self, data, setdata):
        if type(data) is not dict or type(setdata) is not dict:
            print ('the type of update and data isn\'t dict')
            exit(0)
        #update无返回值
        self.coll.update(data,{'$set':setdata})
        
        
