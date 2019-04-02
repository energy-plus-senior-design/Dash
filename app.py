import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

import flask
import pandas as pd
import time
import os
from eplusparser.eplusparser import parse

server = flask.Flask('app')
server.secret_key = os.environ.get('secret_key', 'secret')

df = parse('../OpenStudio_Models/Office/run/eplusout.sql')

app = dash.Dash('app', server=server)

app.scripts.config.serve_locally = False
dcc._js_dist[0]['external_url'] = 'https://cdn.plot.ly/plotly-basic-latest.min.js'

app.layout = html.Div([
    html.H1('Stock Tickers'),
    dcc.Dropdown(
        id='my-dropdown',
        options= [{'label': i, 'value': i} for i in df.columns.levels[0]]
        # value='TSLA'
    ),
    dcc.Dropdown(
        id='my-dropdown-2',
        options= [{'label': i, 'value': i} for i in df.columns.levels[1]]
        # value='TSLA'
    ),
    dcc.Graph(id='my-graph')
], className="container")

app.select1 = ""
app.select2 = ""

@app.callback(Output('my-graph', 'figure'),
              [Input('my-dropdown', 'value'), Input('my-dropdown-2', 'value')])
def update_graph(s1, s2):
    app.select1 = s1
    app.select2 = s2
    dff = df["Electricity:Facility"]
    return {
        'data': [{
            'x': df.index.values,
            'y': df[app.select1][app.select2],
            'line': {
                'width': 3,
                'shape': 'spline'
            }
        }],
        'layout': {
            'margin': {
                'l': 30,
                'r': 20,
                'b': 30,
                't': 20
            }
        }
    }



# def variables_1(dataframe):


if __name__ == '__main__':
    app.run_server()