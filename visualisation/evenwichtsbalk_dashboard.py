import dash
from dash import html, Input, Output, dcc, ctx
import dash_bootstrap_components as dbc
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import plotly.graph_objects as go
from database.database import request_evenwichtsbalk
from flask import session

result = request_evenwichtsbalk()
result["datum"] = pd.to_datetime(result["datum"])


def filter_data(selection):
    bvo_id = session.get("id")
    measurements = pd.Series(result["meting"].unique())
    measurement_count = selection if selection != 0 else len(measurements)

    df_club = result[result["club_code"] == bvo_id]
    filtered_data = df_club[df_club["meting"].isin(
        measurements.iloc[-measurement_count:])].reset_index(drop=True)

    return filtered_data


def calculate_medians(dataframe: pd.DataFrame) -> pd.DataFrame:
    # voor nu zijn dit allen de mediaanen per team en meting
    return dataframe.groupby(["team_naam"]).median(numeric_only=True).reset_index()


def filter_buttons(input_field) -> int:
    if ((input_field is not None) and ((ctx.triggered_id == "btn-input"))):
        return input_field
    elif (ctx.triggered_id == "btn-1"):
        return 1
    elif (ctx.triggered_id == "btn-3"):
        return 3
    elif (ctx.triggered_id == "btn-5"):
        return 5
    elif (ctx.triggered_id == "btn-10"):
        return 10
    elif (ctx.triggered_id == "btn-input"):
        return input_field
    else:
        return 0

# This method is used by the app.py to initialize the Dash dashboard in Flask
# This workaround allows us to use Dash inside a Flask app by using its own route


def init_evenwichtsbalk_dashboard(server):
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dashboard/dash/evenwichtsbalk/',
        external_stylesheets=[dbc.themes.BOOTSTRAP]
    )

    input_group = dbc.InputGroup(
        [
            dbc.Button("Handmatige keuze", id="btn-input", color="dark"),
            dbc.Input(id="input-field",
                      type="number", min=1),
        ], class_name="w-25"),

    button_group = html.Div(
        [
            dbc.Button("Alle metingen", id="btn-all",
                       color="dark", class_name="me-1"),
            dbc.Button("Laatste meting", id="btn-1",
                       color="dark", class_name="me-1"),
            dbc.Button("Laatste 3 metingen", id="btn-3",
                       color="dark", class_name="me-1"),
            dbc.Button("Laatste 5 metingen", id="btn-5",
                       color="dark", class_name="me-1"),
            dbc.Button("Laatste 10 metingen", id="btn-10",  color="dark"),
        ],
    )

    # All the layout items such as the dashboard's charts itself are put in this 'layout' variable below
    dash_app.layout = html.Div(children=[
        dbc.Row(
            [
                dbc.Col(button_group, class_name="text-end"),
                dbc.Col(input_group),
            ],
            class_name="mt-5"),
        dcc.Graph(id="evenwichtsbalk-graph", style={'height': '80vh'}),
    ])

    # Callbacks for the Dash dashboard are initilized here after the creation of the layout has been completed
    init_callbacks(dash_app)

    return dash_app.server


# This method is used to create and initialize callbacks that will be used by the charts or selection items
def init_callbacks(dash_app):
    @ dash_app.callback(Output("evenwichtsbalk-graph", "figure"),
                        [
        Input("input-field", "value"),
        Input("btn-all", "n_clicks"),
        Input("btn-1", "n_clicks"),
        Input("btn-3", "n_clicks"),
        Input("btn-5", "n_clicks"),
        Input("btn-10", "n_clicks"),
        Input("btn-input", "n_clicks"),
    ],)
    def build_graph(*buttons):
        measurent_input = buttons[0] if ctx.triggered_id == "btn-input" else None
        measurent_selection = filter_buttons(measurent_input)
        df_club = filter_data(measurent_selection)
        deltas = calculate_medians(df_club)

        bb3cm = go.Box(x=df_club["team_naam"], y=df_club["Balance_Beam_3cm"],
                       boxpoints='all', name="Evenwichtsbalk 3 cm", marker_color="#636EFA")
        bb4_5cm = go.Box(x=df_club["team_naam"], y=df_club["Balance_Beam_4_5cm"],
                         boxpoints='all', name="Evenwichtsbalk 4,5 cm", marker_color="#EF553B")
        bb6cm = go.Box(x=df_club["team_naam"], y=df_club["Balance_Beam_6cm"],
                       boxpoints='all',  name="Evenwichtsbalk 6 cm", marker_color="#00CC96")
        bb_total = go.Box(
            x=df_club["team_naam"], y=df_club["Balance_beam_totaal"], name="Evenwichtsbalk totaal", marker_color="#AB63FA")

        bb3cm_m = go.Scatter(x=deltas["team_naam"], y=deltas["Balance_Beam_3cm"],
                             mode='lines+markers', name="Evenwichtsbalk 3 cm mediaan", line_color="#636EFA")
        bb4_5cm_m = go.Scatter(x=deltas["team_naam"], y=deltas["Balance_Beam_4_5cm"],
                               name="Evenwichtsbalk 4,5 cm mediaan", mode='lines+markers', line_color='#EF553B')
        bb6cm_m = go.Scatter(x=deltas["team_naam"], y=deltas["Balance_Beam_6cm"],
                             name="Evenwichtsbalk 6 cm mediaan", mode='lines+markers', line_color='#00CC96')
        bb_total_m = go.Scatter(x=deltas["team_naam"], y=deltas["Balance_beam_totaal"],
                                name="Evenwichtsbalk totaal mediaan", mode='lines+markers', line_color='#AB63FA')

        bb_medians = go.Figure(data=[bb3cm_m, bb4_5cm_m, bb6cm_m])

        fig = make_subplots(rows=4, cols=2, column_widths=[0.7, 0.3], x_title="Team", y_title="Aantal stappen", subplot_titles=(
            "Evenwichtsbalk 3 cm", "Individuele evenwichtsbalk medianen", "Evenwichtsbalk 4,5 cm", "Evenwichtsbalk totaal mediaan",
            "Evenwichtsbalk 6 cm", "", "Evenwichtsbalk totaal", ""))

        fig.add_trace(bb3cm, row=1, col=1)
        fig.add_trace(bb4_5cm, row=2, col=1)
        fig.add_trace(bb6cm, row=3, col=1)
        fig.add_trace(bb_total, row=4, col=1)

        for trace in bb_medians.data:
            fig.append_trace(trace, row=1, col=2)
            
        fig.add_trace(bb_total_m, row=2, col=2)
        

        return fig
