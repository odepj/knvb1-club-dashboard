import dash
from dash import html, Input, Output, dcc, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from flask import session
from database.database import request_algemene_moteriek
import numpy
from functools import reduce

# Get all the neccessary data algemene moteriek data from the database
result = request_algemene_moteriek()

# This dictionary will be used to lookup BLOC-test specific rows
columns = {"Evenwichtsbalk": ["Balance_Beam_3cm", "Balance_Beam_4_5cm", "Balance_Beam_6cm", "Balance_beam_totaal"],
           "Zijwaarts springen": ["Zijwaarts_springen_1", "Zijwaarts_springen_2", "Zijwaarts_springen_totaal"],
           "Zijwaarts verplaatsen": ["Zijwaarts_verplaatsen_1", "Zijwaarts_verplaatsen_2", "Zijwaarts_verplaatsen_totaal"],
           "Hand-oog coördinatie": ["Oog_hand_coordinatie_1", "Oog_hand_coordinatie_2", "Oog_hand_coordinatie_totaal"]}


# This method is used to prepare all the required rows based on the selected tests in the dropdown menu
def filter_test_data(tests: list):
    column_results = [columns.get(test) for test in tests if test in columns]
    column_results.insert(0, ["id", "display_name","club_code", "team_naam", "meting"])

    return list(numpy.concatenate(column_results).flat)


# This method is used to filter all the data based on the dropdown menu selections
def filter_data(teams, tests, measurements):
    # Get all the specific test, team, and measurement data with the dropdown selections
    filtered_tests = result[filter_test_data(tests)]
    filtered_teams = result[result["team_naam"].isin(teams)]
    filtered_measurements = result[result["meting"].isin(measurements)]

    # Here we use a reduce and merge function to get ONLY the rows that exist in ALL three filtered DataFrames
    final_results = reduce(lambda left, right: pd.merge(left, right, on=['id'],
                            how='inner', suffixes=('', '_DROP')),
                           [filtered_tests, filtered_teams[filtered_tests.columns],
                            filtered_measurements[filtered_tests.columns]]
                           ).filter(regex='^(?!.*_DROP)').reset_index(drop=True)

    return final_results


# This method is used to get the total BLOC-score per team_naam, meting and club code/name
def get_filtered_sum(teams, tests, measurements):
    bvo_id = session.get("id")
    filtered_data = filter_data(teams, tests, measurements)
    club_sorted = filtered_data[filtered_data["club_code"] == bvo_id]

    return club_sorted.groupby(["team_naam", "meting", "club_code",  "display_name"]).agg('sum')


# This method is used to get the median for each BLOC-test by getting the median from the sum of all club_codes
def get_filtered_median(teams, tests, measurements):
    filtered_data = filter_data(teams, tests, measurements)
    sum = filtered_data.groupby(["team_naam", "meting", "club_code", "display_name"]).agg('sum')

    return sum.reset_index().groupby(["team_naam", "club_code", "display_name"]).agg('median')


# This method is used by the app.py to initialize the Dash dashboard in Flask
# This workaround allows us to use Dash inside a Flask app by using its own route
def init_algemene_moteriek_dashboard(server):
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dashboard/dash/moteriek_dashboard/',
        external_stylesheets=[dbc.themes.BOOTSTRAP]
    )

    # All the selection items such as dropdown menu's are put in this 'controls' variable below
    controls = dbc.Card(
        [
            html.Div(
                [
                    # Team selection dropdown
                    dbc.Label("Team"),
                    dcc.Dropdown(
                        [team_name for team_name in result["team_naam"].unique()],
                        id="teams",
                        placeholder="Selecteer één of meerdere team(s)",
                        value=result["team_naam"].unique(),
                        multi=True
                    ),
                ]
            ),
            html.Div(
                [
                    # BLOC-test selection dropdown                    
                    dbc.Label("BLOC-testen"),
                    dcc.Dropdown(
                        ["Evenwichtsbalk", "Zijwaarts springen",
                            "Zijwaarts verplaatsen", "Hand-oog coördinatie"],
                        id="tests",
                        value=["Evenwichtsbalk", "Zijwaarts springen",
                               "Zijwaarts verplaatsen", "Hand-oog coördinatie"],
                        placeholder="Selecteer één of meerdere BLOC test(en)",
                        multi=True
                    ),
                ],
            ),
            html.Div(
                [
                    # Measurement selection dropdown
                    dbc.Label("Metingen"),
                    dcc.Dropdown(
                        [measurement for measurement in result["meting"].unique()],
                        id="measurements",
                        placeholder="Selecteer één of meerdere meting(en)",
                        value=result["meting"].unique(),
                        multi=True
                    ),
                ]
            ),
        ], body=True)

    # All the layout items such as the dashboard's charts itself are put in this 'layout' variable below
    dash_app.layout = dbc.Container(
        [
            # Controls variable items and algemene_moteriek-graph are initialised below
            dbc.Row(
                [
                    dbc.Col(controls, md=4),
                    dbc.Col(dcc.Graph(id="algemene_moteriek-graph"), md=8),
                ],
                align="center",
            ),

            # DataTable containing all the variable items medians per team and club are initialised below
            dbc.Container([
                html.H5("Medianen van BLOC-test score per team voor alle clubs (punten)",
                        style={"text-align": "center"}),
                dash_table.DataTable(
                    id='algemene_moteriek_data_table', style_table={'overflowY': 'scroll'}, style_data={
                        'color': 'black',
                        'backgroundColor': 'white'
                    },
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(220, 220, 220)',
                        }
                    ],
                    style_header={
                        'backgroundColor': 'rgb(210, 210, 210)',
                        'color': 'black',
                        'fontWeight': 'bold'
                    },),
            ])
        ], fluid=True)

    # Callbacks for the Dash dashboard are initilized here after the creation of the layout has been completed
    init_callbacks(dash_app)

    return dash_app.server


