import pandas as pd
import plotly.express as px
pd.options.mode.chained_assignment = None 

# This list will be used to lookup BLOC-test specific rows
columns_list = ["display_name", "bvo_naam", "seizoen", "lichting",
                "Balance_Beam_3cm", "Balance_Beam_4_5cm", "Balance_Beam_6cm", 
                "Zijwaarts_springen_1", "Zijwaarts_springen_2",
                "Zijwaarts_verplaatsen_1", "Zijwaarts_verplaatsen_2",
                "Oog_hand_coordinatie_1", "Oog_hand_coordinatie_2",]

# This dictionary will be used to rename the axises in the chart
test_names = {"Balance_beam_totaal": "Evenwichtsbalk",
              "Zijwaarts_springen_totaal": "Zijwaarts springen",
              "Zijwaarts_verplaatsen_totaal": "Zijwaarts verplaatsen",
              "Oog_hand_coordinatie_totaal": "Hand-oog coördinatie"}

# This method is used to get the total BLOC-score per seizoen, team, lichting and club
def _calculate_sum(dataframe: pd.DataFrame) -> pd.DataFrame:
    dataframe["geboortedatum"] = pd.to_datetime(dataframe["geboortedatum"])
    dataframe["lichting"] = dataframe["geboortedatum"].dt.year.astype(str)

    team_player_counts = dataframe.groupby("team_naam")["speler_id"].nunique().to_dict()
    dataframe = dataframe.groupby(["team_naam", "reeks_naam", "bvo_naam", 
        "display_name","seizoen", "lichting"]).agg('sum').reset_index()

    dataframe["team_player_count"] = dataframe["team_naam"].map(team_player_counts)
    dataframe.set_index(list(dataframe.select_dtypes(include="object").columns.values), inplace=True)
    return dataframe.iloc[:,:-1].div(dataframe["team_player_count"], axis=0).reset_index()

def create_chart(dataframe: pd.DataFrame) -> px.bar:
    # Get the filtered sum data, columns containing total values and club name
    filtered_data = _calculate_sum(dataframe).round(decimals=2)
    total_columns = filtered_data.filter(regex='totaal').columns
    club = filtered_data["display_name"].get(0, "Geen club beschikbaar")

    details_on_demand = [column for column in columns_list if column in dataframe.columns]
    hover_template = """Club naam: %{customdata[0]} <br>Club code: %{customdata[1]}
        <br>Team: %{x} <br>Totaal score: %{y} punten <br>Seizoen: %{customdata[2]} 
        <br>Lichting: %{customdata[3]}<br><br>BLOC-test specifieke totaal scores:<br>"""

    # Generate a hover_template for details on the demand by looping over the available details
    for i in range(4, len(details_on_demand)):
        hover_template += f"{details_on_demand[i]}: %{{customdata[{i}]}} punten<br>"

    # Create a bar chart using the filtered data and add additional styling and hover information
    fig = px.bar(filtered_data, x='team_naam', y=total_columns, custom_data=details_on_demand,
                 title=f"BLOC-test totaal score spelers per team voor uw club: {club}")

    fig.update_layout(yaxis_title='Totaal score (punten)', xaxis_title='Team',
                      barmode='stack', legend_title="BLOC-testen", title_x=0.5)

    fig.update_traces(hovertemplate=hover_template)

    # rename every BLOC test variable to readable names for the legend and bars using the test_names dictionary
    fig.for_each_trace(lambda t: t.update(name=test_names[t.name]))

    return fig
