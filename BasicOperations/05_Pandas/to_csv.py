import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

dates = pd.date_range('20130101',periods=6)
df = pd.DataFrame(np.random.randn(6,4),index=dates,columns=list('ABCD'))
df2 = pd.DataFrame({'A':1.,
                    'B':np.array([3]*4,dtype='int32'),
                    'C':'foo'})
import os,sys
xpower = os.path.abspath(os.path.join(os.path.dirname(__file__),'temp.csv'))

df2.to_csv(xpower, columns=None, header=True, index=False) #mid if index = False,index will not be write to csv file.
print(dates)
print(df)
print(df2)