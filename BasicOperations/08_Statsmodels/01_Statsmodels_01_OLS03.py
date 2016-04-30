import statsmodels.api as sm
from matplotlib import pyplot as plt
data = sm.datasets.longley.load()
data.exog = sm.add_constant(data.exog)
mod_fit = sm.OLS(data.endog, data.exog).fit()
res = mod_fit.resid # residuals
fig = sm.qqplot(res)
plt.show()

#qqplot of the residuals against quantiles of t-distribution with 4 degrees of freedom:

import scipy.stats as stats
fig = sm.qqplot(res, stats.t, distargs=(4,))
plt.show()

#qqplot against same as above, but with mean 3 and std 10:

fig = sm.qqplot(res, stats.t, distargs=(4,), loc=3, scale=10)
plt.show()

#Automatically determine parameters for t distribution including the loc and scale:

fig = sm.qqplot(res, stats.t, fit=True, line='45')
plt.show()

