def hand_oog_coordinatie(data):
    import pandas as pd
    import plotly.graph_objects as go
    from plotly.utils import PlotlyJSONEncoder
    import json

    df = data
    df.rename(columns={0: 'Oog_hand_coordinatie_totaal', 1: 'Oog_hand_coordinatie_1', 2: 'Oog_hand_coordinatie_2', 3: 'team_naam'},
              inplace=True)

    fig = go.Figure()
    fig.add_trace(go.Box(
    x=df['team_naam'],
    y=df['Oog_hand_coordinatie_1'],
    name="Oog hand coordinatie 1ste meting",
    #jitter=0.3,
    #pointpos=-1.8,
    boxpoints='all', # represent all points
    marker_color='rgb(7,40,89)',
    line_color='rgb(151,255,255)'
    ))

    fig.add_trace(go.Box(
    x=df['team_naam'],
    y=df['Oog_hand_coordinatie_2'],
    name="Oog hand coordinatie 2de meting",
    boxpoints='all', # represent all points
    marker_color='rgb(9,56,125)',
    line_color='rgb(20,20,20)'
    ))

    fig.add_trace(go.Box(
    x=df['team_naam'],
    y=df['Oog_hand_coordinatie_totaal'], 
    name="Oog hand coordinatie Totaal",
    boxpoints='all', # represent all points
    marker_color='rgb(9,56,125)',
    line_color='rgb(255,128,0)'
    ))

    fig.update_layout(title_text="Hand-oog coördinatie", width=1000, height=600)
    fig.update_layout(xaxis_title="Leeftijdscategorie", yaxis_title="Score Hand-oog coördinatie meting")

    return json.dumps(fig, cls=PlotlyJSONEncoder)
    