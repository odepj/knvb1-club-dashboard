import dash
from dash import html, Input, Output, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from flask import session
from database.database import request_algemene_moteriek
import numpy
from functools import reduce

# get all the neccessary data from the database
result = request_algemene_moteriek()

columns = {"Evenwichtsbalk": ["Balance_Beam_3cm", "Balance_Beam_4_5cm", "Balance_Beam_6cm", "Balance_beam_totaal"],
           "Zijwaarts springen": ["Zijwaarts_springen_1", "Zijwaarts_springen_2", "Zijwaarts_springen_totaal"],
           "Zijwaarts verplaatsen": ["Zijwaarts_verplaatsen_1", "Zijwaarts_verplaatsen_2", "Zijwaarts_verplaatsen_totaal"],
           "Hand-oog coördinatie": ["Oog_hand_coordinatie_1", "Oog_hand_coordinatie_2", "Oog_hand_coordinatie_totaal"]}


def filter_test_data(tests: list):
    column_results = [columns.get(test) for test in tests if test in columns]
    column_results.insert(0, ["id", "club_code", "team_naam", "meting"])

    return list(numpy.concatenate(column_results).flat)


def filter_data(teams, tests, measurements):
    bvo_id = session.get("id")
    filtered_tests = result[filter_test_data(tests)]
    filtered_teams = result[result["team_naam"].isin(teams)]
    filtered_measurements = result[result["meting"].isin(measurements)]

    final_results = reduce(lambda left, right: pd.merge(left, right, on=['id'],
                        how='inner', suffixes=('', '_DROP')),
                        [filtered_tests, filtered_teams[filtered_tests.columns],
                        filtered_measurements[filtered_tests.columns]]
                        ).filter(regex='^(?!.*_DROP)').reset_index(drop=True)

    club_filtered = final_results[final_results["club_code"] == bvo_id]
    return club_filtered.groupby(["team_naam", "meting", "club_code"]).agg('sum')


def init_dashboard(server):
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dashboard/dash/moteriek_dashboard/',
        external_stylesheets=[
            dbc.themes.BOOTSTRAP,
        ]
    )

    controls = dbc.Card(
        [
            html.Div(
                [
                    dbc.Label("Team"),
                    dcc.Dropdown(
                        [team_name for team_name in result["team_naam"].unique()],
                        id="teams",
                        placeholder="Select één of meerdere team(s)",
                        value=result["team_naam"].unique(),
                        multi=True
                    ),
                ]
            ),
            html.Div(
                [
                    dbc.Label("BLOC-testen"),
                    dcc.Dropdown(
                        ["Evenwichtsbalk", "Zijwaarts springen",
                            "Zijwaarts verplaatsen", "Hand-oog coördinatie"],
                        id="tests",
                        value=["Evenwichtsbalk", "Zijwaarts springen",
                               "Zijwaarts verplaatsen", "Hand-oog coördinatie"],
                        placeholder="Select één of meerdere BLOC test(en)",
                        multi=True
                    ),
                ],
            ),
            html.Div(
                [
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

    dash_app.layout = dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(controls, md=4),
                    dbc.Col(dcc.Graph(id="algemene_moteriek-graph"), md=8),
                ],
                align="center",
            ),
        ], fluid=True)

    init_callbacks(dash_app)

    return dash_app.server


def init_callbacks(dash_app):
    @dash_app.callback(
        Output("algemene_moteriek-graph", "figure"),
        [
            Input("teams", "value"),
            Input("tests", "value"),
            Input("measurements", "value"),
        ],)
    def build_graph(teams, tests, measurements):
        filtered_data = filter_data(teams, tests, measurements).reset_index()

        total_columns = filtered_data.filter(regex='totaal').columns
        club_code = filtered_data["club_code"].get(
            0, "Geen club code beschikbaar")

        fig = px.bar(filtered_data, x='team_naam', y=total_columns,
                     title=f"BLOC-test totaal score per team voor club: {club_code}",
                     )
        fig.update_layout(yaxis_title='Totaal score', xaxis_title='Team',
                          barmode='stack', legend_title="BLOC-testen", title_x=0.5)

        fig.update_traces(hovertemplate="Team: %{x} <br> Totaal score: %{y}")

        # rename every BLOC test variable to readable names for the legend
        test_names = {"Balance_beam_totaal": "Evenwichtsbalk", "Zijwaarts_springen_totaal": "Zijwaarts springen",
                      "Zijwaarts_verplaatsen_totaal": "Zijwaarts verplaatsen", "Oog_hand_coordinatie_totaal": "Hand-oog coördinatie"}
        fig.for_each_trace(lambda t: t.update(name=test_names[t.name]))

        return fig
