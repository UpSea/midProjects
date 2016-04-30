import numpy as np
import pandas as pd

np.random.seed(123456)
bymin = pd.Series(np.random.randn(24*60*90),
pd.date_range('2014-08-01',
              '2014-10-29 23:59',
              freq='T'))
#print(bymin)
#print(bymin['2014-08-01 00:02':'2014-08-01 00:10'])

dti = pd.date_range('2014-08-29', '2014-09-05', freq='B')
#[print(date) for date in dti.values]
from datetime import datetime
d = datetime(2014, 8, 29)
do = pd.DateOffset(days = 1)
print(d + do)
# import the data offset types
from pandas.tseries.offsets import *
# calculate one business day from 2014-8-31
print(d + BusinessDay())
print(d + 2 * BusinessDay())
'''
The following demonstrates using a  BMonthEnd object to calculate the last business day of
a month from a given date (in this case,  2014-09-02 ):
'''
# what is the next business month end
# from a specific date?
print(d + 2*BMonthEnd())
print(BMonthEnd().rollforward(datetime(2014, 9, 15)))

# get all wednesdays
wednesdays = pd.date_range('2014-06-01',
                           '2014-08-31', 
                           freq="W-WED")
[print(date) for date in wednesdays.values]

