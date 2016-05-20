#!/usr/bin/python
import pymongo
import time
conn = pymongo.MongoClient("192.168.0.212",27017)
db = conn.test #连接库test
#db.authenticate("tage","123") #用户认证


#//插入数据,_id自动创建
post = {"id": "1",
        "author": "Mike",
        "text": "My first blog post!",
        "tags": ["mongodb", "python", "pymongo"],
        "date": time.strftime('%Y-%m-%d %H:%M:%S')}
posts = db.posts
posts.insert(post) #把post数据插入posts聚合(表)中，返回一个ObjectId('...')


#//批量插入(一个列表里面包含了2个字典),_id自动创建
new_posts = [{"id": "2",
              "author": "Mike",
              "text": "Another post!",
              "tags": ["bulk", "insert"],
              "date": time.strftime('%Y-%m-%d %H:%M:%S')},
             {"id": "3",
              "author": "Eliot",
              "title": "MongoDB is fun",
              "text": "and pretty easy too!",
              "date": time.strftime('%Y-%m-%d %H:%M:%S')}]
posts = db.posts
posts.insert(new_posts) #把new_posts数据插入posts聚合(表)中，返回2个ObjectId('...')





#//更新数据
db.posts.update({'id':1},{"$set":{"text":"cscscascs"}})  #更新一个value
db.posts.update({'id':1},{"$set":{"text":"cscscascs","title":"test title"}})  #更新多个value


#//查询数据
a = db.collection_names()  #查询所有聚合名称
a = db.posts.count() #统计posts聚合中的数据数量
a = db.posts.find() #查询posts中所有内容
a = db.posts.find_one({"author":"Mike"}) #根据条件查询posts中数据
a = db.posts.find({"author":"Mike"}).sort('author')  #--默认为升序
a = db.posts.find({"author":"Mike"}).sort('author',pymongo.ASCENDING)  #升序
a = db.posts.find({"author":"Mike"}).sort('author',pymongo.DESCENDING) #降序

#//删除数据
db.posts.remove() #删除posts聚合(表)中所有数据
db.posts.remove({'id':1}) #删除posts聚合(表)中id为1的数据