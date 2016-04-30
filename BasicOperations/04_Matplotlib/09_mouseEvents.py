from numpy.random import rand, randint
from matplotlib.patches import RegularPolygon
import matplotlib.pyplot as plt
import numpy as np
import sys
#fig, ax = plt.subplots()

fig = plt.figure()
ax1 = fig.add_subplot(2,1,1)



ax = fig.add_subplot(2,1,2)
text = ax.text(0.5, 0.5, "event", ha="center", va="center", fontdict={"size":20})
ax1.plot([3,3,4,5])
def on_mouse(event):
    info = 'event.name:{}\nButton:{}\nFig x,y:{}, {}\nData x:{},\nData y:{}'.format(
        event.name,event.button,event.x,event.y,event.xdata,event.ydata) 
    print(info)
    print(type(event.xdata))
    text.set_text(info)
    fig.canvas.draw()
fig.canvas.mpl_connect('button_press_event', on_mouse)
fig.canvas.mpl_connect('button_release_event', on_mouse)
fig.canvas.mpl_connect('motion_notify_event', on_mouse);

plt.show()