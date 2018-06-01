# Libraries
import nidaqmx.stream_readers
import numpy as np
import time

from matplotlib import style
# Vars
global data
data = np.empty([6,])
global time_interval
time_interval = []
global now
global last_time
###################################################################################################
calibration = np.matrix('0.15596   0.05364  -0.29616 -22.76401   0.71258  22.77619; '
                        '0.17628  25.86714  -0.34444 -13.07013  -0.42680 -13.39725; '
                        '29.42932  -1.68566  29.50395  -0.09508  29.75563  -1.01253; '
                        '0.00754   0.22624  -0.47721  -0.11727   0.47877  -0.12927; '
                        '0.53998  -0.02617  -0.25730   0.19768  -0.29711  -0.19153; '
                        '0.00107  -0.33260  -0.00357  -0.34021  -0.01832  -0.33980')
###################################################################################################

def tare_sensor():
    global tare
    tare = np.empty([6, ])
    print("Press ENTER to tare")
    while input() != '':
        pass
    my_multi_channel_ai_reader.read_one_sample(tare, timeout=10)
    print("Done")

def init_stream():
    global my_multi_channel_ai_reader
    global task
    global my_stream
    task = nidaqmx.Task()
    task.ai_channels.add_ai_voltage_chan("Dev1/ai0:5")
    my_stream = nidaqmx._task_modules.in_stream.InStream(task)
    # my_stream.configure_logging("C:\\Users\\BrunoChapdelaine\\Desktop", nidaqmx.constants.LoggingMode.LOG_AND_READ)
    my_multi_channel_ai_reader = nidaqmx.stream_readers.AnalogMultiChannelReader(my_stream)

def read_data():
    global last_time
    my_multi_channel_ai_reader.read_one_sample(data, timeout=10)
    data_tared = data - tare
    data_tared = data_tared[np.newaxis, :].T
    data_tared_cal = np.dot(calibration, data_tared)

    now = time.time()
    time_interval.append(now - last_time)
    last_time = now
    return data_tared_cal

def reading_freq():
    mean_delay = np.average(time_interval[2:len(time_interval)])
    print(str(int(round(1 / mean_delay))) + ' Hz')

if __name__ == '__main__':
    global last_time
    init_stream() # initialize stream
    tare_sensor() # tare sensor
    last_time = time.time()
    for i in range(1000):
        read_data()
        #time.sleep(2)
        #print(str((time.time() - start_time)*1000.0) + " milliseconds")
        #print(str((time.time() - start_time)) + " seconds")
        #delay.append((time.time() - time2))
        #time2 = time.time()
        # Ajouter un tag de temps depuis le début du programme
    reading_freq()
    task.close() # end task
    #print(delay)
    #mean_delay = np.average(delay[1:len(delay)])
    #print(str((1 / mean_delay)) + ' Hz')
    #print(str(int(round(1/mean_delay)))+' Hz')