# This method is used to create and initialize callbacks that will be used by the charts or selection items
def init_callbacks(dash_app):
    # This callback is used to dynamically generate the algemene_moteriek-graph
    @dash_app.callback(
        Output("algemene_moteriek-graph", "figure"),
        [
            Input("teams", "value"),
            Input("tests", "value"),
            Input("measurements", "value"),
        ],)
    def build_graph(teams, tests, measurements):
        test_names = {"Balance_beam_totaal": "Evenwichtsbalk",
                      "Zijwaarts_springen_totaal": "Zijwaarts springen",
                      "Zijwaarts_verplaatsen_totaal": "Zijwaarts verplaatsen",
                      "Oog_hand_coordinatie_totaal": "Hand-oog coördinatie"}

        # Get the filtered sum data, columns containing total values and club name
        filtered_data = get_filtered_sum(teams, tests, measurements).reset_index()
        total_columns = filtered_data.filter(regex='totaal').columns
        club = filtered_data["display_name"].get(0, "Geen club beschikbaar")

        # Get all the details on demand columns from the columns dictionary that are not in the total_columns
        details_on_demand = [columns.get(test) for test in tests if test in columns]
        details_on_demand.insert(0, ["display_name", "club_code", "meting"])
        details_on_demand = list(filter(lambda x: (x not in total_columns), 
                            numpy.concatenate(details_on_demand).flat))

        hover_template = """Club naam: %{customdata[0]} <br>Club code: %{customdata[1]}
        <br>Team: %{x} <br>Totaal score: %{y} punten <br>Meting: %{customdata[2]}
        <br><br>BLOC-test specifieke totaal scores:<br>"""

        # Generate a hover_template for details on the demand by looping over the available details
        for i in range(3, len(details_on_demand)):
            hover_template += f"{details_on_demand[i]}: %{{customdata[{i}]}} punten<br>"

        # Create a bar chart using the filtered data and add additional styling and hover information        
        fig = px.bar(filtered_data, x='team_naam', y=total_columns,
                     title=f"BLOC-test totaal scores per team voor uw club: {club}", 
                     custom_data=details_on_demand)

        fig.update_layout(yaxis_title='Totaal score (punten)', xaxis_title='Team',
                          barmode='stack', legend_title="BLOC-testen", title_x=0.5)

        fig.update_traces(hovertemplate=hover_template)

        # rename every BLOC test variable to readable names for the legend and bars using the test_names dictionary
        fig.for_each_trace(lambda t: t.update(name=test_names[t.name]))

        return fig

    # This callback is used to dynamically generate the algemene_moteriek_data_table
    @dash_app.callback(Output('algemene_moteriek_data_table', 'data'),
                       Output('algemene_moteriek_data_table', 'columns'),
                       [Input("teams", "value"),
                        Input("tests", "value"),
                        Input("measurements", "value")])
    def update_data_table(teams, tests, measurements):
        column_names = {"display_name": "Club", "team_naam": "Team",
                        "Balance_beam_totaal": "Evenwichtsbalk mediaan",
                        "Zijwaarts_springen_totaal": "Zijwaarts springen mediaan",
                        "Zijwaarts_verplaatsen_totaal": "Zijwaarts verplaatsen mediaan",
                        "Oog_hand_coordinatie_totaal": "Hand-oog coördinatie mediaan"}

        # Only get the values that contain any of the regex values, these will be used for the data table
        filtered_data = get_filtered_median(teams, tests, measurements).reset_index().filter(
            regex='totaal|display_name|team_naam')

        # rename all columns to readable names for the data table using the column_names dictionary
        filtered_data.rename(columns=dict(column_names), inplace=True)

        return filtered_data.to_dict('records'), [{"name": i, "id": i} for i in filtered_data.columns]
