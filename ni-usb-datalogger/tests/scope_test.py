import numpy as np
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
# to search for the latest file
import glob
import os

global fx, fy, fz, t


# to find the latest file
dir_path = os.path.dirname(os.path.realpath(__file__))
list_of_files = glob.glob(dir_path+'\*.txt') # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)
#print(latest_file)

def read_data():
    global fx, fy, fz, t
    with open(latest_file, 'r') as file:
        data_in = list(file)[-1]
        data_out = data_in.split(",")
    t = float(data_out[0])
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
    def __init__(self, ax, maxt):
        self.ax = ax
        self.maxt = maxt
        self.tdata = [0]
        self.ydata = [0]
        self.line = Line2D(self.tdata, self.ydata)
        self.ax.add_line(self.line)
        self.ax.set_ylim(-100, 100)
        self.ax.set_xlim(0, self.maxt)

    def update(self, y):
        global t
        lastt = self.tdata[-1]
        if lastt > self.tdata[0] + self.maxt:  # reset the arrays
            self.tdata = [self.tdata[-1]]
            self.ydata = [self.ydata[-1]]
            self.ax.set_xlim(self.tdata[0], self.tdata[0] + self.maxt)
            self.ax.figure.canvas.draw()

        #t = self.tdata[-1] + self.dt

        self.tdata.append(t)
        self.ydata.append(y)
        self.line.set_data(self.tdata, self.ydata)
        return self.line,


if __name__ == '__main__':
    # Scope
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3)
    #ax1.set_xlabel('Time (s)')
    fig.text(0.5, 0.04, 'Time (s)', ha='center', va='center')
    ax1.set_ylabel('Force (N)')
    plt.tight_layout(pad=3)

    #ax1.title('Gaussian colored noise')
    #fig, ax1 = plt.subplots()

    scope1 = Scope(ax1,5)
    scope2 = Scope(ax2,5)
    scope3 = Scope(ax3,5)

    ani1 = animation.FuncAnimation(fig, scope1.update, read_fx, interval=10, blit=True)
    ani2 = animation.FuncAnimation(fig, scope2.update, read_fy, interval=10, blit=True)
    ani3 = animation.FuncAnimation(fig, scope3.update, read_fz, interval=10, blit=True)

    plt.show()

