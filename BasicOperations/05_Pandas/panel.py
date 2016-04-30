import pandas as pd
import numpy as np
index = pd.date_range('1/1/2000', periods=8)

s = pd.Series(np.random.randn(5), index=['a', 'b', 'c', 'd', 'e'])
df = pd.DataFrame(np.random.randn(8, 3), 
                  index=index,
                  columns=['A', 'B', 'C'])
wp = pd.Panel(np.random.randn(2, 5, 4), items=['Item1', 'Item2'],
              major_axis=pd.date_range('1/1/2000', periods=5),
              minor_axis=['A', 'B', 'C', 'D'])
print(wp.values)
print(wp)
major_mean = wp.mean(axis='major')
print(major_mean)
print(wp.sub(major_mean,axis='major').values)

import pandas.util.testing as tm
panel = tm.makePanel(5)
print(panel['ItemA'])
print(panel)
result = panel.apply(lambda x: x*2, axis='items')
print(result['ItemA'])
print(result)
result = panel.apply(lambda x: x.dtype, axis='items')
print(result)
result = panel.apply(lambda x:x.sum(),axis='major_axis')
print(result)
result = panel.apply(lambda x:x.sum(),axis='items')
print(result)

#A transformation operation that returns a Panel, 
#but is computing the z-score across the major_axis.
result = panel.apply(lambda x: (x-x.mean())/x.std(),axis='major_axis')
print(result)
print(result['ItemA'])
for item, frame in wp.iteritems():
    print(item)
    print(frame)
for row in df.itertuples():
    print(row)
    
df = pd.DataFrame({'a': ['foo', 'bar', 'baz'],'b': np.random.randn(3)})
print(df)
data = {'item1': df, 'item2': df}
panel = pd.Panel.from_dict(data, orient='minor')
print(panel)
print(panel['a'])
print(panel['b'])
print(panel['b'].dtypes)    
    
data = {'Item1' : pd.DataFrame(np.random.randn(4, 3)),
        'Item2' : pd.DataFrame(np.random.randn(4, 2))}
wp1 = pd.Panel(data)
wp2 = pd.Panel.from_dict(data, orient='minor')
print(wp1)
print(wp2)
print(wp1['Item1'])
print(wp2[0])

midx = pd.MultiIndex(levels=[['one', 'two'], ['x','y']], labels=[[1,1,0,0],[1,0,1,0]])
df = pd.DataFrame({'A' : [1, 2, 3, 4], 'B': [5, 6, 7, 8]}, index=midx)
print(df)
print(df.to_panel())

i = 8 