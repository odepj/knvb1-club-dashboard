import dash
from dash import html, Input, Output, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import regex as re
from database.database import request_vertesprong, request_sprint, request_change_of_direction, \
    request_algemene_motoriek, request_bvo
from flask import session
from visualisation import algemene_motoriek_chart
import plotly.graph_objs as go

from visualisation.boxplot import create_box
from visualisation.dashboard_template_functions import calculate_mean_result_by_date, \
    filter_bloc_tests, get_colormap, rename_column, filter_measurements, get_measurement_columns, \
    aggregate_measurement_by_team_result, drop_mean_and_median_columns, calculate_result_by_date
from visualisation.sprint_boxplot import create_boxplot_function

# this list contains the names of all the unique bvo's in the database
BVO_LIST = request_bvo()


def save_filter_to_session(key: str, value: str) -> None:
    session[key] = value


def retrieve_filter_from_session(key: str):
    return session.get(key)


def fix_labels(df: pd.DataFrame) -> dict:
    df_ticktext = df[['seizoen', 'reeks_naam']].drop_duplicates()
    ticktext = [f"""{row.seizoen.removeprefix('20')}, {row.reeks_naam}""" for row in df_ticktext.itertuples()]
    tickvals = df['Testdatum'].unique()
    return dict(
        tickmode='array',
        tickvals=tickvals,
        ticktext=ticktext  # tuple van (23/24 - na/voorjaar)
    )


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
        fluid=True, children=[
            # get the current selected url and store the selected dashboard in a dcc.Store object
            dcc.Location(id="url", refresh=True),
            dcc.Store(id='selected_dashboard'),
            dcc.Store(id='dashboard_data'),
            dcc.Store(id='filter_output'),

            dbc.Row([
                # Filter menu's
                dbc.Col(
                    width=2,
                    children=[
                        html.Div(id="filter_selection"),
                        html.Div(id="bloc_test_selection"),
                        html.Div(id="measurement_selection"),
                        html.Div(id="statistics_selection"),
                        html.Div(id="benchmark_selection"),
                        html.Div(id='bvo_alert'),
                    ],
                    style={"height": "10rem"}),
                # Graphs
                dbc.Col(
                    width=10,
                    children=[
                        html.Div(id="show_boxplot"),
                        dbc.Row(id='graph-container', class_name='d-flex justify-content-center',
                                children=[dcc.Graph(id="line_chart")]),
                        dbc.Col(html.Div(id="algemene_motoriek_graph")),
                    ]
                ),
            ])
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
        data_dict = dict()

        if selected_dashboard == "verspringen":
            data_dict = request_vertesprong(bvo_id).to_dict(orient='records')
        elif selected_dashboard == "sprint":
            data_dict = request_sprint(bvo_id).to_dict(orient='records')
        elif selected_dashboard == "cod":
            data_dict = request_change_of_direction(bvo_id).to_dict(orient='records')
        elif selected_dashboard == "algemene_motoriek":
            data_dict = request_algemene_motoriek(bvo_id).to_dict(orient='records')

        return data_dict

    # This callback is used to dynamically return the bloc test selection menu
    @dash_app.callback(
        Output('bloc_test_selection', 'children'),
        [Input('selected_dashboard', 'children')])
    def bloc_test_selection(selected_dashboard):
        if selected_dashboard != "algemene_motoriek":
            return None

        # add the default bloc-test selection
        values = ["Evenwichtsbalk", "Zijwaarts springen",
                  "Zijwaarts verplaatsen", "Hand-oog coördinatie"]

        session_bloc = retrieve_filter_from_session("bloc_test_selection")
        if session_bloc is None:
            session_bloc = values
            save_filter_to_session("bloc_test_selection", values)

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
                    value=session_bloc,
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
        [Input('dashboard_data', 'children'),
         Input('filter_output', 'children')])
    def filter_selection(dashboard_data, filter_output) -> dbc.Card:
        dashboard_data = pd.DataFrame(dashboard_data) if filter_output is None else pd.DataFrame(filter_output)
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
                        value=retrieve_filter_from_session("teams"),
                        placeholder="Teams",
                        className="mb-2"),

                    # Lichting selection dropdown
                    dcc.Dropdown(
                        sorted([lichting for lichting in dashboard_data["geboortedatum"].dt.year.unique()]),
                        id="lichting",
                        value=retrieve_filter_from_session("lichting"),
                        placeholder="Lichting",
                        className="mb-2"),

                    # Seizoen selection dropdown
                    dcc.Dropdown(
                        [season for season in dashboard_data["seizoen"].unique()],
                        id="seizoen",
                        value=retrieve_filter_from_session("seizoen"),
                        placeholder="Seizoen",
                    ),
                ]
            ),
        ], class_name="mb-4")

    # This callback is used to dynamically return the statistics selection menu
    @dash_app.callback(
        Output('statistics_selection', 'children'),
        [Input('dashboard_data', 'children')])
    def statistics_selection(dashboard_data) -> dbc.Card:
        # add the default statistics selection
        values = ["mediaan", "boxplot", "individuen"]

        session_statistics = retrieve_filter_from_session("statistics")
        if session_statistics is None:
            session_statistics = values
            save_filter_to_session("statistics", values)

        return dbc.Card([
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
                    value=session_statistics,
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

    # This callback is used to dynamically return the benchmark selection menu
    @dash_app.callback(
        Output('benchmark_selection', 'children'),
        [Input('dashboard_data', 'children')])
    def benchmark_selection(dashboard_data) -> dbc.Card:
        return dbc.Card([
            dbc.CardHeader("Benchmark", class_name="text-center fw-bold",
                           style={"background-color": "#FF9900"}),
            dbc.CardBody(
                [  # Benchmark selection dropdown
                    dcc.Dropdown(
                        placeholder="BVO's",
                        options=BVO_LIST["display_name"],
                        id="bvo",
                        value=retrieve_filter_from_session("bvo"),
                    ), ],
            ),
        ])

        # This callback is used to dynamically return the bloc test selection menu

    @dash_app.callback(
        Output('measurement_selection', 'children'),
        [Input('dashboard_data', 'children'),
         Input('selected_dashboard', 'children')])
    def measurement_selection(dashboard_data, selected_dashboard):
        if selected_dashboard == "algemene_motoriek":
            return None

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

        return dbc.Card([
            dbc.CardHeader("Metingen", class_name="text-center fw-bold",
                           style={"background-color": "#FF9900"}),
            dbc.CardBody(
                [dbc.Checklist(
                    id="measurement_selection",
                    options=options,
                    value=measurements,
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

    @dash_app.callback(Output('bvo_alert', 'children'),
                       Input('bvo', 'value'))
    def show_alert(bvo):
        if bvo is None:
            return {}

        return dbc.Alert("Functionaliteit niet beschikbaar!",
                         color="danger",
                         id="alert-fade",
                         dismissable=True,
                         style={'margin-top': '10px'}
                         )

    @dash_app.callback(Output("filter_output", "children"),
                       [Input("dashboard_data", "children"),
                        Input("teams", "value"),
                        Input("lichting", "value"),
                        Input("seizoen", "value"),
                        Input("bvo", "value"),
                        Input("bloc_test_selection", "value"),
                        Input("measurement_selection", "value"),
                        Input("statistics", "value")])
    def filter_data(dashboard_data, teams, lichting, seizoen, bvo, bloc_test_selection, measurement_selection,
                    statistics: list):
        dashboard_data = pd.DataFrame(dashboard_data)
        dashboard_data["geboortedatum"] = pd.to_datetime(dashboard_data["geboortedatum"])

        if teams is not None:
            dashboard_data = dashboard_data[dashboard_data["team_naam"] == teams]

        if lichting is not None:
            dashboard_data = dashboard_data[dashboard_data["geboortedatum"].dt.year == lichting]

        if seizoen is not None:
            dashboard_data = dashboard_data[dashboard_data["seizoen"] == seizoen]

        if bvo == session.get('id'):
            team_naam = BVO_LIST[BVO_LIST["display_name"] == bvo]['bvo_naam'].values[0]
            dashboard_data = dashboard_data[dashboard_data["bvo_naam"] == team_naam]

        if bloc_test_selection is not None:
            dashboard_data = filter_bloc_tests(dashboard_data, bloc_test_selection)

        if measurement_selection is not None:
            dashboard_data = filter_measurements(dashboard_data, measurement_selection)

        if any(item in ['gemiddelde', 'mediaan'] for item in statistics):
            dashboard_data = aggregate_measurement_by_team_result(dashboard_data, statistics)

        save_filter_to_session("teams", teams)
        save_filter_to_session("lichting", lichting)
        save_filter_to_session("seizoen", seizoen)
        save_filter_to_session("bvo", bvo)
        save_filter_to_session("bloc_test_selection", bloc_test_selection),
        save_filter_to_session("measurement_selection", measurement_selection),
        save_filter_to_session("statistics", statistics),

        return dashboard_data.to_dict(orient='records')

    # This callback is used to dynamically create a line chart
    @dash_app.callback(Output("line_chart", "figure"),
                       [Input("dashboard_data", "children"),
                        Input("filter_output", "children"),
                        Input("statistics", "value")])
    def create_line_chart(dashboard_data, filter_output, statistics):
        dashboard_data = pd.DataFrame(dashboard_data)
        filter_output = drop_mean_and_median_columns(pd.DataFrame(filter_output))
        additional_traces = list(set(statistics) - (set(statistics) - {'gemiddelde', 'mediaan'}))
        if filter_output.empty:
            # PreventUpdate prevents ALL outputs updating
            raise dash.exceptions.PreventUpdate
        if len(filter_output['team_naam'].unique()) == 1:
            raise dash.exceptions.PreventUpdate

        measurements = get_measurement_columns(filter_output)
        result = calculate_mean_result_by_date(filter_output, measurements)
        bundled_df = [df for _, df in result.groupby('lichting')]
        df_mean_median = [(calculate_result_by_date(dashboard_data, measurements, statistic), statistic) for statistic
                          in additional_traces]

        fig = go.Figure(layout=go.Layout(autosize=True, height=625))

        # Generate the traces for statistics
        dash_dict = {'gemiddelde': 'solid', 'mediaan': 'dot'}
        index = bundled_df[0].index
        for idx, tupy in enumerate(df_mean_median):
            df, statistic = tupy
            df = df[df.index.isin(index)]
            for jdx, measurement in enumerate(measurements):
                column_name = rename_column(measurement)
                fig.add_trace(go.Scatter(
                    x=df.index,
                    y=df[measurement],
                    name=statistic,
                    legendgroup=column_name,
                    legendgrouptitle=dict(text=column_name),
                    mode='lines+markers',
                    line_shape="spline",
                    line=dict(color='black', dash=dash_dict[statistic], width=3),
                ))

        # Generate traces for lichtingen
        dash_list = ['solid', 'dot', 'longdashdot', 'dashdot', 'longdash']
        for idx, df_lichting in enumerate(bundled_df):
            name = str(df_lichting['lichting'].values[0])
            for jdx, measurement in enumerate(measurements):
                column_name = rename_column(measurement)
                fig.add_trace(go.Scatter(
                    x=df_lichting.index,
                    y=df_lichting[measurement],
                    name=name,
                    legendgroup=column_name,
                    legendgrouptitle=dict(text=column_name),
                    mode='lines+markers',
                    line_shape="spline",
                    line=dict(color=get_colormap(idx), dash=dash_list[jdx], width=3),
                ))

        if len(measurements) > 0:
            predicate = filter_output[measurements[0]].dtype == int
            yaxis_title = 'Totaal score (punten)' if predicate else 'Beste of totaal resultaat'
        else:
            yaxis_title = 'Geen selectie'

        fig.update_layout(
            xaxis=fix_labels(filter_output),
            yaxis_title=yaxis_title,
            xaxis_title='Meet moment',
            title_text="<b>Ontwikkeling lichtingen<b>"
        )
        return fig

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

    # This callback is used to dynamically show the boxplot
    @dash_app.callback(
        Output("show_boxplot", "children"),
        [Input("statistics", "value")])
    def show_boxplot(statistics):
        if statistics is not None and "boxplot" in statistics:
            return dcc.Graph(id="boxplot", responsive=True, style={"height": "45rem"})

# This callback is used to dynamically create a boxplot
    @dash_app.callback(
        Output("boxplot", "figure"),
        [Input("selected_dashboard", "children")],
        [Input("statistics", "value")],
        [Input("filter_output", "children")])
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
