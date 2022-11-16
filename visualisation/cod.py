from plotly.subplots import make_subplots


def change_of_direction(data):
    import pandas as pd
    import plotly.graph_objects as go
    from plotly.utils import PlotlyJSONEncoder
    import json

    df = pd.DataFrame(data)

    data1_13 = df.query('team_naam =="Onder 13"')['CoD_links_1'].mean()
    data2_13 = df.query('team_naam =="Onder 13"')['CoD_links_2'].mean()
    data3_13 = df.query('team_naam =="Onder 13"')['CoD_links_beste'].mean()

    data1_14 = df.query('team_naam =="Onder 14"')['CoD_links_1'].mean()
    data2_14 = df.query('team_naam =="Onder 14"')['CoD_links_2'].mean()
    data3_14 = df.query('team_naam =="Onder 14"')['CoD_links_beste'].mean()

    data1_15 = df.query('team_naam =="Onder 15"')['CoD_links_1'].mean()
    data2_15 = df.query('team_naam =="Onder 15"')['CoD_links_2'].mean()
    data3_15 = df.query('team_naam =="Onder 15"')['CoD_links_beste'].mean()

    data1_16 = df.query('team_naam =="Onder 16"')['CoD_links_1'].mean()
    data2_16 = df.query('team_naam =="Onder 16"')['CoD_links_2'].mean()
    data3_16 = df.query('team_naam =="Onder 16"')['CoD_links_beste'].mean()

    data1_17 = df.query('team_naam =="Onder 17"')['CoD_links_1'].mean()
    data2_17 = df.query('team_naam =="Onder 17"')['CoD_links_2'].mean()
    data3_17 = df.query('team_naam =="Onder 17"')['CoD_links_beste'].mean()

    mean_data = [["Onder 13", data1_13, data2_13, data3_13],
                 ["Onder 14", data1_14, data2_14, data3_14],
                 ["Onder 15", data1_15, data2_15, data3_15],
                 ["Onder 16", data1_16, data2_16, data3_16],
                 ["Onder 17", data1_17, data2_17, data3_17]]

    mean_df = pd.DataFrame(mean_data, columns=["team_naam", "CoD_links_1", "CoD_links_2", "CoD_links_beste"])

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
