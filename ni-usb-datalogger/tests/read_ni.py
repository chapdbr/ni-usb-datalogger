import numpy as np
import nidaqmx

data = np.empty([6, 1])
task = nidaqmx.Task()
task.ai_channels.add_ai_voltage_chan("Dev1/ai0:5")

data = task.read()
print(data)

data = task.read()
print(data)