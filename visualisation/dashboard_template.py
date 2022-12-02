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

    # All the layout items such as the dashboard's charts itself are put in this 'layout' variable below
    dash_app.layout = dbc.Container(
    [
        # get the current selected url and store the selected dashboard in a dcc.Store object
        dcc.Location(id="url", refresh=True),
        dcc.Store(id='selected_dashboard'),
        dcc.Store(id='dashboard_data'),

        dbc.Row(
                [
                    dbc.Col(html.Div(), width=3),
                    dbc.Col(dcc.Graph(id="boxplot", responsive=True), width=9, class_name="w-100"),
              ],
            ),
        dbc.Row(
                [
                    dbc.Col(html.Div(), width=3),
                    dbc.Col(dcc.Graph(id="line_chart", responsive=True), width=9, class_name="w-100"),
              ],
            ),
    ])

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
        else: return dict()

    
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