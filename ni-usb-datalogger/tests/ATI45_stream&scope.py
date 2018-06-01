# Libraries
import nidaqmx.stream_readers
import numpy as np
import time
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from matplotlib import style
# Vars
global data
data = np.empty([6,])
global delay
delay = []


###################################################################################################
calibration = np.matrix('0.15596   0.05364  -0.29616 -22.76401   0.71258  22.77619; '
                        '0.17628  25.86714  -0.34444 -13.07013  -0.42680 -13.39725; '
                        '29.42932  -1.68566  29.50395  -0.09508  29.75563  -1.01253; '
                        '0.00754   0.22624  -0.47721  -0.11727   0.47877  -0.12927; '
                        '0.53998  -0.02617  -0.25730   0.19768  -0.29711  -0.19153; '
                        '0.00107  -0.33260  -0.00357  -0.34021  -0.01832  -0.33980')
###################################################################################################

def read_data():
    global fx, fy, fz, mx, my, mz
    my_multi_channel_ai_reader.read_one_sample(data,timeout=10)
    data_tared = data - tare
    data_tared = data_tared[np.newaxis, :].T
    data_tared_cal = np.dot(calibration,data_tared)
    fx = int(data_tared_cal[0, 0])
    fy = int(data_tared_cal[1, 0])
    fz = int(data_tared_cal[2, 0])
    mx = int(data_tared_cal[3, 0])
    my = int(data_tared_cal[4, 0])
    mz = int(data_tared_cal[5, 0])
    return
def read_fx():
    read_data()
    yield fx
def read_fy():
    yield fy
def read_fz():
    yield fz
def read_mx():
    yield mx
def read_my():
    yield my
def read_mz():
    yield mz

def tare_sensor():
    global tare
    tare = np.empty([6, ])
    print("Press ENTER to tare")
    while input() != '':
        pass
    my_multi_channel_ai_reader.read_one_sample(tare, timeout=10)
    print("Done")
    return

def init_stream():
    global my_multi_channel_ai_reader
    global task
    global my_stream
    task = nidaqmx.Task()
    task.ai_channels.add_ai_voltage_chan("Dev1/ai0:5")
    my_stream = nidaqmx._task_modules.in_stream.InStream(task)
    #my_stream.configure_logging("C:\\Users\\BrunoChapdelaine\\Desktop", nidaqmx.constants.LoggingMode.LOG_AND_READ)
    my_multi_channel_ai_reader = nidaqmx.stream_readers.AnalogMultiChannelReader(my_stream)

    return
def init_time():
    global start_time
    start_time = time.time()
    return

class Scope(object):
    def __init__(self, ax, maxt=2, dt=0.2):
        self.ax = ax
        self.dt = dt
        self.maxt = maxt
        self.tdata = [0]
        self.ydata = [0]
        self.line = Line2D(self.tdata, self.ydata)
        self.ax.add_line(self.line)
        self.ax.set_ylim(-100, 100)
        self.ax.set_xlim(0, self.maxt)

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

if __name__ == '__main__':
    init_stream() # initialize stream
    tare_sensor() # tare sensor
    read_data()

    # Scope
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3)
    scope1 = Scope(ax1)
    scope2 = Scope(ax2)
    scope3 = Scope(ax3)

    # pass a generator in "emitter" to produce data for the update func
    ani1 = animation.FuncAnimation(fig, scope1.update, read_fx, interval=200, blit=True)
    ani2 = animation.FuncAnimation(fig, scope2.update, read_fy, interval=200, blit=True)
    ani3 = animation.FuncAnimation(fig, scope3.update, read_fz, interval=200, blit=True)

    plt.show()
