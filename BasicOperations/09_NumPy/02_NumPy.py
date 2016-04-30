import numpy as np
x= np.array([[1,2,3],[3,4,6]]) # 2 by 3 matrix
# number of data items
size1=(np.size(x)) 
# show number of columns
size2=(np.size(x,1)) 

std1=(np.std(x))

std2=np.std(x,1)
std3=np.std(x,0)
total=x.sum() # pay attention to the format
z=np.random.rand(50)# 50 random obs from [0.0, 1)
y=np.random.normal(size=100) # from standard normal
r=np.array(range(0,100),float)/100 # from 0, .01,to .99
print(x)
print(size1)
print(size2)
print(std1)
print(std2)
print(std3)
'''
print(z)
print(y)
print(r)
'''
import numpy as np   
x = [1,2,3,20]
y = np.array(x)

print(x,y) # be careful of format(coma)