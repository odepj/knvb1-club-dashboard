import dash
from dash import html, Input, Output, dcc, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import regex as re
from flask import session
from database.database import request_algemene_motoriek
import numpy
from functools import reduce

# Get all the neccessary data algemene motoriek data from the database
result = request_algemene_motoriek()

# This method is used by the app.py to initialize the Dash dashboard in Flask
# This workaround allows us to use Dash inside a Flask app by using its own route
def init_dashboard_template(server):
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix="/dashboard/dash/dashboard_template/",
        external_stylesheets=[dbc.themes.BOOTSTRAP]
    )

    # All the layout items such as the dashboard's charts itself are put in this 'layout' variable below
    dash_app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=True),
        html.H1(id="selected_dashboard"),
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
    def callback_func(pathname):
        return re.sub(r'^.+/([^/]+)$', r'\1', pathname)
