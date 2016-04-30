import pandas as pd
import numpy as np

df = pd.DataFrame(np.random.randn(10,3))
print('--'*20)
print(df)

df.ix[::2,0] = np.nan; df.ix[::4,1] = np.nan; df.ix[::3,2] = np.nan;
print('--'*20)
print(df)

#df.dropna()                 #drop all rows that have any NaN values
#df.dropna(how='all')        #drop only if ALL columns are NaN
#df.dropna(thresh=2)         #Drop row if it does not have at least two values that are **not** NaN
dfr = df.dropna(subset=[1])       #Drop only if NaN in specific column (as asked in the question)

print('--'*20)
print(df)
print('--'*20)
print(dfr)

print('##'*20)
ss = pd.Series([1,2,3,4,4,5,5])
r = ss.rank()
print(ss)
print(r)