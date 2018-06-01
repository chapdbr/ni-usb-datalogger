import nidaqmx.stream_readers
import numpy as np

data = np.empty([6,])
calibration = np.matrix('0.15596   0.05364  -0.29616 -22.76401   0.71258  22.77619; '
                        '0.17628  25.86714  -0.34444 -13.07013  -0.42680 -13.39725; '
                        '29.42932  -1.68566  29.50395  -0.09508  29.75563  -1.01253; '
                        '0.00754   0.22624  -0.47721  -0.11727   0.47877  -0.12927; '
                        '0.53998  -0.02617  -0.25730   0.19768  -0.29711  -0.19153; '
                        '0.00107  -0.33260  -0.00357  -0.34021  -0.01832  -0.33980')

with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("Dev1/ai0:5")
    my_stream = nidaqmx._task_modules.in_stream.InStream(task)
    my_multi_channel_ai_reader = nidaqmx.stream_readers.AnalogMultiChannelReader(my_stream)

    # Tare
    print("Press ENTER to tare")
    while input() != '':
        pass
    my_multi_channel_ai_reader.read_one_sample(data,timeout=10)
    tare = data
    print("Done")

    # Data output
    while True:
        my_multi_channel_ai_reader.read_one_sample(data,timeout=10)
        data_tared = data - tare
        data_tared = data_tared[np.newaxis, :].T
        data_tared_cal = np.dot(calibration,data_tared)
        print(data_tared_cal)

