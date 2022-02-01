
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pyodbc 
# import pymssql
# geopandas causes problems with dependencies. Installed in geo_env but can't get pymssql to work to.
import geopandas

import config

def update_data():
    try:
        conn_str = ("Driver={SQL Server};"
                    "Server=" + config.server + ";"
                    "Database=" + config.database + ";"
                    "UID=" + config.user + ";"
                    "PWD=" + config.password + ";")
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        df = pd.io.sql.read_sql("SELECT * from pokemondarrellgerber", conn)
        return 0, df
    except Exception as e:
        print(e)
        return -1, None
    

def create_name_graph():
    result, df = update_data()
    if(result == 0):
        df2 = df['pokename'].value_counts().head(10)
        fig = px.bar(df2)
        return fig
    else:
        return None
    
def create_location_graph():
    result, df = update_data()
    if(result == 0):
        df2 = df['placename'].value_counts().head(10)
        fig = px.bar(df2)
        return fig
    else:
        return None   
    

def create_location_map():
    result, df = update_data()
    print(df.shape)
    print(df.columns)
    if(result == 0):
        geoDF = geopandas.GeoDataFrame(
            df, geometry=geopandas.points_from_xy(df.long, df.lat))
        print(geoDF.shape)
        print(geoDF.head())
        fig = geoDF.plot()
        return fig
    else:
        return None
    
app = dash.Dash(__name__)
    
app.layout = html.Div(children = [
    html.H1(children='Pokemon Around the World'),
    
    dcc.Graph(
        id='Pokemon-Names',
        figure = create_name_graph()
    ),
    dcc.Graph(
        id='Pokemon-Places',
        figure=create_location_graph()
    ),
    dcc.Graph(
        id='Pokemon-map',
        figure=create_location_map()
    ),
    dcc.Interval(
        id='interval-component',
        interval = 300*1000,
        n_intervals = 0
    )
])    

@app.callback(Output('Pokemon-Names', 'figure'), 
              Input('interval-component', 'n_intervals'))
def UpdateNameData(n):
    result, df = update_data()
    if(result == 0):
        df2 = df['pokename'].value_counts().head(10)
        fig = px.bar(df2)
        return fig
    else:
        return None


@app.callback(Output('Pokemon-Places', 'figure'),
              Input('interval-component', 'n_intervals'))
def UpdatePlaceData(n):
    result, df = update_data()
    if(result == 0):
        df2 = df['placename'].value_counts().head(10)
        fig = px.bar(df2)
        return fig
    else:
        return None
    

@app.callback(Output('Pokemon-map', 'figure'),
              Input('interval-component', 'n_intervals'))
def UpdateMapData(n):
    result, df = update_data()
    if(result == 0):
        geoDF = geopandas.GeoDataFrame(
            df, geometry=geopandas.points_from_xy(df.long, df.lat))
        print(geoDF.shape)
        print(geoDF.head())
        fig = geoDF.plot()
        return fig
    else:
        return None

if __name__ == '__main__':
    app.run_server(debug=True)
