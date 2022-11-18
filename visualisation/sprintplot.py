def sprint(data):
    # Libary imports
    from plotly.subplots import make_subplots
    import plotly.graph_objects as go
    import pandas as pd
    from plotly.utils import PlotlyJSONEncoder
    import json

    # Load the dataset from SQL Database
    df = data.groupby("team_naam").mean(numeric_only=True).reset_index()
    df.rename(columns={0: 'speler_code', 1: 'club_code', 2: 'X10_meter_sprint_beste', 3: 'X20_meter_sprint_beste', 4: 'X30_meter_sprint_beste', 5: 'team_naam'},
              inplace=True)

    # Initialize figure with subplots
    fig = make_subplots(rows=2, cols=2, x_title="Leeftijdscategorie")
    fig = make_subplots(rows=2, cols=2, x_title="Leeftijdscategorie", subplot_titles=("Tijd in seconden 10 meter sprint", "Tijd in seconden 20 meter sprint",
                        "Tijd in seconden 30 meter sprint", "Gemiddelde tijd in seconden 10,20 en 30 meter sprint <br> per leeftijdscategorie"))

    # Plots for 10,20 and 30 meter sprint grouped by age under 13,14,15,16 and 17 Years
    fig.add_trace(go.Scatter(x=df['team_naam'], y=df["X10_meter_sprint_beste"],
                  name="10 meter sprint per Leeftijdscategorie", line_color='rgb(220,20,60)'), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['team_naam'], y=df["X20_meter_sprint_beste"],
                  name="20 meter sprint per Leeftijdscategorie", line_color='rgb(20,20,20)'), row=1, col=2)
    fig.add_trace(go.Scatter(x=df['team_naam'], y=df["X30_meter_sprint_beste"],
                  name="30 meter sprint per Leeftijdscategorie", line_color='rgb(34,139,34)'), row=2, col=1)

    # Plots Total 10,20 and 30 meter sprint for Under 13,14,15,16 and 17 Years
    fig.add_trace(go.Scatter(x=df['team_naam'], y=df['X10_meter_sprint_beste'],
                  name="10 meter sprint totaal", line_color='rgb(220,20,60)'), row=2, col=2)
    fig.add_trace(go.Scatter(x=df['team_naam'], y=df['X20_meter_sprint_beste'],
                  name="20 meter sprint totaal", line_color='rgb(20,20,20)'), row=2, col=2)
    fig.add_trace(go.Scatter(x=df['team_naam'], y=df['X30_meter_sprint_beste'],
                  name="30 meter sprint totaal", line_color='rgb(34,139,34)'), row=2, col=2)

    # Update title and return plot
    fig.update_layout(title_text='Meting 10,20 en 30 meter sprint',
                      title_x=0.5, width=1200, height=700)

    return json.dumps(fig, cls=PlotlyJSONEncoder)
