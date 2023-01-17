from typing import List, Tuple, Any, Dict, Union

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import regex as re
from dash import html, Input, Output, dcc
from flask import session

from database.database import request_vertesprong, request_sprint, request_change_of_direction, \
    request_algemene_motoriek, request_bvo
from visualisation.dash.dash_app_graphs import *

# this list contains the names of all the unique bvo's in the database
BVO_LIST = request_bvo()


def save_filter_to_session(key: str, value: str) -> None:
    session[key] = value


def retrieve_filter_from_session(key: str):
    return session.get(key)


# This method is used by the app.py to initialize the Dash dashboard in Flask
# This workaround allows us to use Dash inside a Flask app by using its own route
def init_dashboard_template(server):
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix="/dashboard/dash/dashboard_template/",
        external_stylesheets=[dbc.themes.BOOTSTRAP]
    )

    dash_app.layout = basic_dashboard_layout()
    # All the layout items such as the dashboard's charts itself are put in this 'layout' variable below

    # Callbacks for the Dash dashboard are initilized here after the creation of the layout has been completed
    init_callbacks(dash_app)
    # dash_app.run(debug=True, dev_tools_hot_reload=True, )
    return dash_app.server


def basic_dashboard_layout():
    return dbc.Container(
        id='container',
        style={'padding': '1rem'},
        fluid=True,
        children=[
            # get the current selected url and store the selected dashboard in a dcc.Store object
            dcc.Location(id="url", refresh=True),
            dcc.Store(id='selected_dashboard'),
            dcc.Store(id='dashboard_data'),
            dcc.Store(id='filter_output'),

            dbc.Row([
                # Filter menu's
                dbc.Col(width=2,
                        children=[
                            dbc.Card(id="filter_selection_card",
                                     style={'margin-bottom': '1rem'},
                                     children=[
                                         dbc.CardHeader("Filters", class_name="text-center fw-bold",
                                                        style={"background-color": "#FF9900"}),
                                         dbc.CardBody(id="filter_selectors",
                                                      children=[
                                                          # Team selection dropdown
                                                          dcc.Dropdown(
                                                              id="teams_selector",
                                                              placeholder="Teams",
                                                              className="mb-2"
                                                          ),

                                                          # Lichting selection dropdown
                                                          dcc.Dropdown(
                                                              id="lichting_selector",
                                                              placeholder="Lichting",
                                                              className="mb-2"
                                                          ),

                                                          # Seizoen selection dropdown
                                                          dcc.Dropdown(
                                                              id="seizoen_selector",
                                                              placeholder="Seizoen",
                                                              className="mb-2"
                                                          ),
                                                      ])
                                     ]),
                            dbc.Card(id="measurement_selection_card",
                                     style={'margin-bottom': '1rem'},
                                     children=[
                                         dbc.CardHeader("Metingen",
                                                        class_name="text-center fw-bold",
                                                        style={"background-color": "#FF9900"}),
                                         dbc.CardBody(
                                             dbc.Checklist(
                                                 id="measurement_selector",
                                                 label_checked_style={"color": "green"},
                                                 input_style={"backgroundColor": "red"},
                                                 input_checked_style={
                                                     "backgroundColor": "green",
                                                     "borderColor": "#green",
                                                 },
                                             )
                                         )
                                     ]),
                            dbc.Card(id="statistics_selection_card",
                                     style={'margin-bottom': '1rem'},
                                     children=[
                                         dbc.CardHeader("Statistiek",
                                                        class_name="text-center fw-bold",
                                                        style={"background-color": "#FF9900"}),
                                         dbc.CardBody(
                                             [dbc.Checklist(
                                                 id="statistics_selector",
                                                 options=[
                                                     {"label": "Gemiddelde", "value": "gemiddelde"},
                                                     {"label": "Mediaan", "value": "mediaan"},
                                                     {"label": "Boxplot", "value": "boxplot"},
                                                     {"label": "Individuen", "value": "individuen"},
                                                 ],
                                                 value=[],
                                                 label_checked_style={"color": "green"},
                                                 input_style={"backgroundColor": "red"},
                                                 input_checked_style={
                                                     "backgroundColor": "green",
                                                     "borderColor": "#green",
                                                 },
                                             ),
                                             ],
                                         ),
                                     ]),
                        ]),
                # Graphs
                dbc.Col(width=10,
                        children=[
                            dcc.Graph(id="boxplot", style={"height": "45rem"}),
                            dcc.Graph(id="line_chart"),
                            dbc.Col(id="algemene_motoriek_graph"),
                        ])
            ])
        ])


