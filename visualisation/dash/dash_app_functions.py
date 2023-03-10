import itertools
import pandas as pd
import plotly_express as px

META_COLUMNS = ['id', 'bvo_naam', 'seizoen', 'Testdatum', 'reeks_naam', 'team_naam', 'display_name', 'speler_id',
                'geboortedatum', 'Staande_lengte']


def calculate_mean_results_by_date_per_lichting(df: pd.DataFrame, columns):
    df_mean: pd.DataFrame = df.groupby(['Testdatum', 'reeks_naam', 'lichting'])[columns].mean(numeric_only=False).reset_index()
    df_mean.index = df_mean['Testdatum']
    return [(lichting, df) for lichting, df in df_mean.groupby('lichting')]


def calculate_mean_result_by_date(df: pd.DataFrame, columns):
    lichting = pd.to_datetime(df["geboortedatum"])
    df['lichting'] = lichting.dt.year

    df_mean: pd.DataFrame = df.groupby(['Testdatum', 'reeks_naam', 'lichting'])[columns].mean(numeric_only=False)
    df_mean = df_mean.reset_index()
    df_mean.index = df_mean['Testdatum']
    return df_mean


def calculate_result_by_date(df: pd.DataFrame, columns, groupingBy) -> pd.DataFrame:
    grouped = df.groupby(['Testdatum', 'reeks_naam'])[columns]
    if 'mediaan' == groupingBy:
        df_grouped: pd.DataFrame = grouped.median(numeric_only=True).reset_index()
    else:
        df_grouped: pd.DataFrame = grouped.mean(numeric_only=True).reset_index()
    df_grouped.index = df_grouped['Testdatum']
    return df_grouped


def aggregate_measurement_by_team_result(dashboard_data: pd.DataFrame, statistics: list) -> pd.DataFrame:
    df = dashboard_data.copy()

    # Columns to group by
    group = ['team_naam', 'reeks_naam']
    measurements = get_measurement_columns(df)
    columns = measurements + group

    # Group once not twice
    grouped = df[columns].groupby(group)
    aggregators = set(statistics) - (set(statistics) - {'gemiddelde', 'mediaan'})

    for aggregator in aggregators:
        if 'mediaan' == aggregator:
            df_grouped: pd.DataFrame = grouped.median(numeric_only=True).reset_index()
        else:
            df_grouped: pd.DataFrame = grouped.mean(numeric_only=True).reset_index()

        mapping = {column_name: column_name + f'.{aggregator}' for column_name in measurements}
        result = df_grouped[columns].rename(columns=mapping)
        df = pd.merge(left=df, right=result, how='inner')

    return df


def get_colormap(index_selector) -> str:
    return f"{px.colors.qualitative.Set1[index_selector]}"


def transform_into_labels(df: pd.DataFrame) -> dict:
    df_ticktext = df[['seizoen', 'reeks_naam']].drop_duplicates()

    # Resulting string: "23/24, voorjaar"
    ticktext = [f"""{row.seizoen.removeprefix('20')}, {row.reeks_naam}""" for row in df_ticktext.itertuples()]
    tickvals = df['Testdatum'].unique()
    return dict(tickmode='array', tickvals=tickvals, ticktext=ticktext)



def filter_bloc_tests(dashboard_data: pd.DataFrame, bloc_test_selection: list) -> pd.DataFrame:
    # This dictionary will be used to lookup BLOC-test specific rows
    columns = {"Evenwichtsbalk": ["Balance_Beam_3cm", "Balance_Beam_4_5cm", "Balance_Beam_6cm", "Balance_beam_totaal"],
               "Zijwaarts springen": ["Zijwaarts_springen_1", "Zijwaarts_springen_2", "Zijwaarts_springen_totaal"],
               "Zijwaarts verplaatsen": ["Zijwaarts_verplaatsen_1", "Zijwaarts_verplaatsen_2",
                                         "Zijwaarts_verplaatsen_totaal"],
               "Hand-oog co??rdinatie": ["Oog_hand_coordinatie_1", "Oog_hand_coordinatie_2",
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


def rename_column(column: str) -> str:
    names = {
        'X10_meter_sprint_beste': '10 Meter sprint',
        'X20_meter_sprint_beste': '20 Meter sprint',
        'X30_meter_sprint_beste': '30 Meter sprint',
        'Oog_hand_coordinatie_totaal': "Hand-oog co??rdinatie",
        'Zijwaarts_springen_totaal': "Zijwaarts springen",
        'Zijwaarts_verplaatsen_totaal': "Zijwaarts verplaatsen",
        'Balance_beam_totaal': "Evenwichtsbalk",
        'CoD_links_beste': 'COD links',
        'CoD_rechts_beste': 'COD rechts',
        'Vertesprong_beste': 'Vertesprong',
    }

    column_suffix = None
    if any(x in column for x in ['.mediaan', '.gemiddelde']):
        column, column_suffix = column.split('.')

    renamed_column = names[column]
    return renamed_column if column_suffix is None else renamed_column + " " + column_suffix


def get_measurement_columns(df: pd.DataFrame):
    # #Get the columns that have the actual measurement
    measurement_columns = list(set(df.columns.values).symmetric_difference(META_COLUMNS))
    measurements = sorted([col for col in measurement_columns if any(x in col for x in ['beste', 'totaal'])])
    measurements.reverse()
    return measurements


def drop_mean_and_median_columns(df: pd.DataFrame) -> pd.DataFrame:
    measurement_columns = list(set(df.columns.values).symmetric_difference(META_COLUMNS))
    columns_to_drop = [col for col in measurement_columns if any(x in col for x in ['.mediaan', '.gemiddelde'])]
    return df.drop(columns_to_drop, axis=1)


def split_last_word_from_string(sentence: str) -> tuple[str, str]:
    as_list = sentence.split(' ')
    last = as_list[len(as_list) - 1]
    as_list.remove(last)
    return ' '.join(as_list), last


def get_unique_values(df: pd.DataFrame, columns) -> dict:
    unique = dict()
    for column in columns:
        unique.update({f'{column}': sorted([column_values for column_values in df[column].unique()])})
    return unique


def get_filter_options_or_default(df: pd.DataFrame, get_options_for: str, according_to: list[tuple[str, list]], otherwise_default_to: dict):
    key1, value1 = according_to[0]
    key2, value2 = according_to[1]
    if value1 and value2:
        return df[df[key1].isin([value1]) & df[key2].isin([value2])][get_options_for].unique()
    elif value1:
        return df[df[key1].isin([value1])][get_options_for].unique()
    elif value2:
        return df[df[key2].isin([value2])][get_options_for].unique()
    else:
        return otherwise_default_to[get_options_for]
