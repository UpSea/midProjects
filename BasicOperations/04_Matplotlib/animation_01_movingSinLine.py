import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
x = np.linspace(0, 10, 1000)
line, = ax.plot(x, np.sin(x), lw=2)

def update_data(line):
    x[:] += 0.1
    line.set_ydata(np.sin(x)) 
    fig.canvas.draw()         

timer = fig.canvas.new_timer(interval=0.005) 
timer.add_callback(update_data, line)
timer.start()

plt.show()