# This method is used to create and initialize callbacks that will be used by the charts or selection items
def init_callbacks(dash_app):
    # This callback is used to dynamically return the current selected dashboard from the url
    @dash_app.callback(
        Output('selected_dashboard', 'data'),
        [Input('url', 'pathname')])
    def get_selected_dashboard(pathname) -> str:
        return re.sub(r'^.+/([^/]+)$', r'\1', pathname)

    @dash_app.callback(
        Output('dashboard_data', 'data'),
        [Input('selected_dashboard', 'data')])
    def get_dashboard_data(selected_dashboard) -> list[dict]:
        bvo_id = session.get('id')
        # bvo_id = '1X8m4'
        data = pd.DataFrame()

        if selected_dashboard == "verspringen":
            data = request_vertesprong(bvo_id)
        elif selected_dashboard == "sprint":
            data = request_sprint(bvo_id)
        elif selected_dashboard == "cod":
            data = request_change_of_direction(bvo_id)
        elif selected_dashboard == "algemene_motoriek":
            data = request_algemene_motoriek(bvo_id)
        data["geboortedatum"] = pd.to_datetime(data["geboortedatum"])
        data['lichting'] = data["geboortedatum"].dt.year

        return data.to_dict(orient='records')

    # This callback is used to dynamically return the filters selection menu
    @dash_app.callback(dict(teams_selector=Output("teams_selector", "options"),
                            lichting_selector=Output("lichting_selector", "options"),
                            seizoen_selector=Output("seizoen_selector", "options")),
                       [Input('dashboard_data', 'data'),
                        Input("teams_selector", "value"),
                        Input("lichting_selector", "value"),
                        Input("seizoen_selector", "value"),
                        ])
    def filter_selection(dashboard_data, team_selector, lichting_selector, seizoen_selector):
        df = pd.DataFrame(dashboard_data)
        original_values = get_unique_values(df, ['team_naam', 'lichting', 'seizoen'])
        to_filter_by = [('team_naam', team_selector), ('lichting', lichting_selector), ('seizoen', seizoen_selector)]

        return dict(
            teams_selector=get_filter_options_or_default(df, 'team_naam', [to_filter_by[1], to_filter_by[2]], original_values),
            lichting_selector=get_filter_options_or_default(df, 'lichting', [to_filter_by[0], to_filter_by[2]], original_values),
            seizoen_selector=get_filter_options_or_default(df, 'seizoen', [to_filter_by[0], to_filter_by[1]], original_values)
        )

    # This callback is used to dynamically return the statistics selection menu
    @dash_app.callback(
        Output('statistics_selector', 'value'),
        [Input('dashboard_data', 'data')])
    def statistics_selection(dashboard_data) -> dbc.Card:
        # add the default statistics selection
        values = ["mediaan", "boxplot", "individuen"]

        session_statistics = retrieve_filter_from_session("statistics")
        if session_statistics is None:
            session_statistics = values
            save_filter_to_session("statistics", values)

        return session_statistics


    @dash_app.callback(
        dict(options=Output('measurement_selector', 'options'),
             value=Output('measurement_selector', 'value')),
        [Input('dashboard_data', 'data'),
         Input('selected_dashboard', 'data')])
    def measurement_selection(dashboard_data, selected_dashboard):
        dashboard_data = pd.DataFrame(dashboard_data)
        if dashboard_data.empty:
            # PreventUpdate prevents ALL outputs updating
            raise dash.exceptions.PreventUpdate

        measurements = get_measurement_columns(dashboard_data)
        options = [{"label": f"{rename_column(entry)}", "value": f"{entry}"} for entry in measurements]

        session_statistics = retrieve_filter_from_session("measurement_selection")
        if session_statistics is None:
            session_statistics = measurements
        save_filter_to_session("measurement_selection", session_statistics)

        return dict(options=options, value=measurements)

    @dash_app.callback(Output("filter_output", "data"),
                       [Input("dashboard_data", "data"),
                        Input("teams_selector", "value"),
                        Input("lichting_selector", "value"),
                        Input("seizoen_selector", "value"),
                        Input("measurement_selector", "value"),
                        Input("statistics_selector", "value")])
    def filter_data(dashboard_data, teams, lichting, seizoen, measurement_selection, statistics: list) -> list[dict]:
        dashboard_data = pd.DataFrame(dashboard_data)

        if teams is not None:
            dashboard_data = dashboard_data[dashboard_data["team_naam"] == teams]

        if lichting is not None:
            dashboard_data = dashboard_data[dashboard_data["lichting"] == lichting]

        if seizoen is not None:
            dashboard_data = dashboard_data[dashboard_data["seizoen"] == seizoen]

        if measurement_selection is not None:
            dashboard_data = filter_measurements(dashboard_data, measurement_selection)

        if any(item in ['gemiddelde', 'mediaan'] for item in statistics):
            dashboard_data = aggregate_measurement_by_team_result(dashboard_data, statistics)

        save_filter_to_session("teams", teams)
        save_filter_to_session("lichting", lichting)
        save_filter_to_session("seizoen", seizoen)
        save_filter_to_session("measurement_selection", measurement_selection)
        save_filter_to_session("statistics", statistics)

        return dashboard_data.to_dict(orient='records')

    # This callback is used to dynamically create a line chart
    @dash_app.callback(Output("line_chart", "figure"),
                       [Input("dashboard_data", "data"),
                        Input("filter_output", "data"),
                        Input("statistics_selector", "value")])
    def create_line_chart(dashboard_data, filter_output, statistics):
        filter_output = pd.DataFrame(filter_output)
        if filter_output.empty:
            # PreventUpdate prevents ALL outputs updating
            raise dash.exceptions.PreventUpdate
        if len(filter_output['team_naam'].unique()) == 1:
            raise dash.exceptions.PreventUpdate

        return create_line(filter_output, dashboard_data, statistics)

    # This callback is used to dynamically return the bloc test chart
    @dash_app.callback(
        Output("algemene_motoriek_graph", "children"),
        [Input("selected_dashboard", "data"), Input("filter_output", "data")])
    def create_bloc_test_chart(selected_dashboard, dashboard_data):
        if selected_dashboard != "algemene_motoriek":
            return None

        if dashboard_data is None:
            # PreventUpdate prevents ALL outputs updating
            raise dash.exceptions.PreventUpdate

        figure = create_chart(
            pd.DataFrame(dashboard_data))
        return dcc.Graph(figure=figure, responsive=True)

    # This callback is used to dynamically show the boxplot
    @dash_app.callback(
        Output("boxplot", "style"),
        [Input("statistics_selector", "value")])
    def show_boxplot(statistics):
        if statistics is not None and "boxplot" in statistics:
            return {"height": "45rem"}
        else:
            return {'display': 'none'}

    # This callback is used to dynamically create a boxplot
    @dash_app.callback(
        Output("boxplot", "figure"),
        [Input("selected_dashboard", "data")],
        [Input("statistics_selector", "value")],
        [Input("filter_output", "data")])
    def create_boxplot(selected_dashboard, statistics, dashboard_data):
        # place code for creating the boxplot here
        # var dashboard data contains a dict of the current dashboard data DataFrame
        # return created plot here as callback output
        if dashboard_data is None:
            # PreventUpdate prevents ALL outputs updating
            raise dash.exceptions.PreventUpdate

        if selected_dashboard != "sprint":
            return create_box(
                "all" if "individuen" in statistics else False,
                pd.DataFrame(dashboard_data))

        return create_boxplot_function(
            "all" if "individuen" in statistics else False,
            pd.DataFrame(dashboard_data))
