import dash
from dash import html


def init_dashboard(server):
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dashboard/algemene_moteriek/',
        external_stylesheets=[
            'static/css/main.css',
        ]
    )

    dash_app.layout = html.Div([html.H4("he's alive!")])




    init_callbacks(dash_app)


    return dash_app.server


def init_callbacks(dash_app):
    #@app.callback()
    #def update_graph(rows):
        # Callback logic
        # ...
    return None

     