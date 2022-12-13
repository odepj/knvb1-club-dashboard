import itertools
import re
from functools import reduce

import pandas as pd
import plotly_express as px
from matplotlib import pyplot as plt

META_COLUMNS = ['id', 'bvo_naam', 'seizoen', 'Testdatum', 'reeks_naam', 'team_naam', 'display_name', 'speler_id',
                'geboortedatum', 'Staande_lengte']


def calculate_delta(value: pd.Series, from_, to_):
    # pandas counterpart, but I feel the latter will become more useful.
    # diff = value.pct_change(periods=len(value) - 1)
    first = value.loc[from_][0]
    last = value.get(to_)[0]
    return round(abs(((first - last) / first) * 100), 1)


def nearest(items, pivot):
    return min(items, key=lambda x: abs(x - pivot))


def calculate_mean_result_by_date(df: pd.DataFrame, columns):
    lichting = pd.to_datetime(df["geboortedatum"])
    df['lichting'] = lichting.dt.year

    df_mean: pd.DataFrame = df.groupby(['Testdatum', 'reeks_naam', 'lichting'])[columns].mean(numeric_only=False)
    df_mean = df_mean.reset_index()
    df_mean.index = df_mean['Testdatum']
    return df_mean


def get_colormap(index_selector) -> str:
    return f"{px.colors.qualitative.Set1[index_selector]}"


def add_figure_rangeslider(fig):
    # Add range slider
    return fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=12,
                         label="laatste 2 metingen",
                         step="month",
                         stepmode="backward"),
                    dict(count=2.25,
                         label="laatste 5 metingen",
                         step="year",
                         stepmode="backward"),
                    dict(count=5,
                         label="laatste 10 metingen",
                         step="year",
                         stepmode="todate"),
                    dict(label="alle metingen",
                         step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )


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


def filter_measurements(dashboard_data: pd.DataFrame, measurement_selection: list) -> pd.DataFrame:
    dropped_list = list(set(get_measurement_columns(dashboard_data)).symmetric_difference(measurement_selection))
    return dashboard_data.copy().drop(dropped_list, axis=1)


def rename_column(column) -> str:
    names = {
        'X10_meter_sprint_beste': '10 Meter sprint',
        'X20_meter_sprint_beste': '20 Meter sprint',
        'X30_meter_sprint_beste': '30 Meter sprint',
        'Oog_hand_coordinatie_totaal': "Hand-oog coördinatie",
        'Zijwaarts_springen_totaal': "Zijwaarts springen",
        'Zijwaarts_verplaatsen_totaal': "Zijwaarts verplaatsen",
        'Balance_beam_totaal': "Evenwichtsbalk",
        'CoD_links_beste': 'COD links',
        'CoD_rechts_beste': 'COD rechts',
        'Vertesprong_beste': 'Vertesprong',
    }
    return names[column]


def get_measurement_columns(df: pd.DataFrame) -> list[str]:
    # #Get the columns that have the actual measurement
    measurement_columns = list(set(df.columns.values).symmetric_difference(META_COLUMNS))
    measurements = sorted([col for col in measurement_columns if any(x in col for x in ['beste', 'totaal'])])
    measurements.reverse()
    return measurements
