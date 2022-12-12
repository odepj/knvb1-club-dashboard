import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def create_line_graph(dataframe: pd.DataFrame) -> go.scatter:
    dataframe = dataframe.groupby("seizoen").mean(numeric_only=True).reset_index()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dataframe['seizoen'],
        y=dataframe["X10_meter_sprint_beste"],
        name="gemiddelde 10 meter",
        line=dict(),
    ))
    fig.add_trace(go.Scatter(
        x=dataframe['seizoen'],
        y=dataframe["X20_meter_sprint_beste"],
        name="gemiddelde 20 meter",
        line=dict(),
    ))
    fig.add_trace(go.Scatter(
        x=dataframe['seizoen'],
        y=dataframe["X30_meter_sprint_beste"],
        name="gemiddelde 30 meter",
        line=dict(),
    ))

    fig.update_layout(title_text="Sprint", width=1400, height=700)
    fig.update_layout(yaxis_title="gemiddelde sprint scores")
    fig.update_layout(xaxis_title="seizoen")

    return fig


def create_box(dataframe: pd.DataFrame) -> go.box:
    dataframe.sort_values(['team_naam'], inplace=True)

    fig = go.Figure()
    fig.add_trace(go.Box(
        x=dataframe['team_naam'],
        y=dataframe['X10_meter_sprint_beste'],
        name="10 meter sprint",
        boxpoints='all',
    ))
    fig.add_trace(go.Box(
        x=dataframe['team_naam'],
        y=dataframe['X20_meter_sprint_beste'],
        name="20 meter sprint",
        boxpoints='all',
    ))
    fig.add_trace(go.Box(
        x=dataframe['team_naam'],
        y=dataframe['X30_meter_sprint_beste'],
        name="30 meter sprint",
        boxpoints='all',
    ))


    # fig = px.box(dataframe, x='team_naam', y='X10_meter_sprint_beste', points="all")
    fig.update_layout(title_text="Sprint", width=1400, height=700)
    fig.update_layout(yaxis_title="sprint scores")
    fig.update_layout(xaxis_title="team naam")
    # fig.show()
    return fig
