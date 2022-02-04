
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pyodbc 
from dataclasses import dataclass
import datetime as dt

import config

@dataclass
class DashboardData:
    df: pd.DataFrame() = None
    timestamp: dt.datetime = dt.datetime(1970, 1, 1)
    
    def update_data(self, delay):
        if dt.datetime.now() - self.timestamp > delay:
            try:
                conn_str = ("Driver={SQL Server};"
                            "Server=" + config.server + ";"
                            "Database=" + config.database + ";"
                            "UID=" + config.user + ";"
                            "PWD=" + config.password + ";")
                conn = pyodbc.connect(conn_str)
                cursor = conn.cursor()
                self.df = pd.io.sql.read_sql("SELECT * from pokemondarrellgerber", conn)
                self.timestamp = dt.datetime.now()
            except Exception as e:
                print(e)
                df = None
                
globalData = DashboardData()
UpdateDelay = pd.Timedelta(10, unit='m') # seconds    

def create_name_graph():
    globalData.update_data(UpdateDelay)
    if(globalData.df is not None):
        df2 = globalData.df['pokename'].value_counts().head(10)
        fig = px.bar(df2)
        return fig
    else:
        return None
    
def create_location_graph():
    globalData.update_data(UpdateDelay)
    if(globalData.df is not None):
        df2 = globalData.df['placename'].value_counts().head(10)
        fig = px.bar(df2)
        return fig
    else:
        return None   
    

def create_map():
    globalData.update_data(UpdateDelay)
    if(globalData.df is not None):
        fig = px.scatter_geo(globalData.df,
                            lat="lat",
                            lon="long",
                            hover_name="pokename",
                             color="pokename",
                            title="Locations of Pokemon")
        fig.update_layout(showlegend=False)
        return fig
    else:
        return None

    
app = dash.Dash(__name__)
    
app.layout = html.Div(children = [
    html.H1(children='Pokemon Around the World'),
    
    dcc.Graph(
        id='Pokemon-Names',
        figure = create_name_graph(),
        style={
              'display': 'inline-block', "padding-left": "50px", "padding-bottom": "20px"}
    ),
    dcc.Graph(
        id='Pokemon-Places',
        figure=create_location_graph(),
        style={
            'display': 'inline-block', "padding-left": "50px", "padding-bottom": "20px"}
    ),
    dcc.Graph(
        id="Pokemon-Map",
        figure=create_map(),
        style={
              'display': 'inline-block', "padding-left": "50px", "padding-bottom": "20px"}
    ),
    dcc.Interval(
        id='interval-component',
        interval = 30*1000,
        n_intervals = 0
    )
])    

@app.callback(Output('Pokemon-Names', 'figure'), 
              Input('interval-component', 'n_intervals'))
def UpdateNameData(n):
    return create_name_graph()


@app.callback(Output('Pokemon-Places', 'figure'),
              Input('interval-component', 'n_intervals'))
def UpdatePlaceData(n):
    return create_location_graph()


@app.callback(Output('Pokemon-Map', 'figure'),
              Input('interval-component', 'n_intervals'))
def UpdateMapData(n):
    return create_map()
    
if __name__ == '__main__':
    app.run_server(debug=True)
