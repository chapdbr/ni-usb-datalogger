# Libraries
# For sensor reading
import nidaqmx.stream_readers
import numpy as np
import time
# For plotting app
import dash
import dash_core_components as dcc
import dash_html_components as html
from collections import deque
import plotly.graph_objs as go
import logging

# Define sensor reading vars
global data
data = np.empty([6,])
global delay
delay = []
global input_time
input_time = []

# Stop suppress dash server posts to console
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Define app vars
app = dash.Dash('sensor-data')

max_length = 20
times = deque(maxlen=max_length)
fx = deque(maxlen=max_length)
fy = deque(maxlen=max_length)
fz = deque(maxlen=max_length)
mx = deque(maxlen=max_length)
my = deque(maxlen=max_length)
mz = deque(maxlen=max_length)

data_dict = {"Force en X":fx,
"Force en Y":fy,
"Force en Z":fz,
"Moment en X":mx,
"Moment en Y":my,
"Moment en Z":mz}

###################################################################################################
calibration = np.matrix('0.15596   0.05364  -0.29616 -22.76401   0.71258  22.77619; '
                        '0.17628  25.86714  -0.34444 -13.07013  -0.42680 -13.39725; '
                        '29.42932  -1.68566  29.50395  -0.09508  29.75563  -1.01253; '
                        '0.00754   0.22624  -0.47721  -0.11727   0.47877  -0.12927; '
                        '0.53998  -0.02617  -0.25730   0.19768  -0.29711  -0.19153; '
                        '0.00107  -0.33260  -0.00357  -0.34021  -0.01832  -0.33980')
###################################################################################################

def read_data():
    my_multi_channel_ai_reader.read_one_sample(data,timeout=10)
    data_tared = data - tare
    data_tared = data_tared[np.newaxis, :].T
    data_tared_cal = np.dot(calibration,data_tared)
    #input_time = (time.time()-start_time)
    return data_tared_cal

def add_data_to_plot(data_tared_cal):
    times.append(time.time())
    fx.append(data_tared_cal[0,0])
    fy.append(data_tared_cal[1,0])
    fz.append(data_tared_cal[2,0])
    mx.append(data_tared_cal[3,0])
    my.append(data_tared_cal[4,0])
    mz.append(data_tared_cal[5,0])
    return times, fx, fy, fz, mx, my, mz

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
# Initialize values

init_stream() # initialize stream
tare_sensor() # tare sensor
init_time()  # initialize time
data_tared_cal = read_data()
times, fx, fy, fz, mx, my, mz = add_data_to_plot(data_tared_cal)

# Define app layout
app.layout = html.Div([
    html.Div([
        html.H2('Sensor Data',
                style={'float': 'left',
                       }),
        ]),
    dcc.Dropdown(id='sensor-data-name', #dropdown menu
                 options=[{'label': s, 'value': s}
                          for s in data_dict.keys()],
                 value=['Force en X','Force en Y','Force en Z'], #default values at startup
                 multi=True
                 ),
    html.Div(children=html.Div(id='graphs'), className='row'),
    dcc.Interval(
        id='graph-update',
        interval=100, #graph update interval in ms
        n_intervals=0)
    ], className="container",style={'width':'98%','margin-left':10,'margin-right':10,'max-width':50000}) #maxwidth peut être enlevé si vu sur ordi

@app.callback(
    dash.dependencies.Output('graphs','children'),
    [dash.dependencies.Input('sensor-data-name', 'value')],
    events=[dash.dependencies.Event('graph-update', 'interval')]
    )
def update_graph(data_names):
    graphs = []
    data_tared_cal = read_data()

    data2plot = open('data.txt','r').read()
    lines
    add_data_to_plot(data_tared_cal)
    if len(data_names)>2:
        class_choice = 'col s12 m6 l4'
    elif len(data_names) == 2:
        class_choice = 'col s12 m6 l6'
    else:
        class_choice = 'col s12'


    for data_name in data_names:

        data = go.Scatter(
            x=list(times),
            y=list(data_dict[data_name]),
            name='Scatter',
            fill="tozeroy",
            fillcolor="#6897bb"
            )

        graphs.append(html.Div(dcc.Graph(
            id=data_name,
            animate=False,
            figure={'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(times),max(times)]),
                                                        yaxis=dict(range=[-100,100]),
                                                        margin={'l':50,'r':1,'t':45,'b':1},
                                                        title='{}'.format(data_name))}
            ), className=class_choice))

    return graphs

external_css = ["https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css"]
for css in external_css:
    app.css.append_css({"external_url": css})

external_js = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js']
for js in external_css:
    app.scripts.append_script({'external_url': js})


if __name__ == '__main__':
    app.run_server(debug=False)
    print('proot')
    #task.close() # end task