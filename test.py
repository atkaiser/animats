"""
Matplotlib Animation Example

author: Jake Vanderplas
email: vanderplas@astro.washington.edu
website: http://jakevdp.github.com
license: BSD
Please feel free to use and modify this, but keep the above information. Thanks!
"""

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
ax = plt.axes(xlim=(0, 200), ylim=(0, 200))
particles, = ax.plot([], [], 'bo')
particles2, = ax.plot([], [], 'ro')

# initialization function: plot the background of each frame
def init():
    particles.set_data([], [])
    particles2.set_data([], [])
    return (particles, particles2)

# animation function.  This is called sequentially
def animate(i):
    print i
    particles.set_data([i], [i])
    particles2.set_data([200-i], [200-i])
    return (particles, particles2)

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=200, interval=20, blit=False)

plt.show()