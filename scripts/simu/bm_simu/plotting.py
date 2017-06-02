import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches

import matplotlib as mpl
mpl.rcParams['text.usetex'] = True

from bm import LinearBrownianMotion


def plot_bm_with_last_zero_lt(x):
    fig = plt.figure(figsize=(10,6))
    ax = fig.add_subplot(111)
    
    n = 0
    while True:
        B = LinearBrownianMotion.random(start=0, end=1, at=0, n_points=2000)
        z = B.last_zero()
        n += 1
        if x is None or z <= x:
            break
        
    times = B.times()
    
    ax.plot(times, B(times), label='$B(t)$')
    ax.plot(z, 0, marker='o', color='red', markersize=5)
    
    add_last_zero_tick(ax, z)
    
    configure(ax)
    return ax, n

def configure(ax):
    ax.grid(True)
    ax.legend()
    
def add_last_zero_tick(ax, z):
    z_coords = (z, 0)
    text_coords = (z+0.05, -0.1)
    arrowprops = dict(facecolor='black', shrink=0.05, width=0.1, headwidth=4)
    ax.annotate(r'$\mathrm{Ultimo \,\, cero} \, (\approx %.4f)$' % z,
                xy=z_coords,
                xytext=text_coords,
                arrowprops=arrowprops)