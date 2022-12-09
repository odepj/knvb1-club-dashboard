import dash
from dash import html, Input, Output, dcc
import dash_bootstrap_components as dbc
import datetime as dt
import pandas as pd
import regex as re
from database.database import request_vertesprong, request_sprint, request_change_of_direction, request_algemene_motoriek, request_bvo
from flask import session
from visualisation import algemene_motoriek_chart

# this list contains the names of all the unique bvo's in the database
bvo_list = request_bvo()

# This dictionary will be used to lookup BLOC-test specific rows
columns = {"Evenwichtsbalk": ["Balance_Beam_3cm", "Balance_Beam_4_5cm", "Balance_Beam_6cm", "Balance_beam_totaal"], 
        "Zijwaarts springen": ["Zijwaarts_springen_1", "Zijwaarts_springen_2", "Zijwaarts_springen_totaal"],
        "Zijwaarts verplaatsen": ["Zijwaarts_verplaatsen_1", "Zijwaarts_verplaatsen_2", "Zijwaarts_verplaatsen_totaal"],
        "Hand-oog coördinatie": ["Oog_hand_coordinatie_1", "Oog_hand_coordinatie_2", "Oog_hand_coordinatie_totaal"]}


# This method is used by the app.py to initialize the Dash dashboard in Flask
# This workaround allows us to use Dash inside a Flask app by using its own route
def init_dashboard_template(server):
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix="/dashboard/dash/dashboard_template/",
        external_stylesheets=[dbc.themes.BOOTSTRAP]
    )

     # The benchmark dropdown menu is put in this 'benchmark' variable below
    benchmark = dbc.Card([
        dbc.CardHeader("Benchmark", class_name="text-center fw-bold",
                       style={"background-color": "#FF9900"}),
        dbc.CardBody(
            [  # Benchmark selection dropdown
                dcc.Dropdown(
                    placeholder="BVO's",
                    options=bvo_list["display_name"],
                    id="bvo",
                ), ],
        ),
    ])

    statistics = dbc.Card([
            dbc.CardHeader("Statistiek", class_name="text-center fw-bold",
                           style={"background-color": "#FF9900"}),
            dbc.CardBody(
                [dbc.Checklist(
                    id="statistics",
                    options=[
                        {"label": "Gemiddelde", "value": "gemiddelde"},
                        {"label": "Mediaan", "value": "mediaan"},
                        {"label": "Boxplot", "value": "boxplot"},
                        {"label": "Individuen", "value": "individuen"},
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

    # All the layout items such as the dashboard's charts itself are put in this 'layout' variable below
    dash_app.layout = dbc.Container(
        [
            # get the current selected url and store the selected dashboard in a dcc.Store object
            dcc.Location(id="url", refresh=True),
            dcc.Store(id='selected_dashboard'),
            dcc.Store(id='dashboard_data'),
            dcc.Store(id='filter_output'),

            dbc.Row(
                [
                    dbc.Col([html.Div(id="bloc_test_selection"), html.Div(id="filter_selection"), statistics, benchmark],
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
                            "value": "Evenwichtsbalk"},
                        {"label": "Zijwaarts springen",
                         "value": "Zijwaarts springen"},
                        {"label": "Zijwaarts verplaatsen",
                         "value": "Zijwaarts verplaatsen"},
                        {"label": "Hand-oog coördinatie",
                         "value": "Hand-oog coördinatie"},
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


    # This callback is used to dynamically return the filters selection menu
    @dash_app.callback(
        Output('filter_selection', 'children'),
        [Input('dashboard_data', 'children')])
    def filter_selection(dashboard_data) -> dbc.Card:
        dashboard_data = pd.DataFrame(dashboard_data)
        dashboard_data["geboortedatum"] = pd.to_datetime(dashboard_data["geboortedatum"])

        return dbc.Card([
            dbc.CardHeader("Filters", class_name="text-center fw-bold",
                           style={"background-color": "#FF9900"}),
            dbc.CardBody(
                [
                    # Team selection dropdown
                    dcc.Dropdown(
                        sorted([team_name for team_name in dashboard_data["team_naam"].unique()]),
                        id="teams",
                        placeholder="Teams",
                        className="mb-2"),

                    # Lichting selection dropdown
                    dcc.Dropdown(
                        sorted([lichting for lichting in dashboard_data["geboortedatum"].dt.year.unique()]),
                        id="lichting",
                        placeholder="Lichting",
                        className="mb-2"),

                    # Seizoen selection dropdown
                    dcc.Dropdown(
                        [season for season in dashboard_data["seizoen"].unique()],
                        id="seizoen",
                        placeholder="Seizoen",
                    ),
                ]
            ),
        ], class_name="mb-4")

    @dash_app.callback(Output("filter_output", "children"), 
        [Input("dashboard_data", "children"),
        Input("teams", "value"),
        Input("lichting", "value"),
        Input("seizoen", "value"),
        Input("statistics", "value"),
        Input("bvo", "value"),
        Input("bloc_test_selection", "value")])
    def filter_data(dashboard_data, teams, lichting, seizoen, statistics, bvo, bloc_test_selection):
        dashboard_data = pd.DataFrame(dashboard_data)
        dashboard_data["geboortedatum"] = pd.to_datetime(dashboard_data["geboortedatum"])

        if teams is not None:
            dashboard_data = dashboard_data[dashboard_data["team_naam"] == teams]
        if lichting is not None:
            dashboard_data = dashboard_data[dashboard_data["geboortedatum"].dt.year == lichting]
        if seizoen is not None:
            dashboard_data = dashboard_data[dashboard_data["seizoen"] == seizoen]
        #if bvo is not None:
            # mist nog

        if bloc_test_selection is not None:
            column_results = [columns.get(bloc_test_selection) for bloc_test_selection 
                in bloc_test_selection if bloc_test_selection not in columns] 
            dashboard_data = dashboard_data.drop(column_results, axis=1)

        return dashboard_data.to_dict(orient='records')


    # This callback is used to dynamically return the bloc test chart
    @dash_app.callback(
        Output("algemene_motoriek_graph", "children"),
        [Input("selected_dashboard", "children"), Input("filter_output", "children")])
    def create_bloc_test_chart(selected_dashboard, dashboard_data):
        if selected_dashboard != "algemene_motoriek":
            return None

        if dashboard_data is None:
            # PreventUpdate prevents ALL outputs updating
            raise dash.exceptions.PreventUpdate

        figure = algemene_motoriek_chart.create_chart(
            pd.DataFrame(dashboard_data))
        return dcc.Graph(figure=figure, responsive=True)


    # This callback is used to dynamically create a boxplot
    @dash_app.callback(
        Output("boxplot", "figure"),
        [Input("filter_output", "children")])
    def create_boxplot(dashboard_data):
        # place code for creating the boxplot here
        # var dashboard data contains a dict of the current dashboard data DataFrame

        # return created plot here as callback output
        return {}


    # This callback is used to dynamically create a line chart
    @dash_app.callback(
        Output("line_chart", "figure"),
        [Input("filter_output", "children")])
    def create_line_chart(dashboard_data):
        # place code for creating the line chart here
        # var dashboard data contains a dict of the current dashboard data DataFrame

        # return created chart here as callback output
        return {}
