import plotly.graph_objects as go
import regex as re
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
            y=marker_df.iloc[:,1],
            name=column_name,
            mode="markers",
            showlegend=True,
            marker=dict(size=70, symbol="line-ew", line=dict(width=3, color=marker_color)
            )))

    if selected_dashboard != "sprint":
        title_text = "<b>Vergelijking van teams<b>"
        yaxis_title = "Beste van totaal resultaat"
    else:
        title_text = "<b>Sprint vergelijking van teams<b>"
        yaxis_title = "sprint score"

    fig.update_layout(title_text=title_text, autosize=True, yaxis_title=yaxis_title, xaxis_title="Team naam")

    return fig


def build_line_chart(filter_output, dashboard_data, statistics):
    filter_output = pd.DataFrame(filter_output)
    dashboard_data = pd.DataFrame(dashboard_data)
    filter_output = drop_mean_and_median_columns(filter_output)
    additional_traces = list(set(statistics) - (set(statistics) - {'gemiddelde', 'mediaan'}))
    measurements = get_measurement_columns(filter_output)
    result = calculate_mean_result_by_date(filter_output, measurements)
    bundled_df = [df for _, df in result.groupby('lichting')]
    df_mean_median = [(calculate_result_by_date(dashboard_data, measurements, statistic), statistic) for statistic
                      in additional_traces]

    line = go.Figure(layout=go.Layout(autosize=True))
    box = go.Figure(layout=go.Layout(autosize=True))

    # Generate the traces for statistics
    dash_dict = {'gemiddelde': 'solid', 'mediaan': 'dot'}
    index = bundled_df[0].index
    for idx, tupy in enumerate(df_mean_median):
        df, statistic = tupy
        df = df[df.index.isin(index)]
        for jdx, measurement in enumerate(measurements):
            column_name = rename_column(measurement)
            line.add_trace(go.Scatter(
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
            line.add_trace(go.Scatter(
                x=df_lichting.index,
                y=df_lichting[measurement],
                name=name,
                legendgroup=column_name,
                legendgrouptitle=dict(text=column_name),
                mode='lines+markers',
                line_shape="spline",
                line=dict(color=get_colormap(idx), dash=dash_list[jdx], width=3),
            ))
                
            if "boxplot" in statistics:
                box.add_trace(go.Box(
                    x=df_lichting["lichting"],
                    y=df_lichting[measurement],
                    name=column_name,
                    showlegend=True,
                    legendgroup=column_name,
                    line=dict(color=get_colormap(measurements.index(measurement))))
                )

                # make sure that there is only one of the names in the legend
                names = set()
                box.for_each_trace(
                    lambda trace: trace.update(showlegend=False) 
                    if (trace.name in names) else names.add(trace.name))


    if len(measurements) > 0:
        predicate = filter_output[measurements[0]].dtype == int
        yaxis_title = 'Totaal score (punten)' if predicate else 'Beste/totaal resultaat'
    else:
        yaxis_title = 'Geen selectie'

    line.update_layout(
        xaxis=transform_into_labels(filter_output),

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
        fig['layout']['xaxis']['title']='Meet moment'
        fig['layout']['xaxis2']['title']='Lichting'

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
                 'Balance_beam_totaal': get_colormap(3),})

    fig.update_layout(yaxis_title='Totaal score (punten)', xaxis_title='Team',
                      barmode='stack', legend_title="BLOC-testen")

    # rename every BLOC test variable to readable names for the legend and bars using the test_names dictionary
    fig.for_each_trace(lambda t: t.update(name=rename_column(t.name)))

    return fig
