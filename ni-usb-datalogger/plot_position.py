import numpy as np
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import math
import time
# to search for the latest file
import glob
import os

# multiprocess
from multiprocessing import Process
global pos


# to find the latest file
dir_path = os.path.dirname(os.path.realpath(__file__))
list_of_files = glob.glob(dir_path+'\*.txt') # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)
#print(latest_file)

def read_data():
    global pos, filename
    with open(filename, 'r') as file:
        data_in = list(file)[-1]
        data_out = data_in.split(",")

    pos = [float(data_out[5]), float(data_out[6]), float(data_out[7])]

def read_pos():
    global pos
    while True:
        read_data()
        yield pos

class Scope(object):
    def __init__(self, ax):
        self.ax = ax
        self.x = [0]
        self.y = [0]
        self.z = [0]

    def update_3d(self, position):
        self.pos = position
        self.x = float(self.pos[0])
        self.y = float(self.pos[1])
        self.z = float(self.pos[2])
        self.ax.cla()
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.ax.set_title('Plane position')
        self.ax.quiver(0, 0, 0, self.x, self.y, self.z, pivot="tail", color="black")
        self.ax.quiver(0, 0, 0, self.x, 0, 0, color="blue", linestyle="dashed")
        self.ax.quiver(0, 0, 0, 0, self.y, 0, color="blue", linestyle="dashed")
        self.ax.quiver(0, 0, 0, 0, 0, self.z, color="blue", linestyle="dashed")
        self.ax.set_xlim(-15, 15)
        self.ax.set_ylim(-15, 15)
        self.ax.set_zlim(0, 15)
        #self.ax.view_init(elev=30, azim=60)
        self.ax.view_init(elev=30, azim=-37.5)

def plot_data(filename_in):
    global filename
    filename = filename_in

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    #ax1.title('Gaussian colored noise')
    #fig, ax1 = plt.subplots()

    scope = Scope(ax)

    ani = animation.FuncAnimation(fig, scope.update_3d, read_pos, interval=40, blit=False)

    plt.show()

if __name__ == '__main__':
    # Create fig and plot data
    plot_data(latest_file)
