
1)
import matplotlib.pyplot as plt     
fig = plt.figure()
ax1 = fig.add_subplot(3,2,1)

2)
ax2 = plt.subplot(312, sharex=ax1)
ax2.plot(results.index, results.AAPL)

3)
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

fig    = Figure()
canvas = FigureCanvas(fig)
ax     = fig.add_axes([0.1, 0.1, 0.8, 0.8])