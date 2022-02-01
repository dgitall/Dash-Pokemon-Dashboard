
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pymssql

import config

def update_data():
    try:
        conn = pymssql.connect(config.server, config.user,
                            config.password, config.database)
        df = pd.read_sql("SELECT * from pokemondarrellgerber", conn)
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
    
if __name__ == '__main__':
    app.run_server(debug=True)
