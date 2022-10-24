# Import libraries
from dash import Dash, html, dcc, Input, Output
import base64
import pandas as pd
import plotly.express as px

# Load the dataset
df = pd.read_csv("matches.csv")

# Create the Dash app
app = Dash()

# Set up the app layout
date_dropdown = dcc.Dropdown(options=df['team'].unique(),
                            value='Ajax')

app.layout = html.Div(children=[  
    html.H1(children='Uitslagen per geselecteerd voetbal team seizoen 2021-2022'),
    date_dropdown,
    dcc.Graph(id='bar-graph',) 
])

# Set up the callback function
@app.callback(
    Output(component_id='bar-graph', component_property='figure'),
    Input(component_id=date_dropdown, component_property='value')
)
def update_graph(team):
    filtered_date_time = df[df['team'] == team]
    bar_fig = px.bar(filtered_date_time,
                       x='result', y='date',
                       color='opponent',
                       title=f'Uitslagen van {team}')
    return bar_fig


# Run local server
if __name__ == '__main__':
    app.run_server(debug=True)
