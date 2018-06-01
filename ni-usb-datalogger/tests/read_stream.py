import nidaqmx.stream_readers
import numpy as np

data = np.empty([6,])


task = nidaqmx.Task()
task.ai_channels.add_ai_voltage_chan("Dev1/ai0:5")
my_stream = nidaqmx._task_modules.in_stream.InStream(task)
my_multi_channel_ai_reader = nidaqmx.stream_readers.AnalogMultiChannelReader(my_stream)
for i in range(10):
    my_multi_channel_ai_reader.read_one_sample(data,timeout=10)
    print(data)
