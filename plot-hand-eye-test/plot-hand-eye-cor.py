import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pymysql
from sqlalchemy import create_engine

connect_args={'ssl':{'fake_flag_to_enable_tls': True}}
connect_string = 'mysql+pymysql://{}:{}@{}/{}'.format('tiggele', 'h05$rzZA$.I3084I', 'oege.ie.hva.nl', 'ztiggele')
connector = create_engine(connect_string,connect_args=connect_args) 

sql_a = pd.read_sql(
    "SELECT speler_code, Oog_hand_coordinatie_Totaal, Oog_hand_coordinatie_1, Oog_hand_coordinatie_2,  team_naam FROM `han`",
    con=connector,
)

df = sql_a

fig = go.Figure()
fig.add_trace(go.Box(
    x=df['team_naam'],
    y=df['Oog_hand_coordinatie_1'],
    z=df['speler_code'],
    name="Oog hand coordinatie 1ste meting",
    jitter=0.3,
    pointpos=-1.8,
    boxpoints='all', # represent all points
    marker_color='rgb(7,40,89)',
    line_color='rgb(7,40,89)'
))

fig.add_trace(go.Box(
    x=df['team_naam'],
    y=df['Oog_hand_coordinatie_2'],
    name="Oog hand coordinatie 2de meting",
    boxpoints=False, # no data points
    marker_color='rgb(9,56,125)',
    line_color='rgb(9,56,125)'
))

fig.add_trace(go.Box(
    x=df['team_naam'],
    y=df['Oog_hand_coordinatie_Totaal'], 
    name="Oog hand coordinatie Totaal",
    boxpoints='suspectedoutliers', # only suspected outliers
    marker=dict(
        color='rgb(8,81,156)',
        outliercolor='rgba(219, 64, 82, 0.6)',
        line=dict(
            outliercolor='rgba(219, 64, 82, 0.6)',
            outlierwidth=2)),
    line_color='rgb(8,81,156)'
))

fig.update_layout(title_text="Hand-oog coördinatie")
fig.show()