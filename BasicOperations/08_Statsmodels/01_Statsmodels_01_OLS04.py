import logbook
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
from datetime import datetime
import pytz

from zipline.algorithm import TradingAlgorithm
from zipline.transforms import batch_transform
from zipline.utils.factory import load_from_yahoo
from zipline.api import symbol
import matplotlib.pyplot as plt

"""Computes regression coefficient (slope and intercept)
via Ordinary Least Squares between two SIDs.
"""

px = [1,2,3,4,5]
py = [2,4,6,8,10]

px = sm.add_constant(px, prepend=True)

intercept, slope = sm.OLS(py, px).fit().params
print(slope, intercept)

plt.scatter(px[:,1],py)

x = np.linspace(0,6,100)
y = x*slope + intercept 

plt.plot(x,y)
plt.show()