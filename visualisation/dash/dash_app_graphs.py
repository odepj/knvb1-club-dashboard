import plotly.graph_objects as go
from plotly.subplots import make_subplots

from visualisation.dash.dash_app_functions import *


def create_boxplot(individuen, dataframe: pd.DataFrame) -> go.box:
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
        column_name = rename_column(extra_column)
        fig.add_trace(go.Scatter(
            x=dataframe['team_naam'],
            y=dataframe[extra_column],
            name=column_name,
            mode="markers",
            showlegend=True,
            marker=dict(size=80, symbol="line-ew", line=dict(width=2, color="red")))),

    return fig


def create_box(individuen, dataframe: pd.DataFrame) -> go.Box:
    fig = create_boxplot(individuen, dataframe)
    fig.update_layout(title_text="<b>Vergelijking van teams<b>", autosize=True)
    fig.update_layout(yaxis_title="Beste van totaal resultaat")
    fig.update_layout(xaxis_title="team naam")
    return fig


def create_boxplot_function(individuen, dataframe: pd.DataFrame) -> go.Box:
    fig = create_boxplot(individuen, dataframe)
    fig.update_layout(title_text="<b>Sprint vergelijking van teams<b>", autosize=True)
    fig.update_layout(yaxis_title="sprint score")
    fig.update_layout(xaxis_title="team naam")
    return fig


def create_line(filter_output, dashboard_data, statistics):
    dashboard_data = pd.DataFrame(dashboard_data)
    filter_output = drop_mean_and_median_columns(pd.DataFrame(filter_output))
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
        xaxis=fix_labels(filter_output),
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

# This dictionary will be used to lookup BLOC-test specific rows
columns = {"Evenwichtsbalk": ["Balance_Beam_3cm", "Balance_Beam_4_5cm", "Balance_Beam_6cm", "Balance_beam_totaal"],
           "Zijwaarts springen": ["Zijwaarts_springen_1", "Zijwaarts_springen_2", "Zijwaarts_springen_totaal"],
           "Zijwaarts verplaatsen": ["Zijwaarts_verplaatsen_1", "Zijwaarts_verplaatsen_2",
                                     "Zijwaarts_verplaatsen_totaal"],
           "Hand-oog coördinatie": ["Oog_hand_coordinatie_1", "Oog_hand_coordinatie_2", "Oog_hand_coordinatie_totaal"]}

# This dictionary will be used to rename the axises in the chart
test_names = {"Balance_beam_totaal": "Evenwichtsbalk",
              "Zijwaarts_springen_totaal": "Zijwaarts springen",
              "Zijwaarts_verplaatsen_totaal": "Zijwaarts verplaatsen",
              "Oog_hand_coordinatie_totaal": "Hand-oog coördinatie"}


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

    # Create a bar chart using the filtered data and add additional styling and hover information
    fig = px.bar(filtered_data, x='team_naam', y=total_columns,
                 title="<b>Opbouw scores BLOC test<b>", )

    fig.update_layout(yaxis_title='Totaal score (punten)', xaxis_title='Team',
                      barmode='stack', legend_title="BLOC-testen")

    # rename every BLOC test variable to readable names for the legend and bars using the test_names dictionary
    fig.for_each_trace(lambda t: t.update(name=test_names[t.name]))

    return fig
