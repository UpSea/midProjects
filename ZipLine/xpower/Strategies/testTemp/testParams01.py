import numpy as np

t = np.arange(0.0, 10.0, 0.01)
s = np.sin(2*np.pi*t)
params={}
params['s']=s
params['t']=t