import dash
from dash import html, Input, Output, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import regex as re
from database.database import request_vertesprong, request_sprint, request_change_of_direction, \
    request_algemene_motoriek
from flask import session
from visualisation import algemene_motoriek_chart

import plotly.graph_objs as go

from visualisation.util_functions import calculate_mean_result_by_date, add_figure_rangeslider


# This method is used by the app.py to initialize the Dash dashboard in Flask
# This workaround allows us to use Dash inside a Flask app by using its own route
def init_dashboard_template(server):
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix="/dashboard/dash/dashboard_template/",
        external_stylesheets=[dbc.themes.BOOTSTRAP]
    )

    # All the filter dropdown menu's are put in this 'filters' variable below
    filters = dbc.Card([
        dbc.CardHeader("Filters", class_name="text-center fw-bold",
                       style={"background-color": "#FF9900"}),
        dbc.CardBody(
            [
                # Team selection dropdown
                # TODO: dynamic options based on given dashboard_data
                dcc.Dropdown(
                    ["Onder 13", "Onder 14"],
                    id="teams",
                    placeholder="Teams",
                    className="mb-2"),

                # Lichting selection dropdown
                # TODO: dynamic options based on given dashboard_data
                dcc.Dropdown(
                    ["Lichting 2001", "Lichting 2004"],
                    id="lichting",
                    placeholder="Lichting",
                    className="mb-2"),

                # Seizoen selection dropdown
                # TODO: dynamic options based on the given dashboard_data
                dcc.Dropdown(
                    ["'21/'22 najaar", "'22/'23 voorjaar"],
                    id="seizoen",
                    placeholder="Seizoen",
                ),
            ]
        ),
    ], class_name="mb-4")

    # All the statistiek dropdown menu's are put in this 'statistics' variable below
    statistics = dbc.Card([
        dbc.CardHeader("Statistiek", class_name="text-center fw-bold",
                       style={"background-color": "#FF9900"}),
        dbc.CardBody(
            [dbc.Checklist(
                id="statistics",
                options=[
                    {"label": "Gemiddelde", "value": 0},
                    {"label": "Mediaan", "value": 1},
                    {"label": "Boxplot", "value": 2},
                    {"label": "Individuen", "value": 3},
                ],

                label_checked_style={"color": "green"},
                input_style={"backgroundColor": "red"},
                input_checked_style={
                    "backgroundColor": "green",
                    "borderColor": "#green",
                },
            ),
            ],
        ),
    ], class_name="mb-4")

    # The benchmark dropdown menu is put in this 'benchmark' variable below
    benchmark = dbc.Card([
        dbc.CardHeader("Benchmark", class_name="text-center fw-bold",
                       style={"background-color": "#FF9900"}),
        dbc.CardBody(
            [  # Seizoen selection dropdown
                # TODO: dynamic options based on the given dashboard_data
                dcc.Dropdown(
                    ["FC Volendam", "Ajax"],
                    id="bvo",
                    placeholder="BVO's",
                ), ],
        ),
    ])

    # All the layout items such as the dashboard's charts itself are put in this 'layout' variable below
    dash_app.layout = dbc.Container(
        [
            # get the current selected url and store the selected dashboard in a dcc.Store object
            dcc.Location(id="url", refresh=True),
            dcc.Store(id='selected_dashboard'),
            dcc.Store(id='dashboard_data'),

            dbc.Row(
                [
                    dbc.Col([html.Div(id="bloc_test_selection"), filters, statistics, benchmark],
                            width=2, style={"height": "10rem"}),
                    dbc.Col(dcc.Graph(id="boxplot", responsive=True), width=10),
                ],
                class_name="align-items-stretch"),

            dbc.Row(
                [
                    dbc.Col(dcc.Graph(id="line_chart",
                                      responsive=True), width=10),
                ],
                class_name="justify-content-end"
            ),

            dbc.Row(
                [
                    dbc.Col(html.Div(id="algemene_motoriek_graph"), width=10),
                ],
                class_name="justify-content-end"
            ),
        ], fluid=True)

    # Callbacks for the Dash dashboard are initilized here after the creation of the layout has been completed
    init_callbacks(dash_app)

    return dash_app.server


