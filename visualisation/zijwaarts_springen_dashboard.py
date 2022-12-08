from datetime import datetime

import dash
import pandas as pd
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from flask import session

from database.database import get_zijwaarts_springen
from visualisation.util_functions import add_figure_rangeslider, calculate_delta, calculate_mean_result_by_date, nearest

# Retrieve data from DB.
data = get_zijwaarts_springen()
col = 'Zijwaarts_springen_totaal'
date_range = data['Testdatum'].drop_duplicates().values


# col = ['Zijwaarts_springen_1', 'Zijwaarts_springen_2','Zijwaarts_springen_totaal']


# This method is used by the app.py to initialize the Dash dashboard in Flask
# This workaround allows us to use Dash inside a Flask app by using its own route
def init_vs_dashboard(server):
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dashboard/dash/zijwaartsspringen/',
        external_stylesheets=[dbc.themes.BOOTSTRAP]
    )

    dash_app.layout = html.Main(
        dbc.Row([
            dbc.Col(id='graph-container', width=10,
                    children=[dcc.Graph(id='zijwaarts-springen-graph', responsive=True)]),
            dbc.Card(id='indicator', className='col-2')
        ]))

    # Callbacks for the Dash dashboard are initialized here after the creation of the layout has been completed
    init_callbacks(dash_app)

    return dash_app.server


# This method is used to create and initialize callbacks that will be used by the charts or selection items
def init_callbacks(dash_app):
    @dash_app.callback(Output("zijwaarts-springen-graph", "figure"), Input("graph-container", "loading_state"))
    def build_graph(loading_state):
        club_id = session.get("id")

        mean = calculate_mean_result_by_date(data.drop_duplicates())
        club = calculate_mean_result_by_date(data[data['bvo_naam'] == club_id].drop_duplicates())
        bundled_df = [club, mean]

        fig = go.Figure()
        [fig.add_trace(go.Scatter(x=d.index, y=d[col], name=d['bvo_naam'].values[0])) for d in bundled_df]
        fig.update_layout(yaxis_title='Totaal score (punten)', xaxis_title='Datum',
                          legend_title="Teams", title_x=0.5)
        fig = add_figure_rangeslider(fig)
        return fig

    @dash_app.callback(Output("indicator", "children"),
                       [Input("zijwaarts-springen-graph", "selectedData"),
                        Input("zijwaarts-springen-graph", "relayoutData")]
                       )
    def update_graph(selectedData, relayoutData):
        # selectedData['range']['x']
        club_id = session.get("id")

        mean = calculate_mean_result_by_date(data.drop_duplicates())
        club = calculate_mean_result_by_date(data[data['bvo_naam'] == club_id].drop_duplicates())
        s, f = mean[col], club[col]

        if relayoutData is not None and 'xaxis.range' in relayoutData:
            x_left, x_right = [nearest(date_range, datetime.strptime(entry.split(' ')[0], '%Y-%m-%d').date()) for entry
                               in relayoutData['xaxis.range']]
            df_left, df_right = pd.DataFrame([], index=[x_left]), pd.DataFrame([], index=[x_right])
            delta_s = calculate_delta(s, from_=df_left.iloc[-1:].index, to_=df_right.iloc[-1:].index)
            delta_f = calculate_delta(f, from_=df_left.iloc[-1:].index, to_=df_right.iloc[-1:].index)
            return [
                html.H5('Delta verbetering', style={'margin-top': '5px'}),
                html.Span(f'Van - tot:'),
                html.Em(f"{x_left} - {x_right}"),
                html.Span(f'Team {club_id}:'),
                html.Em(f"{delta_f}%"),
                html.Span('Landelijk gemiddelde:'),
                html.Em(f"{delta_s}%"),
            ]

        delta_s = calculate_delta(s, from_=s.iloc[:1].index, to_=s.iloc[-1:].index)
        delta_f = calculate_delta(f, from_=f.iloc[:1].index, to_=f.iloc[-1:].index)

        return [
            html.H5('Delta verbetering', style={'margin-top': '5px'}),
            html.Span(f'Van - tot:'),
            html.Em(f"2013-10-05 - 2018-04-05"),  # Komt later wel, brein is kaduuk
            html.Span(f'Team {club_id}:'),
            html.Em(f"{delta_f}%"),
            html.Span('Landelijk gemiddelde:'),
            html.Em(f"{delta_s}%"),
        ]
