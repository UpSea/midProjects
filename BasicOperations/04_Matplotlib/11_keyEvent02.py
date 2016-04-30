from numpy.random import rand, randint
from matplotlib.patches import RegularPolygon
import matplotlib.pyplot as plt
import numpy as np
import sys

from matplotlib import pyplot as plt

fig, ax = plt.subplots()

def on_key_press(event):
    print(event.key)
    sys.stdout.flush()

fig.canvas.mpl_connect('key_press_event', on_key_press);

plt.show()