# This method is used to create and initialize callbacks that will be used by the charts or selection items
def init_callbacks(dash_app):
    # This callback is used to dynamically return the current selected dashboard from the url
    @dash_app.callback(
        Output('selected_dashboard', 'children'),
        [Input('url', 'pathname')])
    def get_selected_dashboard(pathname) -> str:
        return re.sub(r'^.+/([^/]+)$', r'\1', pathname)

    @dash_app.callback(
        Output('dashboard_data', 'children'),
        [Input('selected_dashboard', 'children')])
    def get_dashboard_data(selected_dashboard) -> dict:
        bvo_id = session.get('id')

        if selected_dashboard == "verspringen":
            return request_vertesprong(bvo_id).to_dict(orient='records')
        elif selected_dashboard == "sprint":
            return request_sprint(bvo_id).to_dict(orient='records')
        elif selected_dashboard == "cod":
            return request_change_of_direction(bvo_id).to_dict(orient='records')
        elif selected_dashboard == "algemene_motoriek":
            return request_algemene_motoriek(bvo_id).to_dict(orient='records')
        else:
            return dict()

    # This callback is used to dynamically return the bloc test selection menu
    @dash_app.callback(
        Output('bloc_test_selection', 'children'),
        [Input('selected_dashboard', 'children')])
    def bloc_test_selection(selected_dashboard):
        if selected_dashboard != "algemene_motoriek":
            return None

        return dbc.Card([
            dbc.CardHeader("BLOC-testen", class_name="text-center fw-bold",
                           style={"background-color": "#FF9900"}),
            dbc.CardBody(
                [dbc.Checklist(
                    id="bloc_test_selection",
                    options=[
                        {"label": "Evenwichtsbalk",
                         "value": "Balance_beam_totaal"},
                        {"label": "Zijwaarts springen",
                         "value": "Zijwaarts_springen_totaal"},
                        {"label": "Zijwaarts verplaatsen",
                         "value": "Zijwaarts_verplaatsen_totaal"},
                        {"label": "Hand-oog coördinatie",
                         "value": "Oog_hand_coordinatie_totaal"},
                    ],
                    label_checked_style={"color": "green"},
                    input_style={"backgroundColor": "red"},
                    input_checked_style={
                        "backgroundColor": "green",
                        "borderColor": "#green",
                    },
                ),
                ],
            ),
        ], class_name="mb-4")

    # This callback is used to dynamically return the bloc test chart
    @dash_app.callback(
        Output("algemene_motoriek_graph", "children"),
        [Input("selected_dashboard", "children"), Input("dashboard_data", "children")])
    def create_bloc_test_chart(selected_dashboard, dashboard_data):
        if selected_dashboard != "algemene_motoriek":
            return None

        figure = algemene_motoriek_chart.create_chart(pd.DataFrame(dashboard_data))
        return dcc.Graph(figure=figure, responsive=True)

    # This callback is used to dynamically create a boxplot
    @dash_app.callback(
        Output("boxplot", "figure"),
        [Input("dashboard_data", "children")])
    def create_boxplot(dashboard_data):
        # place code for creating the boxplot here
        # var dashboard data contains a dict of the current dashboard data DataFrame

        # return created plot here as callback output
        return {}

    # This callback is used to dynamically create a line chart
    @dash_app.callback(
        Output("line_chart", "figure"),
        [Input("dashboard_data", "children")]
    )
    def create_line_chart(dashboard_data):
        club_id = session.get('id')
        dashboard_data = pd.DataFrame(dashboard_data)
        #   Dashboard data should contain the measurement(s), datum, club_code and meting.
        #   Mean results are grouped by geboortedatum. Datum will be the df_index for x-axis convenience.
        #   x-axis displays 'meting'
        #   Each measurement column gets its own trace and will be coloured by club_code
        #

        # place code for creating the line chart here
        # var dashboard data contains a dict of the current dashboard data DataFrame
        # mean = calculate_mean_result_by_date(dashboard_data.drop_duplicates())
        # club = calculate_mean_result_by_date(dashboard_data[dashboard_data['club_code'] == club_id].drop_duplicates())

        # bundled_df = [club, mean]

        fig = go.Figure()
        # [fig.add_trace(go.Scatter(x=d.index, y=d.columns, name=d['club_code'].values[0])) for d in bundled_df]
        fig.update_layout(
            yaxis_title='Totaal score (punten)',
            xaxis_title='Datum',
            legend_title="Teams",
            title_x=0.5
        )
        fig = add_figure_rangeslider(fig)
        return fig
