import pandas as pd
import statsmodels.api as sm
from patsy import dmatrices

#url='http://vincentarelbundock.github.com/Rdatasets/csv/HistData/Guerry.csv'
url='Guerry.csv'
df = pd.read_csv(url)
vars = ['Department','Lottery','Literacy','Wealth','Region']
df = df[vars]
df = df.dropna()
y,X=dmatrices('Lottery~Literacy+Wealth+Region',data=df,return_type='dataframe')
mod = sm.OLS(y,X)
res = mod.fit()
print(res.summary())
print(sm.stats.linear_rainbow(res))
sm.graphics.plot_partregress('Lottery','Wealth',['Region','Literacy'],data=df,obs_labels=False).show()
pause = 3