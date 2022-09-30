import pandas as pd
import plotly.graph_objects as go

#Read csv file with pandas
han_data = pd.read_csv('HAN_csv_example.csv', index_col=0, sep=',')

#Drop empty columns
han_data = han_data.drop("Maturity.Offset", axis=1)

#Checking unique groups for splitting DataFrame
column_values = han_data[["team_id"]].values.ravel()
print(pd.unique(column_values))

han_data_per_team = han_data.groupby("team_id")

for team_id, han_data in han_data_per_team:
    #Create a correlation table
    han_data_corr = han_data.corr(method='pearson')

    #Set up the correlation plot
    fig = go.Figure(go.Heatmap(
        z=han_data_corr.values.tolist(),
        x=han_data_corr.columns,
        y=han_data_corr.columns, 
        colorscale='rdylgn',
        zmin=-1, zmax=1
))  

    fig.update_layout(
        title_text=team_id
    )

    fig.show()