import pandas as pd
import plotly.express as px

from visualisation.dashboard_template_functions import drop_mean_and_median_columns

# This dictionary will be used to lookup BLOC-test specific rows
columns = {"Evenwichtsbalk": ["Balance_Beam_3cm", "Balance_Beam_4_5cm", "Balance_Beam_6cm", "Balance_beam_totaal"],
           "Zijwaarts springen": ["Zijwaarts_springen_1", "Zijwaarts_springen_2", "Zijwaarts_springen_totaal"],
           "Zijwaarts verplaatsen": ["Zijwaarts_verplaatsen_1", "Zijwaarts_verplaatsen_2", "Zijwaarts_verplaatsen_totaal"],
           "Hand-oog coördinatie": ["Oog_hand_coordinatie_1", "Oog_hand_coordinatie_2", "Oog_hand_coordinatie_totaal"]}

# This dictionary will be used to rename the axises in the chart
test_names = {"Balance_beam_totaal": "Evenwichtsbalk",
              "Zijwaarts_springen_totaal": "Zijwaarts springen",
              "Zijwaarts_verplaatsen_totaal": "Zijwaarts verplaatsen",
              "Oog_hand_coordinatie_totaal": "Hand-oog coördinatie"}


# This method is used to get the total BLOC-score per team_naam, reeks_naam and club code/name
def _calculate_sum(dataframe: pd.DataFrame) -> pd.DataFrame:
    team_player_counts = dataframe.groupby("team_naam")["speler_id"].nunique().to_dict()
    dataframe = dataframe.groupby(["team_naam", "reeks_naam", "bvo_naam", "display_name"]).sum().reset_index()
    dataframe["team_player_count"] = dataframe["team_naam"].map(team_player_counts)
    dataframe.set_index(list(dataframe.select_dtypes(include="object").columns.values), inplace=True)
    
    return dataframe.iloc[:,:-1].div(dataframe["team_player_count"], axis=0).reset_index()


def create_chart(dataframe: pd.DataFrame) -> px.bar:
    dataframe = drop_mean_and_median_columns(dataframe)

    # Get the filtered sum data, columns containing total values and club name
    filtered_data = _calculate_sum(dataframe).round(decimals=2)
    total_columns = filtered_data.filter(regex='totaal').columns
    #club = filtered_data["display_name"].get(0, "Geen club beschikbaar")

    # Get all the details on demand columns from the columns dictionary that are not in the total_columns
    # TEMPORARY solution, please check algemene_dashboard.py for the dynamic version of these lines of code
    #tests = ["Evenwichtsbalk", "Zijwaarts springen",
    #         "Zijwaarts verplaatsen", "Hand-oog coördinatie"]
#
    #details_on_demand = [columns.get(test)
    #                     for test in tests if test in columns]
    #details_on_demand.insert(0, ["display_name", "bvo_naam", "reeks_naam"])
    #details_on_demand = list(filter(lambda x: (x not in total_columns),
                                    #numpy.concatenate(details_on_demand).flat))

    hover_template = """Club naam: %{customdata[0]} <br>Club code: %{customdata[1]}
        <br>Team: %{x} <br>Totaal score: %{y} punten <br>Meting: %{customdata[2]}
        <br><br>BLOC-test specifieke totaal scores:<br>"""

    # Generate a hover_template for details on the demand by looping over the available details
    #for i in range(3, len(details_on_demand)):
    #    hover_template += f"{details_on_demand[i]}: %{{customdata[{i}]}} punten<br>"

    # Create a bar chart using the filtered data and add additional styling and hover information
    fig = px.bar(filtered_data, x='team_naam', y=total_columns,
                 title="<b>Opbouw scores BLOC test<b>",)

    fig.update_layout(yaxis_title='Totaal score (punten)', xaxis_title='Team',
                      barmode='stack', legend_title="BLOC-testen")

    #fig.update_traces(hovertemplate=hover_template)

    # rename every BLOC test variable to readable names for the legend and bars using the test_names dictionary
    fig.for_each_trace(lambda t: t.update(name=test_names[t.name]))

    return fig
