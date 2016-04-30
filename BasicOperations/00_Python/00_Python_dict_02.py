dict = {"a" : "apple", "b" : "banana", "g" : "grape", "o" : "orange"}
dict["w"] = "watermelon"
del(dict["a"]) # delete a
dict["g"] = "grapefruit"
print('01..',dict)
print (dict.pop("b")) #delete b and print b
print (dict)
dict.clear() #clear dict
print (dict)