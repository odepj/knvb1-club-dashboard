import dash
from dash import html, Input, Output, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import regex as re
from database.database import request_vertesprong, request_sprint, request_change_of_direction, request_algemene_motoriek
from functools import reduce
from flask import session


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
    ])

    # All the statistiek dropdown menu's are put in this 'statistics' variable below
    statistics = dbc.Card([
        dbc.CardHeader("Statistiek", class_name="text-center fw-bold",
                       style={"background-color": "#FF9900"}),
        dbc.CardBody(
            [dbc.Checklist(
                id="statistics",
                options=[
                    {"label": "Gemiddelde", "value": 1},
                    {"label": "Mediaan", "value": 2},
                    {"label": "Boxplot", "value": 3},
                    {"label": "Individuen", "value": 4},
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
    ])

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
                    dbc.Col(filters, width=2),
                    dbc.Col(dcc.Graph(id="boxplot", responsive=True), width=10),
                ],
                class_name="align-items-stretch"),

            dbc.Row(
                [
                    dbc.Col(statistics, width=2),
                    dbc.Col(dcc.Graph(id="line_chart",
                            responsive=True), width=10),
                ],
            ),

            dbc.Row(
                [
                    dbc.Col(benchmark, width=2),
                ],
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
        [Input("dashboard_data", "children")])
    def create_line_chart(dashboard_data):
        # place code for creating the line chart here
        # var dashboard data contains a dict of the current dashboard data DataFrame

        # return created chart here as callback output
        return {}
