import pandas as pd
import plotly.graph_objects as go
import plotly.express as pl
from visualisation.dashboard_template_functions import get_measurement_columns, rename_column, drop_mean_and_median_columns


def create_box(individuen, dataframe: pd.DataFrame) -> go.box:
    dataframe.sort_values(['team_naam'], inplace=True)
    extra_columns = dataframe.filter(regex='.mediaan|.gemiddelde').columns.values
    selected_columns = dataframe[get_measurement_columns(dataframe)]
    selected_columns = drop_mean_and_median_columns(selected_columns)

    fig = go.Figure()
    for column in selected_columns:
        column_name = rename_column(column)

        fig.add_trace(go.Box(
            x=dataframe['team_naam'],
            y=dataframe[column],
            name=column_name,
            boxpoints=individuen,
            line=dict(),
            showlegend=True
    ))

    for extra_column in extra_columns:
        column_name = rename_column(extra_column)
        fig.add_trace(go.Scatter(
        x=dataframe['team_naam'],
        y=dataframe[extra_column],
        name=column_name,
        mode="markers",
        showlegend=True,
        marker=dict(size=80, symbol="line-ew", line=dict(width=2, color="red"))))

    fig.update_layout(title_text="<b>Vergelijking van teams<b>", autosize=True)
    fig.update_layout(yaxis_title="Beste van totaal resultaat")
    fig.update_layout(xaxis_title="team naam")

    return fig