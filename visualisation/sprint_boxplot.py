import pandas as pd
import plotly.graph_objects as go
from visualisation.dashboard_template_functions import get_measurement_columns, rename_column


def create_boxplot_function(individuen, dataframe: pd.DataFrame) -> go.box:
    dataframe.sort_values(['team_naam'], inplace=True)
    selected_columns = get_measurement_columns(dataframe)

    df_median = dataframe.groupby("team_naam").median(numeric_only=True).reset_index()
    df_median.sort_values(['team_naam'], inplace=True)

    fig = go.Figure()
    for column in selected_columns:
        column_name = rename_column(column)

        fig.add_trace(go.Box(
            x=dataframe['team_naam'],
            y=dataframe[column],
            name=column_name,
            boxpoints=individuen,
            line=dict()))

        fig.add_trace(go.Scatter(
        x=df_median['team_naam'],
        y=df_median[column],
        name=f"{column_name} mediaan",
        mode="markers",
        marker=dict(size=80, symbol="line-ew", line=dict(width=2, color="red"))
    ))

    fig.update_layout(title_text="Sprint", autosize=False, width=1400, height=2600)
    fig.update_layout(yaxis_title="sprint scores")
    fig.update_layout(xaxis_title="team naam")

    return fig