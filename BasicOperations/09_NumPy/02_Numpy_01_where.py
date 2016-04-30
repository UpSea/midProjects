import numpy as np

x = np.arange(9.).reshape(3, 3)

row,col = np.where( x > 5 )                 #mid 返回两以为数组，对应序数组成坐标对，此坐标对指向的数为满足条件的数
a1 = np.where(x>1)
b = x[np.where( x > 3.0 )]                  #mid result is 1D.

c = np.where(x < 5, x, -1)                  #mid broadcasting.

d = 8