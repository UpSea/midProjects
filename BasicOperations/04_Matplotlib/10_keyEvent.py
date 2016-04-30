from numpy.random import rand, randint
from matplotlib.patches import RegularPolygon
import matplotlib.pyplot as plt
import numpy as np
import sys

fig, ax = plt.subplots()
x = np.linspace(0, 10, 1000)
line, = ax.plot(x, np.sin(x))
text = ax.text(0.5, 0.5, "event", ha="center", va="center", fontdict={"size":20})
keys = 'typed:'
def on_key_press(event):
    if event.key in 'rgbcmyk':
        line.set_color(event.key)  
    else:
        tempKeys = '{}{}'.format(keys,event.key)
        text.set_text(tempKeys)

    fig.canvas.draw()              

fig.canvas.mpl_disconnect(fig.canvas.manager.key_press_handler_id)
fig.canvas.mpl_connect('key_press_event', on_key_press)

plt.show()