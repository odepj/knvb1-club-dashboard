from plotly.subplots import make_subplots
import pandas as pd
import plotly.graph_objects as go
from plotly.utils import PlotlyJSONEncoder
import json


def change_of_direction(data):

    df = pd.DataFrame(data)
    mean_df = df.groupby("team_naam").mean(numeric_only=True).reset_index()

    fig = make_subplots(rows=3, cols=3, subplot_titles=
    ('Links 1', 'Links 2',
     'Links Beste', 'Rechts 1',
     'Rechts 2', 'Rechts beste',
     '', 'Verschil gemiddelde'))

    fig.add_trace(go.Box(
        x=df['team_naam'],
        y=df['CoD_links_1'],
        name="Links-1",
        boxpoints='all',
        marker_color='rgb(0, 0, 0)',
        line_color='rgb(0, 0, 0)'
    ), row=1, col=1)
    fig.add_trace(go.Box(
        x=df['team_naam'],
        y=df['CoD_links_2'],
        name="Links-2",
        boxpoints='all',
        marker_color='rgb(33, 34, 79)',
        line_color='rgb(33, 34, 79)'
    ), row=1, col=2)
    fig.add_trace(go.Box(
        x=df['team_naam'],
        y=df['CoD_links_beste'],
        name="Links-beste",
        boxpoints='all',
        marker_color='rgb(101, 104, 105)',
        line_color='rgb(101, 104, 105)'
    ), row=1, col=3)
    fig.add_trace(go.Box(
        x=df['team_naam'],
        y=df['CoD_rechts_1'],
        name="Rechts_1",
        boxpoints='all',
        marker_color='rgb(88, 69, 107)',
        line_color='rgb(88, 69, 107)'
    ), row=2, col=1)
    fig.add_trace(go.Box(
        x=df['team_naam'],
        y=df['CoD_rechts_2'],
        name="Rechts_2",
        boxpoints='all',
        marker_color='rgb(46, 43, 117)',
        line_color='rgb(46, 43, 117)'
    ), row=2, col=2)
    fig.add_trace(go.Box(
        x=df['team_naam'],
        y=df['CoD_rechts_beste'],
        name="Rechts_beste",
        boxpoints='all',
        marker_color='rgb(82, 119, 125)',
        line_color='rgb(82, 119, 125)'
    ), row=2, col=3)
    fig.add_trace(go.Scatter(
        x=mean_df['team_naam'],
        y=mean_df["CoD_links_1"],
        name="gemiddelde links 1",
        line=dict(color="#F11C12"),
    ), row=3, col=2)
    fig.add_trace(go.Scatter(
        x=mean_df['team_naam'],
        y=mean_df["CoD_links_2"],
        name="gemiddelde links 2",
        line=dict(color="#1923CF"),
    ), row=3, col=2)
    fig.add_trace(go.Scatter(
        x=mean_df['team_naam'],
        y=mean_df["CoD_links_beste"],
        name="gemiddelde links beste",
        line=dict(color="#FD00D4"),
    ), row=3, col=2)

    fig.update_layout(title_text="Change of Direction", width=1400, height=700)
    fig.update_layout(yaxis_title="Change of Direction Score")
    return json.dumps(fig, cls=PlotlyJSONEncoder)
