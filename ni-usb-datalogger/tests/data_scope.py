
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import time
global fx, fy, fz
def read_data():
    global fx, fy, fz
    with open('ATI45.txt', 'r') as file:
        data_in = list(file)[-1]
        data_out = data_in.split(",")
    fx = float(data_out[1])
    fy = float(data_out[2])
    fz = float(data_out[3])
    #mx = data_out[4]
    #my = data_out[5]
    #mz = data_out[6]

def read_fx():
    global fx
    while True:
        read_data()
        yield fx
def read_fy():
    global fy
    while True:
        yield fy
def read_fz():
    global fz
    while True:
        yield fz
def read_mx():
    global mx
    while True:
        yield mx
def read_my():
    global my
    while True:
        yield my
def read_mz():
    global mz
    while True:
        yield mz



class Scope(object):
    def __init__(self, ax, maxt, dt):
        self.ax = ax
        self.dt = dt
        self.maxt = maxt
        self.tdata = [0]
        self.ydata = [0]
        self.line, = plt.plot(self.tdata, self.ydata, 'r', animated=True)
        #self.ax.add_line(self.line)
        self.ax.set_ylim(-100, 100)
        self.ax.set_xlim(0, self.maxt)
        self.line.set_data(self.tdata, self.ydata)

    def update(self, y):
        self.lastt = self.tdata[-1]
        if self.lastt > self.tdata[0] + self.maxt:  # reset the arrays
            self.tdata = [self.tdata[-1]]
            self.ydata = [self.ydata[-1]]
            self.ax.set_xlim(self.tdata[0], self.tdata[0] + self.maxt)
            self.ax.figure.canvas.draw()

        self.t = self.tdata[-1] + self.dt
        self.tdata.append(self.t)
        self.ydata.append(y)
        self.line.set_data(self.tdata, self.ydata)
        return self.line,
def emitter(p=0.03):
    'return a random value with probability p, else 0'
    while True:
        v = np.random.rand(1)
        if v > p:
            yield 0.
        else:
            yield np.random.rand(1)

if __name__ == '__main__':
    # Scope
    #fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3)
    #fig, ax1 = plt.subplots()
    fig1, ax1 = plt.subplots()
    fig2, ax2 = plt.subplots()
    fig3, ax3 = plt.subplots()
    scope1 = Scope(ax1,2,0.05)
    scope2 = Scope(ax2,2,0.05)
    scope3 = Scope(ax3,2,0.05)

    ani1 = animation.FuncAnimation(fig1, scope1.update, read_fx, interval=50, blit=True)
    ani2 = animation.FuncAnimation(fig2, scope2.update, read_fy, interval=50, blit=True)
    ani3 = animation.FuncAnimation(fig3, scope3.update, read_fz, interval=50, blit=True)

    plt.show()
