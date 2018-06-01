# Libraries

# For plotting app
import time
import dash
import dash_core_components as dcc
import dash_html_components as html
from collections import deque
import plotly.graph_objs as go
import logging



# Stop suppress dash server posts to console
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Define app vars
app = dash.Dash('sensor-data')

maxLineLength = 20
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

def read_data():
    with open('ATI45.txt', 'r') as log:
        data_in = list(log)[-1]
        data_out = data_in.split(",")
    return data_out
def add_data_to_plot(data):
    times.append(time.time())
    fx.append(data[1])
    fy.append(data[2])
    fz.append(data[3])
    #mx.append(data_tared_cal[3,0])
    #my.append(data_tared_cal[4,0])
    #mz.append(data_tared_cal[5,0])
    return times, fx, fy, fz

def init_time():
    global start_time
    start_time = time.time()
    return
# Initialize values

times, fx, fy, fz = add_data_to_plot(read_data())

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
                 value=['Force en X', 'Force en Y', 'Force en Z'], #default values at startup
                 multi=True
                 ),
    html.Div(children=html.Div(id='graphs'), className='row'),
    dcc.Interval(
        id='graph-update',
        interval=500, #graph update interval in ms
        n_intervals=0)
    ], className="container",style={'width':'98%','margin-left':10,'margin-right':10,'max-width':50000}) #maxwidth peut être enlevé si vu sur ordi

@app.callback(
    dash.dependencies.Output('graphs','children'),
    [dash.dependencies.Input('sensor-data-name', 'value')],
    events=[dash.dependencies.Event('graph-update', 'interval')]
    )
def update_graph(data_names):
    graphs = []
    data = read_data()
    add_data_to_plot(data)
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
            animate=True,
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