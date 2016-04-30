
#所以lambda中没有return语句。也不能使用if, while等等。其背后的设计哲学为：

a = map(lambda x: print(x ** 2), [1, 2, 3, 4, 5])
[b for b in a]

b = map(lambda x, y,z: x + y+z, [1, 3, 5, 7, 9], [2, 4, 6, 8, 10],[3]*5)
[print(c) for c in b]

c = 3


mylist = ["my name is %(name)s", "and my age is %(age)d"]
mydict = {'name': 'Tom', 'age': 13}

result = map(lambda x: x % mydict, mylist)
for s in result:
    print (s)
    
print(type(result))