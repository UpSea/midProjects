
# sort a dict.
def sortedDictValues(adict,reverse=False):
    keys = adict.keys()
    keys.sort(reverse=reverse)
    return [adict[key] for key in keys]


# construct a dict from two list.
names = ['n1','n2','n3']
values = [1,2,3]

nvs = zip(names,values)
nvDict = dict( (name,value) for name,value in nvs)