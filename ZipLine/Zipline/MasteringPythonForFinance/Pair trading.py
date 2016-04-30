# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 15:48:18 2015

@author: mid
"""
import numpy as np
import zipline as zp
import zipline.utils.factory as zpf
from datetime import datetime
import matplotlib.pyplot as plt

# load data for Coke and Pepsi and visualize
data = zpf.load_from_yahoo(stocks=['PEP', 'KO'], 
                           indexes={},
                           start=datetime(1997, 1, 1), 
                           end=datetime(1998, 6, 1), 
                           adjusted=True)
data.plot(figsize=(12,8));
plt.savefig('5104OS_07_20.png', bbox_inches='tight', dpi=300)

# calculate and plot the spread
plt.subplot()
data['Spread'] = data.PEP - data.KO
data['1997':].Spread.plot(figsize=(12,8))
plt.ylabel('Spread')
plt.axhline(data.Spread.mean());
plt.savefig('5104OS_07_21.png', bbox_inches='tight', dpi=300)


import statsmodels.api as sm
@zp.transforms.batch_transform
def ols_transform(data, ticker1, ticker2):
    """Compute the ordinary least squares of two series.
    """
    p0 = data.price[ticker1]
    p1 = sm.add_constant(data.price[ticker2], prepend=True)
    slope, intercept = sm.OLS(p0, p1).fit().params

    return slope, intercept
    
class Pairtrade(zp.TradingAlgorithm):
    """ Pairtrade algorithm for two stocks, using a window 
    of 100 days for calculation of the z-score and 
    normalization of the spread. We will execute on the spread 
    when the z-score is > 2.0 or < -2.0. If the absolute value 
    of the z-score is < 0.5, then we will empty our position 
    in the market to limit exposure.
    """
    def initialize(self, window_length=100):
        self.spreads=[]
        self.invested=False
        self.window_length=window_length
        self.ols_transform= \
            ols_transform(refresh_period=self.window_length,
                          window_length=self.window_length)

    def handle_data(self, data):
        # calculate the regression, will be None until 100 samples
        params=self.ols_transform.handle_data(data, 'PEP', 'KO')
        if params:
            # get the intercept and slope
            intercept, slope=params

            # now get the z-score
            zscore=self.compute_zscore(data, slope, intercept)

            # record the z-score
            self.record(zscore=zscore)

            # execute based upon the z-score
            self.place_orders(data, zscore)

    def compute_zscore(self, data, slope, intercept):
        # calculate the spread
        spread=(data['PEP'].price-(slope*data['KO'].price+ 
                                       intercept))
        self.spreads.append(spread) # record for z-score calc
        self.record(spread = spread)
        
        # now calc the z-score
        spread_wind=self.spreads[-self.window_length:]
        zscore=(spread - np.mean(spread_wind))/np.std(spread_wind)
        return zscore

    def place_orders(self, data, zscore):
        if zscore>=2.0 and not self.invested:
            # buy the spread, buying PEP and selling KO
            self.order('PEP', int(100/data['PEP'].price))
            self.order('KO', -int(100/data['KO'].price))
            self.invested=True
            self.record(action="PK")
        elif zscore<=-2.0 and not self.invested:
            # buy the spread, buying KO and selling PEP
            self.order('PEP', -int(100 / data['PEP'].price))
            self.order('KO', int(100 / data['KO'].price))
            self.invested = True
            self.record(action='KP')
        elif abs(zscore)<.5 and self.invested:
            # minimize exposure
            ko_amount=self.portfolio.positions['KO'].amount
            self.order('KO', -1*ko_amount)
            pep_amount=self.portfolio.positions['PEP'].amount
            self.order('PEP', -1*pep_amount)
            self.invested=False
            self.record(action='DE')
        else:
            # take no action
            self.record(action='noop')    

perf = Pairtrade().run(data['1997':])

# what actions did we take?
selection = ((perf.action=='PK') | (perf.action=='KP') |
             (perf.action=='DE'))
actions = perf[selection][['action']]
actions

# plot prices
ax1 = plt.subplot(411)
data[['PEP', 'KO']].plot(ax=ax1)
plt.ylabel('Price')

# %%plot spread
ax2 = plt.subplot(412, sharex=ax1)
data.Spread.plot(ax=ax2)
plt.ylabel('Spread')

# %%plot z-scores
ax3 = plt.subplot(413)
perf['1997':].zscore.plot()
ax3.axhline(2, color='k')
ax3.axhline(-2, color='k')
plt.ylabel('Z-score')

# %%plot portfolio value
ax4 = plt.subplot(414)
perf['1997':].portfolio_value.plot()
plt.ylabel('Protfolio Value')

# %%draw lines where we took actions
for ax in [ax1, ax2, ax3, ax4]:
    for d in actions.index[actions.action=='PK']:
        ax.axvline(d, color='g')
    for d in actions.index[actions.action=='KP']:
        ax.axvline(d, color='c')
    for d in actions.index[actions.action=='DE']:
        ax.axvline(d, color='r')

plt.gcf().set_size_inches(16, 12)
plt.savefig('5104OS_07_22.png', bbox_inches='tight', dpi=300)
''''''
