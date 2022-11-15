import dash
from dash import html, Input, Output, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from database.database import get_zijwaarts_springen, session

from visualisation.figure_builder import line_figure_builder, indicator_builder, add_figure_rangeslider


def get_club_id():
    try:
        return session.get('id')
    except:
        return None


def group_team_and_club(df: pd.DataFrame):
    if df['club_code'].nunique() > 1:
        club_code = 'mean'

    else:
        club_code = df['club_code'].drop_duplicates().values[0]

    df_mean = df.groupby(['datum', 'meting']).mean(numeric_only=False)
    df_mean['club_code'] = club_code
    df_mean['meting'], df_mean.index = df_mean.index.droplevel(0), df_mean.index.droplevel(1)
    return df_mean


# Retrieve data from DB.
data = get_zijwaarts_springen()
club_id = 'EoYnc'  # This is a big problem
club = None

mean = group_team_and_club(data.drop_duplicates())
if club_id is not None:
    club = group_team_and_club(data[data['club_code'] == club_id].drop_duplicates())
    # result = pd.concat([club, mean], axis=0)
else:
    result = mean

fig = go.Figure()
fig.add_trace(go.Scatter(x=mean.index, y=mean['Zijwaarts_springen_totaal']))
fig.add_trace(go.Scatter(x=club.index, y=club['Zijwaarts_springen_totaal']))
# fig.add_trace(line_figure_builder(mean, x=mean.index, y=['Zijwaarts_springen_totaal'], color='club_code'))
fig = add_figure_rangeslider(fig)

indicator1 = go.Figure().add_trace(indicator_builder(mean, delta='Zijwaarts_springen_totaal', name='me2an'))
indicator2 = go.Figure().add_trace(indicator_builder(club, delta='Zijwaarts_springen_totaal', name=club_id))

indicator = go.Figure()
# indicator.add_trace(indicator_builder(mean, delta='Zijwaarts_springen_totaal', name='mean'))
if club is not None:
    indicator.add_trace(indicator_builder(club, delta='Zijwaarts_springen_totaal', name=club_id))


print('h')
# This method is used by the app.py to initialize the Dash dashboard in Flask
# This workaround allows us to use Dash inside a Flask app by using its own route
def init_vs_dashboard(server):
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dashboard/dash/zijwaartsspringen/',
        external_stylesheets=[dbc.themes.BOOTSTRAP]
    )

    # All the layout items such as the dashboard's charts itself are put in this 'layout' variable below
    dash_app.layout = html.Main(
        [
            dcc.Graph(
                id='zijwaarts-springen-graph',
                figure=fig,
                # style={'width': '90%'}
            ),
            dcc.Graph(
                className='indicator',
                figure=indicator
            ),
            dcc.Graph(
                className='indicator',
                figure=indicator1
            ),
            dcc.Graph(
                className='indicator',
                figure=indicator2
            )
        ],
        # style={
        #     'display': 'flex',
        #     'flex-direction': 'row'
        # }
    )

    # Callbacks for the Dash dashboard are initialized here after the creation of the layout has been completed
    init_callbacks(dash_app)

    return dash_app.server


# This method is used to create and initialize callbacks that will be used by the charts or selection items
def init_callbacks(dash_app):
    # @dash_app.callback(Output("zijwaarts-springen-graph", "figure"), input())
    # def build_graph():
    #     return line_figure_builder(data)

    @dash_app.callback(
        Output("zijwaarts-springen-graph", 'children'),
        [Input('my-range-slider', 'value')])
    def update_output(value):
        print('You have selected "{}"'.format(value))
