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


def calculate_medians_by_team(dataframe: pd.DataFrame) -> pd.DataFrame:
    return dataframe.groupby(["team_naam"]).median(numeric_only=True).reset_index()


def calculate_medians_by_measurement(dataframe: pd.DataFrame) -> pd.DataFrame:
    return dataframe.groupby(["team_naam", "meting"]).median(numeric_only=True).reset_index()


def calculate_delta(dataframe: pd.DataFrame) -> pd.DataFrame:
    medians = calculate_medians_by_measurement(dataframe)
    return medians


def create_balance_beam_plots(df_club: pd.DataFrame):
    bb3cm = go.Box(x=df_club["team_naam"], y=df_club["Balance_Beam_3cm"],
                   boxpoints='all', name="Evenwichtsbalk 3 cm", marker_color="#636EFA")
    bb4_5cm = go.Box(x=df_club["team_naam"], y=df_club["Balance_Beam_4_5cm"],
                     boxpoints='all', name="Evenwichtsbalk 4,5 cm", marker_color="#EF553B")
    bb6cm = go.Box(x=df_club["team_naam"], y=df_club["Balance_Beam_6cm"],
                   boxpoints='all',  name="Evenwichtsbalk 6 cm", marker_color="#00CC96")
    bb_total = go.Box(x=df_club["team_naam"], y=df_club["Balance_beam_totaal"],
                      name="Evenwichtsbalk totaal", marker_color="#AB63FA")
    return [bb3cm, bb4_5cm, bb6cm, bb_total]


def create_balance_beam_median_plots(team_medians: pd.DataFrame):
    bb3cm_m = go.Scatter(x=team_medians["team_naam"], y=team_medians["Balance_Beam_3cm"],
                         mode='lines+markers', name="Evenwichtsbalk 3 cm mediaan", line_color="#636EFA")
    bb4_5cm_m = go.Scatter(x=team_medians["team_naam"], y=team_medians["Balance_Beam_4_5cm"],
                           name="Evenwichtsbalk 4,5 cm mediaan", mode='lines+markers', line_color='#EF553B')
    bb6cm_m = go.Scatter(x=team_medians["team_naam"], y=team_medians["Balance_Beam_6cm"],
                         name="Evenwichtsbalk 6 cm mediaan", mode='lines+markers', line_color='#00CC96')
    bb_total_m = go.Scatter(x=team_medians["team_naam"], y=team_medians["Balance_beam_totaal"],
                            name="Evenwichtsbalk totaal mediaan", mode='lines+markers', line_color='#AB63FA')
    return [go.Figure(data=[bb3cm_m, bb4_5cm_m, bb6cm_m]), bb_total_m]


def create_total_progression_plot(measurement_medians: pd.DataFrame):
    colours = {
        "Onder 13": "#FF0000",
        "Onder 14": "#00FF00",
        "Onder 15": "#0000FF",
        "Onder 16": "#4B0082",
        "Onder 17": "#9400D3",
    }
    return px.line(measurement_medians, x="meting", y="Balance_beam_totaal",
                   color="team_naam", markers=True, color_discrete_map=colours)


def create_subplots(bb_plots, bb_m_plots, progression_plot):
    fig = make_subplots(rows=4, cols=2, column_widths=[0.7, 0.3], x_title="Team", y_title="Aantal stappen", subplot_titles=(
        "Evenwichtsbalk 3 cm", "Individuele evenwichtsbalk medianen", "Evenwichtsbalk 4,5 cm", "Evenwichtsbalk totaal mediaan",
        "Evenwichtsbalk 6 cm", "Evenwichtsbalk totaal progressie", "Evenwichtsbalk totaal", ""))

    for i in range(0, 4):
        fig.add_trace(bb_plots[i], row=i+1, col=1)

    for trace in bb_m_plots[0].data:
        fig.append_trace(trace, row=1, col=2)

    fig.add_trace(bb_m_plots[1], row=2, col=2)

    for trace in progression_plot.data:
        fig.append_trace(trace, row=3, col=2)

    return fig


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
        ]),

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
                dbc.Col(button_group, class_name="text-end", width=8),
                dbc.Col(input_group, width=4),
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
        bb_plots = create_balance_beam_plots(df_club)

        team_medians = calculate_medians_by_team(df_club)
        bb_m_plots = create_balance_beam_median_plots(team_medians)

        measurement_medians = calculate_medians_by_measurement(df_club)
        progression_plot = create_total_progression_plot(measurement_medians)

        return create_subplots(bb_plots, bb_m_plots, progression_plot)
