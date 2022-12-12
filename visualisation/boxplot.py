import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from visualisation.dashboard_template_functions import calculate_mean_result_by_date, add_figure_rangeslider, \
    filter_bloc_tests
from database.database import request_vertesprong, request_sprint, request_change_of_direction, \
    request_algemene_motoriek, request_bvo
from flask import session
import dash
from dash import html, Input, Output, dcc
import dash_bootstrap_components as dbc


# this list contains the names of all the unique bvo's in the database
BVO_LIST = request_bvo()
META_COLUMNS = ['id', 'bvo_naam', 'seizoen', 'Testdatum', 'reeks_naam', 'team_naam', 'display_name', 'speler_id',
                'geboortedatum', 'Staande_lengte']


#1 van deze 2?
def create_line_graph(dashboard_data, statistics):
    bvo_id = session.get('id')
    print('boxplot:', statistics)
    dashboard_data = pd.DataFrame(dashboard_data)

    measurement_columns = list(set(dashboard_data.columns.values).symmetric_difference(META_COLUMNS))
    measurement = sorted([col for col in measurement_columns if any(x in col for x in ['beste', 'totaal'])])

    # This has got to go
    mean = calculate_mean_result_by_date(dashboard_data, measurement)
    club = calculate_mean_result_by_date(dashboard_data[dashboard_data['bvo_naam'] == bvo_id],
                                             measurement)

    bundled_df: list[pd.DataFrame] = [club, mean]

    fig = go.Figure()
    for df in bundled_df:
        x = df.index
        for column in measurement:
            y = df[column]
            column_name = column.replace('_', ' ')
            bvo_name = df['bvo_naam'].values[0]
            name = f'{bvo_name} - {column_name}'
            fig.add_trace(go.box(x=x, y=y, name=name))

    fig.update_layout(
        yaxis_title='gemiddelde scores',
        xaxis_title='seizoen',
        legend_title="Boxplot",
        title_x=0.5
    )
    return fig


#def create_line_graph(dataframe: pd.DataFrame) -> go.scatter:
#    dataframe = dataframe.groupby("seizoen").mean(numeric_only=True).reset_index()

    #fig = go.Figure()
    #fig.add_trace(go.Scatter(
    #    x=dataframe['seizoen'],
    #    y=dataframe["gemiddelde scores"],
    #    name="Boxplot",
    #    line=dict(),
    #))

    #fig.update_layout(title_text="Boxplot", width=1400, height=700)
    #fig.update_layout(yaxis_title="gemiddelde scores")
    #fig.update_layout(xaxis_title="seizoen")

    #return fig


#def create_box(dataframe: pd.DataFrame) -> go.box:
    #dataframe.sort_values(['team_naam'], inplace=True)

    #fig = go.Figure()
    #fig.add_trace(go.Box(
        #x=dataframe['seizoen'],
        #y=dataframe['gemiddelde scores'],
        #name="Boxplot",
        #boxpoints='all',
    #))

    # fig.show()
    #return fig
