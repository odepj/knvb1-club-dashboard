import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pymysql
from regex import F
from sqlalchemy import create_engine

#oege database connectie
connect_args={'ssl':{'fake_flag_to_enable_tls': True}}
connect_string = 'mysql+pymysql://{}:{}@{}/{}'.format('tiggele', 'h05$rzZA$.I3084I', 'oege.ie.hva.nl', 'ztiggele')
connector = create_engine(connect_string,connect_args=connect_args) 

#Tabellen ophalen uit SQL
sql_a = pd.read_sql(
    "SELECT speler_code, club_code, Balance_Beam_6cm, Balance_Beam_4_5cm, Balance_Beam_3cm, Balance_beam_totaal, meting,  team_naam FROM `han`",
    con=connector,
)

df = sql_a

fig = go.Figure()
#grafiek evenwichtsbalk gekozen team 3cm boxplot
fig.add_trace(go.Box(
    x=df['team_naam'], 
    y=df['Balance_Beam_3cm'],
    name="Team meting 3cm ",
    boxpoints=False, 
    marker_color='rgb(0,204,255)',
    line_color='rgb(0,204,255)'  
))

#benchmarkgrafiek evenwichtsbalk 3cm boxplot
fig.add_trace(go.Box(
    x=df['team_naam'], 
    y=df['Balance_Beam_3cm'],
    name="Benchmark meting 3cm",
    boxpoints=False,
    marker_color='rgb(255,51,51)',
    line_color='rgb(255,51,51)'  
))

#grafiek evenwichtsbalk gekozen team 4.5cm boxplot
fig.add_trace(go.Box(
    x=df['team_naam'],
    y=df['Balance_Beam_4_5cm'],
    name="Team meting 4.5cm",
    boxpoints=False, # no data points
    marker_color='rgb(51,153,255)',
    line_color='rgb(51,153,255)'
))

#benchmark grafiek evenwichtsbalk 4.5cm boxplot
fig.add_trace(go.Box(
    x=df['team_naam'],
    y=df['Balance_Beam_4_5cm'],
    name="Benchmark meting 4.5cm",
    boxpoints=False, # no data points
    marker_color='rgb(51,153,255)',
    line_color='rgb(255,0,0)'
))

#grafiek evenwichtsbalk gekozen team 6cm
fig.add_trace(go.Box(
    x=df['team_naam'],
    y=df['Balance_Beam_6cm'],
    name="Team meting 6cm",
    boxpoints=False, # no data points
    marker_color='rgb(0,0,255)',
    line_color='rgb(0,0,255)'
))

#benchmarkgrafiek evenwichtsbalk 6cm
fig.add_trace(go.Box(
    x=df['team_naam'],
    y=df['Balance_Beam_6cm'],
    name="Benchmark meting 6cm",
    boxpoints=False, # no data points
    marker_color='rgb(0,0,255)',
    line_color='rgb(204,0,0)'
))

#Totale teammeting van alle 3 de afstanden van de evenwichtbalk boxplot 
fig.add_trace(go.Box(
    x=df['team_naam'],
    y=df['Balance_beam_totaal'], 
    name="Totale score",
    boxpoints='suspectedoutliers', # only suspected outliers
    marker=dict(
        color='rgb(8,81,156)',
        outliercolor='rgba(8, 81, 156, 0.6)',
        line=dict(
            outliercolor='rgba(8, 8, 156, 0.6)',
            outlierwidth=2)),
    line_color='rgb(22,173,210)'
))

#Totale benchmarkmeting van de evenwichtbalk
fig.add_trace(go.Box(
    x=df['team_naam'],
    y=df['Balance_beam_totaal'],
    name="Totale benchmark score",
    boxpoints=False, # no data points
    marker_color='rgb(0,0,255)',
    line_color='rgb(204,0,0)'
))

#gegroepeerd en de juiste titel
fig.update_layout(
    title_text="Evenwichtsbalk",
    boxmode='group'
)

fig.show()
