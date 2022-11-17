import dash
import pandas as pd
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from flask import session

from database.database import get_zijwaarts_springen
from visualisation.util_functions import add_figure_rangeslider, calculate_delta, calculate_mean_result_by_date

# Retrieve data from DB.
data = get_zijwaarts_springen()
col = 'Zijwaarts_springen_totaal'
# col = ['Zijwaarts_springen_1', 'Zijwaarts_springen_2','Zijwaarts_springen_totaal']


# This method is used by the app.py to initialize the Dash dashboard in Flask
# This workaround allows us to use Dash inside a Flask app by using its own route
def init_vs_dashboard(server):
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dashboard/dash/zijwaartsspringen/',
        external_stylesheets=[dbc.themes.BOOTSTRAP]
    )

    dash_app.layout = html.Main(id='graph-container')

    # Callbacks for the Dash dashboard are initialized here after the creation of the layout has been completed
    init_callbacks(dash_app)

    return dash_app.server


# This method is used to create and initialize callbacks that will be used by the charts or selection items
def init_callbacks(dash_app):
    @dash_app.callback(Output("graph-container", "children"), Input("graph-container", "loading_state"))
    def build_graph(loading_state):
        print('loading_state:', loading_state)
        club_id = session.get("id")

        mean = calculate_mean_result_by_date(data.drop_duplicates())
        club = calculate_mean_result_by_date(data[data['club_code'] == club_id].drop_duplicates())
        bundled_df = [club, mean]

        fig = go.Figure()
        [fig.add_trace(go.Scatter(x=d.index, y=d[col], name=d['club_code'].values[0])) for d in bundled_df]
        fig.update_layout(yaxis_title='Totaal score (punten)', xaxis_title='Datum',
                          legend_title="Teams", title_x=0.5)
        fig = add_figure_rangeslider(fig)

        graph = dbc.Col(
            id='graph-container', width=10,
            children=[
                dcc.Graph(id='zijwaarts-springen-graph', figure=fig, responsive=True)
            ]
        )

        s, f = mean[col], club[col]
        delta_s = calculate_delta(s, from_=s.iloc[:1].index, to_=s.iloc[-1:].index)
        delta_f = calculate_delta(f, from_=f.iloc[:1].index, to_=f.iloc[-1:].index)
        card = dbc.Card(
            [
                html.H5('Delta verbetering', style={'margin-top': '5px'}),
                html.Span(f'Team {club_id}:'),
                html.Em(f"{delta_f}%"),
                html.Span('Landelijk gemiddelde:'),
                html.Em(f"{delta_s}%"),
            ], className='col-2', id='indicator'
        )

        return dbc.Row([graph, card])

    @dash_app.callback(Output("indicator", "children"),
                       [Input("zijwaarts-springen-graph", "selectedData"),
                        Input("zijwaarts-springen-graph", "relayoutData")]
                       )
    def update_graph(selectedData, relayoutData):
        print('relayoutData:', relayoutData)
        print('selectedData:', selectedData)
        # print('graph_selection:', graph_selection)
        # print('selectedData:', selectedData)

        slider_range = None
        if relayoutData is not None:
            if 'xaxis.range' in relayoutData:
                slider_range = relayoutData['xaxis.range']
                print(slider_range)

        graph_range = selectedData
        if selectedData is not None:
            if 'range' in selectedData is not None:
                graph_range = selectedData['range']['x']
                print(graph_range)
        return [
            html.H5('slider_range:', style={'margin-top': '5px'}),
            html.Em(f"{slider_range}%"),
            html.Span('graph_selection:'),
            html.Em(f"{graph_range}%"),
        ]
