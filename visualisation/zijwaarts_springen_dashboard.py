import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from database.database import get_zijwaarts_springen
from visualisation.uitl_functions import add_figure_rangeslider, calculate_delta, group_team_and_club


# Retrieve data from DB.
data = get_zijwaarts_springen()
club_id = 'EoYnc'  # This is a big problem
club = None
col = 'Zijwaarts_springen_totaal'

mean = group_team_and_club(data.drop_duplicates())
if club_id is not None:
    club = group_team_and_club(data[data['club_code'] == club_id].drop_duplicates())
else:
    result = mean

fig = go.Figure()
fig.add_trace(go.Scatter(x=mean.index, y=mean[col]))
fig.add_trace(go.Scatter(x=club.index, y=club[col]))
fig = add_figure_rangeslider(fig)

graph = dbc.Col(dcc.Graph(id='zijwaarts-springen-graph', figure=fig), width=10)

s, f = mean[col], club[col]
delta_s = calculate_delta(s, from_=s.iloc[:1].index, to_=s.iloc[-1:].index)
delta_f = calculate_delta(f, from_=f.iloc[:1].index, to_=f.iloc[-1:].index)
card = dbc.Card(
    [
        html.H5('Groei delta', style={'margin-top': '5px'}),
        html.Span(f'Team {club_id}:'),
        html.Em(f"{delta_f}%"),
        html.Span('Landelijk gemiddelde:'),
        html.Em(f"{delta_s}%"),
    ], className='col-2'
)


# This method is used by the app.py to initialize the Dash dashboard in Flask
# This workaround allows us to use Dash inside a Flask app by using its own route
def init_vs_dashboard(server):
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dashboard/dash/zijwaartsspringen/',
        external_stylesheets=[dbc.themes.BOOTSTRAP]
    )

    dash_app.layout = html.Main([dbc.Row([graph, card])])

    # Callbacks for the Dash dashboard are initialized here after the creation of the layout has been completed
    init_callbacks(dash_app)

    return dash_app.server


# This method is used to create and initialize callbacks that will be used by the charts or selection items
def init_callbacks(dash_app):
    return None
