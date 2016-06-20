import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

dates = pd.date_range('20130101',periods=6)
df = pd.DataFrame(np.random.randn(6,4),index=,columns=list('ABCD'))
df2 = pd.DataFrame({'A':1.,
                    'B':np.array([3]*4,dtype='int32'),
                    'C':'foo'})
print(dates)
print(df)
print(df2)
print(df2.dtypes)
print(df.values)
print(df.describe())
print(df.sort_index(axis=1,ascending=False))
print(df.sort(columns='B'))

# 1)slice
print(df['A']) #mid column
print(df.A)
print(df[['A','B']]) #mid columns
print(df[2:3]) #mid row
print(df[0:3]) #mid rows
# 2)lable
print(df.loc[:,['A','B']]) #mid columns
print(df.loc[dates[0]]) #mid row
print(df['20130102':'20130104']) #mid rows
print(df.loc['20130101':'20130104',['A','B']])
print(df.loc['20130102',['A','B']])
print(df.loc['20130102','A'])
# 3)locaction
print(df.iloc[3]) #mid row
print(df.iloc[3:5,0:2]) #mid rows,columns
print(df.iloc[[1,2,3],[0,2]])
print(df.iloc[1,1])
print(df.iat[1,1])
# 4)boolean
print(df[df['A']>0])
print(df[df>0])
df3 = df.copy()
df3['E'] = ['one','one','two','three','four','three']
print(df3)
print(df3[df3['E'].isin(['two','four'])])
print(df3[df3['E']=='one'])
# 5)multiIndex
dfmi = df.copy()
dfmi.index = pd.MultiIndex.from_tuples([(1,'a'),(2,'b'),(1,'c'),(2,'a'),(3,'b'),(2,'d')],names=['first','second'])
print(dfmi)
row = df.ix[1]
column = df['B']
print(row)
print(df)
print(df.sub(row,axis='columns'))
print(df)
print(df.sub(row,axis=1))
print(df.sub(column, axis='index'))
print(df.sub(column, axis=0))
print(dfmi.sub(column, axis=0, level='second'))


d = [{'one' : 1,'two':1},{'one' : 2,'two' : 2},{'one' : 3,'two' : 3},{'two' : 4}]
df = pd.DataFrame(d,index=['a','b','c','d'],columns=['one','two'])
df.index.name='index'

print(df)
print(df[df.isnull()['one']])#单个逻辑条件
print(df[(df.one >=1 ) & (df.one < 3) ])
print(df[df.isin([1,'four'])])

i = 8