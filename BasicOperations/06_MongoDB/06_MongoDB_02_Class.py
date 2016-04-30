#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pymongo

class PyConnect(object):
    
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

if __name__ == '__main__':
    connect = PyConnect('192.168.1.100', 27017)
    connect.use('test_for_new')
    connect.setCollection('collection1')
    connect.insert({'a':10, 'b':1})
    
    import datetime
    post = {"author": "Mike01",
            'father':
            {
                'age':60,
                'height':170,
                'weitht':150,
                'friends':
                {
                    'best':'bigcow',
                    'better':'littlebird'
                }
            },  
            "text": "My first blog post!",
            "tags": ["mongodb", "python", "pymongo"],
            "date": datetime.datetime.utcnow()
            }    
    connect.insert(post)
    connect.update({'a':100, 'b':1}, {'c':10})
    

    #connect.remove({'author':'Mike01'}) 
    connect.remove({'b':1})
    result = connect.find()
    for x in result:
        if 'c' in x:
            print (x['_id'], x['a'], x['b'], x['c'])
        elif 'text' in x:
            print ('author:',x['author'],'.Text:',x['text'])
