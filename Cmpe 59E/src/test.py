import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
from math import ceil
import math
from pred import Pred
from prey import Prey
import parameters

white = 0.5
red = 1.
blue = 0.
n = parameters.gridSize

xs = 22
ys = 22
xd = 30
yd = 32

prd = Pred(xs, ys, 2, red)
pry = Prey(xd, yd, 1, blue)

def drawcircle(grid, x0, y0, radius):
    def putpixel(x,y):
        grid[x,y] = red
    
    x = radius;
    y = 0;
    err = 0;

    while (x >= y):
    
        putpixel(x0 + x, y0 + y);
        putpixel(x0 + y, y0 + x);
        putpixel(x0 - y, y0 + x);
        putpixel(x0 - x, y0 + y);
        putpixel(x0 - x, y0 - y);
        putpixel(x0 - y, y0 - x);
        putpixel(x0 + y, y0 - x);
        putpixel(x0 + x, y0 - y);
        
        y += 1;
        err += 1 + 2*y;
        if (2*(err-x) + 1 > 0):
            x -= 1;
            err += 1 - 2*x;

def generate_data():
    global prd, pry
    a = np.zeros((n, n)) + white
    a[prd.x,prd.y] = prd.gNumber
    a[pry.x,pry.y] = pry.gNumber
    pry.runAway(prd)
    prd.chase(pry)
    return a

def update(data):
    mat.set_data(data)
    return mat 

def data_gen():
    while True:
        yield generate_data()

fig, ax = plt.subplots(figsize=(20,13))
mat = ax.matshow(generate_data(), cmap='seismic', aspect='auto')
plt.colorbar(mat)
ani = animation.FuncAnimation(fig=fig, func=update, frames=data_gen, interval=500,
                              save_count=50)
plt.show()

#print np.arange(25).reshape(5, 5)

#ani.save('animation.mp4', clear_temp=False)
#convert *.png animation.gif