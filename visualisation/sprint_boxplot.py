import pandas as pd
import plotly.graph_objects as go


def create_boxplot_function(individuen, dataframe: pd.DataFrame) -> go.box:
    dataframe.sort_values(['team_naam'], inplace=True)

    df_median = dataframe.groupby("team_naam").median(numeric_only=True).reset_index()
    df_median.sort_values(['team_naam'], inplace=True)

    fig = go.Figure()
    fig.add_trace(go.Box(
        x=dataframe['team_naam'],
        y=dataframe['X10_meter_sprint_beste'],
        name="10 meter sprint",
        boxpoints=individuen,
        line=dict(),
    ))
    fig.add_trace(go.Box(
        x=dataframe['team_naam'],
        y=dataframe['X20_meter_sprint_beste'],
        name="20 meter sprint",
        boxpoints=individuen,
        line=dict(),
    ))
    fig.add_trace(go.Box(
        x=dataframe['team_naam'],
        y=dataframe['X30_meter_sprint_beste'],
        name="30 meter sprint",
        boxpoints=individuen,
        line=dict(),
    ))
    fig.add_trace(go.Scatter(
        x=df_median['team_naam'],
        y=df_median['X10_meter_sprint_beste'],
        name="10 meter sprint mediaan",
        mode="markers",
        marker=dict(size=80, symbol="line-ew", line=dict(width=2, color="red"))
    ))
    fig.add_trace(go.Scatter(
        x=df_median['team_naam'],
        y=df_median['X20_meter_sprint_beste'],
        name="20 meter sprint mediaan",
        mode="markers",
        marker=dict(size=80, symbol="line-ew", line=dict(width=2, color="red"))
    ))
    fig.add_trace(go.Scatter(
        x=df_median['team_naam'],
        y=df_median['X30_meter_sprint_beste'],
        name="30 meter sprint mediaan",
        fillcolor="white",
        mode="markers",
        marker=dict(size=80, symbol="line-ew", line=dict(width=2, color="red"))
    ))

    fig.update_layout(title_text="Sprint", autosize=False, width=1400, height=2600)

    fig.update_layout(yaxis_title="sprint scores")
    fig.update_layout(xaxis_title="team naam")

    return fig