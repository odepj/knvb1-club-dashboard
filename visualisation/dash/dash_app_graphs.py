import plotly.graph_objects as go
import regex as re
from numpy import int64

from visualisation.dash.dash_app_functions import *
from plotly.subplots import make_subplots


def create_boxplot(individuen, dataframe: pd.DataFrame, selected_dashboard) -> go.box:
    dataframe.sort_values(['team_naam'], inplace=True)
    extra_columns = dataframe.filter(regex='.mediaan|.gemiddelde').columns.values
    selected_columns = dataframe[get_measurement_columns(dataframe)]
    selected_columns = drop_mean_and_median_columns(selected_columns)
    measurements = selected_columns.columns.values.tolist()

    fig = go.Figure()
    for column in selected_columns:
        column_name = rename_column(column)

        fig.add_trace(go.Box(
            x=dataframe['team_naam'],
            y=dataframe[column],
            name=column_name,
            boxpoints=individuen,
            line=dict(color=get_colormap(measurements.index(column))),
            showlegend=True
        ))

    for extra_column in extra_columns:
        if re.search('.mediaan', extra_column):
            marker_color = "black"
        elif re.search('.gemiddelde', extra_column):
            marker_color = "orange"

        column_name = rename_column(extra_column)
        marker_df = dataframe.groupby('team_naam')[[extra_column]].mean().reset_index()

        fig.add_trace(go.Scatter(
            x=marker_df['team_naam'],
            y=marker_df.iloc[:, 1],
            name=column_name,
            mode="markers",
            showlegend=True,
            marker=dict(size=70, symbol="line-ew", line=dict(width=3, color=marker_color))))

    if selected_dashboard != "sprint":
        title_text = "<b>Vergelijking van teams<b>"
        yaxis_title = "Beste van totaal resultaat"
    else:
        title_text = "<b>Sprint vergelijking van teams<b>"
        yaxis_title = "sprint score"

    fig.update_layout(title_text=title_text, autosize=True, yaxis_title=yaxis_title, xaxis_title="Team naam")

    return fig


def build_line_chart(dataframe, statistics):
    # Get all measurement and statistical columns and calculate the mean values for each 'lichting'
    extra_columns = dataframe.filter(regex='.mediaan|.gemiddelde').columns.values
    lichting_columns = sorted(list(set(get_measurement_columns(dataframe)) - set(extra_columns)))
    lichting_data = calculate_mean_results_by_date_per_lichting(dataframe, lichting_columns)

    # line types and colors for the 'lichting' traces
    line_types = ['solid', 'dot', 'longdashdot', 'dashdot', 'longdash']
    color_map = [get_colormap(i) for i in range(0, len(lichting_data))]

    # line types for the statistical traces
    statistical_line_types = {'gemiddelde': 'solid', 'mediaan': 'dot'}

    line = go.Figure(layout=go.Layout(autosize=True))
    box = go.Figure(layout=go.Layout(autosize=True))

    for idx, (lichting, df_lichting) in enumerate(lichting_data):
        for jdx, measurement in enumerate(lichting_columns):
            column_name = rename_column(measurement)
            line.add_trace(go.Scatter(
                x=df_lichting.index,
                y=df_lichting[measurement],
                name=lichting,
                legendgroup=column_name,
                legendgrouptitle=dict(text=column_name),
                mode='lines+markers',
                line=dict(color=color_map[idx], dash=line_types[jdx], width=3, shape='spline'),
            ))

            if "boxplot" in statistics:
                box.add_trace(go.Box(
                    x=df_lichting["lichting"],
                    y=df_lichting[measurement],
                    name=column_name,
                    showlegend=True,
                    legendgroup=column_name,
                    line=dict(color=get_colormap(lichting_columns.index(measurement))))
                )

                # make sure that there is only one of the names in the legend
                names = set()
                box.for_each_trace(
                    lambda trace: trace.update(showlegend=False)
                    if (trace.name in names) else names.add(trace.name))

    names = list(sorted(set([split_last_word_from_string(rename_column(extra_column))[0] for extra_column in extra_columns])))
    for idx, extra_column in enumerate(extra_columns):
        if re.search('.mediaan', extra_column):
            marker_color = "black"
        elif re.search('.gemiddelde', extra_column):
            marker_color = "orange"

        column_name, column_type = split_last_word_from_string(rename_column(extra_column))
        df = calculate_result_by_date(dataframe, extra_columns, extra_column)
        line.add_trace(go.Scatter(
            x=df.index,
            y=df[extra_column],
            name=column_name,
            legendgroup=column_name,
            legendgrouptitle=dict(text=column_name),
            mode='lines+markers',
            line=dict(color=marker_color, dash=line_types[names.index(column_name)], width=3, shape='spline'),
        ))

    # y_axis title based on whether the scoring is in points or some other unit of measure
    if len(lichting_columns) > 0:
        predicate = dataframe[lichting_columns[0]].dtype == int64
        yaxis_title = 'Totaal score (punten)' if predicate else 'Beste of totaal resultaat'
    else:
        yaxis_title = 'Geen selectie'

    line.update_layout(
        xaxis=transform_into_labels(dataframe),
        yaxis_title=yaxis_title,
        xaxis_title='Meet moment',
        title_text="<b>Ontwikkeling lichtingen<b>"
    )

    if "boxplot" in statistics:
        fig = make_subplots(rows=2, cols=1, y_title=yaxis_title)
        fig.add_traces(line.data, rows=1, cols=1)
        fig.add_traces(box.data, rows=2, cols=1)
        fig.update_layout(title_text="<b>Ontwikkeling lichtingen<b>")

        # edit axis labels
        fig['layout']['xaxis']['title'] = 'Meet moment'
        fig['layout']['xaxis2']['title'] = 'Lichting'

        return fig

    return line


# This method is used to get the total BLOC-score per team_naam, reeks_naam and club code/name
def _calculate_sum(dataframe: pd.DataFrame) -> pd.DataFrame:
    team_player_counts = dataframe.groupby("team_naam")["speler_id"].nunique().to_dict()
    dataframe = dataframe.groupby(["team_naam", "reeks_naam", "bvo_naam", "display_name"]).sum(
        numeric_only=True).reset_index()
    dataframe["team_player_count"] = dataframe["team_naam"].map(team_player_counts)
    dataframe.set_index(list(dataframe.select_dtypes(include="object").columns.values), inplace=True)

    return dataframe.iloc[:, :-1].div(dataframe["team_player_count"], axis=0).reset_index()


def create_chart(dataframe: pd.DataFrame) -> px.bar:
    dataframe = drop_mean_and_median_columns(dataframe)

    # Get the filtered sum data, columns containing total values and club name
    filtered_data = _calculate_sum(dataframe).round(decimals=2)
    total_columns = filtered_data.filter(regex='totaal').columns

    # Create a bar chart using the filtered data and add additional styling
    fig = px.bar(filtered_data, x='team_naam', y=total_columns,
                 title="<b>Opbouw scores BLOC test<b>", color_discrete_map=
                 {'Zijwaarts_verplaatsen_totaal': get_colormap(0),
                  'Zijwaarts_springen_totaal': get_colormap(1),
                  'Oog_hand_coordinatie_totaal': get_colormap(2),
                  'Balance_beam_totaal': get_colormap(3), })

    fig.update_layout(yaxis_title='Totaal score (punten)', xaxis_title='Team',
                      barmode='stack', legend_title="BLOC-testen")

    # rename every BLOC test variable to readable names for the legend and bars using the test_names dictionary
    fig.for_each_trace(lambda t: t.update(name=rename_column(t.name)))

    return fig
