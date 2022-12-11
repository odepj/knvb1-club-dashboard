import dash
from dash import html, Input, Output, dcc
import dash_bootstrap_components as dbc
import itertools
import pandas as pd
import regex as re
from database.database import request_vertesprong, request_sprint, request_change_of_direction, \
    request_algemene_motoriek, request_bvo
from flask import session
from visualisation import algemene_motoriek_chart
import plotly.graph_objs as go
from visualisation.util_functions import calculate_mean_result_by_date, add_figure_rangeslider

# this list contains the names of all the unique bvo's in the database
BVO_LIST = request_bvo()
META_COLUMNS = ['id', 'bvo_naam', 'seizoen', 'Testdatum', 'reeks_naam', 'team_naam', 'display_name', 'speler_id',
                'geboortedatum', 'Staande_lengte']


def filter_bloc_tests(dashboard_data: pd.DataFrame, bloc_test_selection: list) -> pd.DataFrame:
    # This dictionary will be used to lookup BLOC-test specific rows
    columns = {"Evenwichtsbalk": ["Balance_Beam_3cm", "Balance_Beam_4_5cm", "Balance_Beam_6cm", "Balance_beam_totaal"],
               "Zijwaarts springen": ["Zijwaarts_springen_1", "Zijwaarts_springen_2", "Zijwaarts_springen_totaal"],
               "Zijwaarts verplaatsen": ["Zijwaarts_verplaatsen_1", "Zijwaarts_verplaatsen_2",
                                         "Zijwaarts_verplaatsen_totaal"],
               "Hand-oog coördinatie": ["Oog_hand_coordinatie_1", "Oog_hand_coordinatie_2",
                                        "Oog_hand_coordinatie_totaal"]}

    # remove all the bloc_tests from the columns dictionary if it exists in selection
    for bloc_test in bloc_test_selection:
        columns.pop(bloc_test)

    remaining_columns = list(columns.values())
    dropped_list = list(itertools.chain.from_iterable(remaining_columns))
    return dashboard_data.drop(dropped_list, axis=1)


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
                    options=BVO_LIST["display_name"],
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
                value=["mediaan",
                       "boxplot", "individuen"],
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
                        html.Div(id="bloc_test_selection"),
                        html.Div(id="filter_selection"),
                        statistics,
                        benchmark
                    ]
                ),
                # Graphs
                dbc.Col(
                    width=10,
                    children=[
                        html.Div(id="show_boxplot"),
                        dbc.Row(id='graph-container', class_name='d-flex justify-content-center',
                                children=[dbc.Card(id='overview', class_name='col-10'), dcc.Graph(id="line_chart")]),
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

        data_set = data_dict
        return data_dict

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
                    value=["Evenwichtsbalk", "Zijwaarts springen",
                           "Zijwaarts verplaatsen", "Hand-oog coördinatie"],
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
                        Input("bvo", "value"),
                        Input("bloc_test_selection", "value")])
    def filter_data(dashboard_data, teams, lichting, seizoen, bvo, bloc_test_selection):
        dashboard_data = pd.DataFrame(dashboard_data)
        dashboard_data["geboortedatum"] = pd.to_datetime(dashboard_data["geboortedatum"])

        if teams is not None:
            dashboard_data = dashboard_data[dashboard_data["team_naam"] == teams]
        if lichting is not None:
            dashboard_data = dashboard_data[dashboard_data["geboortedatum"].dt.year == lichting]
        if seizoen is not None:
            dashboard_data = dashboard_data[dashboard_data["seizoen"] == seizoen]
        if bvo is not None:
            team_naam = BVO_LIST[BVO_LIST["display_name"] == bvo]['bvo_naam'].values[0]
            dashboard_data = dashboard_data[dashboard_data["bvo_naam"] == team_naam]

        if bloc_test_selection is not None:
            dashboard_data = filter_bloc_tests(dashboard_data, bloc_test_selection)

        return dashboard_data.to_dict(orient='records')

    # This callback is used to dynamically create a line chart
    @dash_app.callback(Output("line_chart", "figure"),
                       [Input("filter_output", "children")])
    # Input("statistics", "value"),])
    def create_line_chart(dashboard_data):
        bvo_id = session.get('id')
        dashboard_data = pd.DataFrame(dashboard_data)

        # #Get the columns that have the actual measurement
        measurement_columns = list(set(dashboard_data.columns.values).symmetric_difference(META_COLUMNS))
        measurement = sorted([col for col in measurement_columns if any(x in col for x in ['beste', 'totaal'])])

        # place code for creating the line chart here
        mean = calculate_mean_result_by_date(dashboard_data.drop_duplicates(), measurement)
        club = calculate_mean_result_by_date(dashboard_data[dashboard_data['bvo_naam'] == bvo_id].drop_duplicates(),
                                             measurement)

        bundled_df: list[pd.DataFrame] = [club, mean]

        fig = go.Figure()
        for idx, df in enumerate(bundled_df):
            x = df.index
            for column in measurement:
                column_name = column.replace('_', ' ')
                bvo_name = df['bvo_naam'].values[0]
                name = f'{bvo_name} - {column_name}'
                y = df[column]
                fig.add_trace(go.Scatter(x=x, y=y, name=name))

        fig.update_layout(
            yaxis_title='Totaal score (punten)',
            xaxis_title='Datum',
            legend_title="Teams",
            title_x=0.5
        )
        fig = add_figure_rangeslider(fig)
        return fig

    @dash_app.callback(Output("overview", "children"),
                       [Input("line_chart", "selectedData"),
                        Input("line_chart", "relayoutData")])
    def update_line_chart(selectedData, relayoutData):
        return f'{selectedData}, {relayoutData}'

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
        print(statistics)

        if "boxplot" in statistics:
            return dcc.Graph(id="boxplot", responsive=True)

    # This callback is used to dynamically create a boxplot
    @dash_app.callback(
        Output("boxplot", "figure"),
        [Input("filter_output", "children")])
    def create_boxplot(dashboard_data):
        # place code for creating the boxplot here
        # var dashboard data contains a dict of the current dashboard data DataFrame

        # return created plot here as callback output
        return {}
