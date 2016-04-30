dict = {"a" : "apple", "b" : "banana"}
print (dict)
dict2 = {"c" : "grape", "d" : "orange"}
dict.update(dict2) # add dict2 to dict
print (dict)
#udpate()的等价语句
D = {"key1" : "value1", "key2" : "value2"}
E = {"key3" : "value3", "key4" : "value4"}
for k in E:
    D[k] = E[k]
print (D)