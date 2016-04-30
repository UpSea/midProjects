import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
x = np.linspace(0, 10, 1000)
line, = ax.plot(x, np.sin(x), lw=2, animated=True) 

fig.canvas.draw() 
background = fig.canvas.copy_from_bbox(ax.bbox) 

def update_data(line):
    x[:] += 0.1
    line.set_ydata(np.sin(x))
    fig.canvas.restore_region(background)  
    ax.draw_artist(line)     
    fig.canvas.blit(ax.bbox) 

timer = fig.canvas.new_timer(interval=5)
timer.add_callback(update_data, line)
timer.start()

plt.show()