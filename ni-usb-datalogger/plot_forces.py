import numpy as np
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math
import time
# to search for the latest file
import glob
import os

# multiprocess
from multiprocessing import Process
global fx, fy, fz, t


# to find the latest file
dir_path = os.path.dirname(os.path.realpath(__file__))
list_of_files = glob.glob(dir_path+'\*.txt') # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)
#print(latest_file)

def read_data():
    global fx, fy, fz, fr, t, filename
    with open(filename, 'r') as file:
        data_in = list(file)[-1]
        data_out = data_in.split(",")
    t = float(data_out[0])
    fx = float(data_out[1])
    fy = float(data_out[2])
    fz = float(data_out[3])
    fr = float(data_out[4])
    #mx = data_out[5]
    #my = data_out[6]
    #mz = data_out[7]

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
def read_fr():
    global fr
    while True:
        yield fr

class Scope(object):
    def __init__(self, ax, maxt, type):
        self.ax = ax
        self.maxt = maxt
        self.type = type # to limit axes and set color
        self.tdata = [0]
        self.ydata = [0]
        if type == 'f': # to set color
            self.line = Line2D(self.tdata, self.ydata, color='blue')
            self.ax.add_line(self.line)
        elif type == 'fr':
            self.line = Line2D(self.tdata, self.ydata, color='red')
            self.ax.add_line(self.line)
        if self.type == 'f': # for fx, fy, fz
            self.ax.set_ylim(-100, 100)
            self.ax.set_xlim(0, self.maxt)
        elif type == 'fr': # for fr
            self.ax.set_ylim(0, 200)
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

def plot_data(filename_in):
    global filename
    filename = filename_in
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(nrows=1, ncols=4, figsize=(14,7))
    #ax1.set_xlabel('Time (s)')
    fig.text(0.5, 0.04, 'Temps (s)', ha='center', va='center')
    ax1.set_ylabel('Force en X (N)')
    ax2.set_ylabel('Force en Y (N)')
    ax3.set_ylabel('Force en Z (N)')
    ax4.set_ylabel('Norme (N)')
    plt.tight_layout(pad=3)


    #ax1.title('Gaussian colored noise')
    #fig, ax1 = plt.subplots()

    scope1 = Scope(ax1, 5, 'f')
    scope2 = Scope(ax2, 5, 'f')
    scope3 = Scope(ax3, 5, 'f')
    scope4 = Scope(ax4, 5, 'fr')

    ani1 = animation.FuncAnimation(fig, scope1.update, read_fx, interval=40, blit=True)
    ani2 = animation.FuncAnimation(fig, scope2.update, read_fy, interval=40, blit=True)
    ani3 = animation.FuncAnimation(fig, scope3.update, read_fz, interval=40, blit=True)
    ani4 = animation.FuncAnimation(fig, scope4.update, read_fr, interval=40, blit=True)

    plt.show()

if __name__ == '__main__':
    # Create fig and plot data
    plot_data(latest_file)
