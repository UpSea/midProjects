import matplotlib.pyplot as plt
import numpy as np


x = np.arange(0,30,0.01)
y = np.log(np.sin(x)) #mid ����log��ʾln
plt.plot(x,y)
plt.show()