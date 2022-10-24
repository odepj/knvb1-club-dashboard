import pandas as pd
import plotly.express as px
from plotly.utils import PlotlyJSONEncoder
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json


def create_default_scatterplot(data, column_names, x, y, color, hover_data, labels):
    df = pd.DataFrame([[ij for ij in i] for i in data])
    df.rename(columns=column_names,
              inplace=True)
    df.sort_values(by=['id'], ascending=[1])

    fig: px.scatter = px.scatter(
        df, x=x, y=y, color=color, hover_data=hover_data, labels=labels)

    return json.dumps(fig, cls=PlotlyJSONEncoder)


def vertesprong(data):
    column_names = {0: 'id', 1: 'Vertesprong_1', 2: 'Vertesprong_2',
                    3: 'Vertesprong_beste', 4: 'Staande_lengte'}
    x = 'Staande_lengte'
    y = 'Vertesprong_beste'
    color = 'Vertesprong_beste'
    hover_data = ['Vertesprong_1', 'Vertesprong_2', 'id']
    labels = {"Staande_lengte": "Staande lengtes in centimeters",
              "Vertesprong_beste": "Vertesprong in meters"}

    return create_default_scatterplot(
        data, column_names, x, y, color, hover_data, labels)


def zijwaarts_springen(data):
    column_names = {0: 'id', 1: 'Zijwaarts_springen_1', 2: 'Zijwaarts_springen_2',
                    3: 'Zijwaarts_springen_totaal', 4: 'Staande_lengte'}
    x = 'Staande_lengte'
    y = 'Zijwaarts_springen_totaal'
    color = 'Zijwaarts_springen_totaal'
    hover_data = ['Zijwaarts_springen_1', 'Zijwaarts_springen_2', 'id']
    labels = {"Staande_lengte": "Staande lengtes in centimeters",
              "Zijwaarts_springen_totaal": "Zijwaarts springen in meters"}

    return create_default_scatterplot(
        data, column_names, x, y, color, hover_data, labels)


def hand_oog_coordinatie(data):
    column_names = {0: 'id', 1: 'Oog_hand_coordinatie_1', 2: 'Oog_hand_coordinatie_2',
                       3: 'Oog_hand_coordinatie_Totaal', 4: 'Lengte_bovenlichaam'}
    x = 'Lengte_bovenlichaam'
    y = 'Oog_hand_coordinatie_Totaal'
    color = 'Oog_hand_coordinatie_Totaal'
    hover_data = ['Oog_hand_coordinatie_1',
                  'Oog_hand_coordinatie_2', 'id']
    labels = {
        "Lengte_bovenlichaam": "Lengte bovenlichaam in centimeters",
        "Oog_hand_coordinatie_Totaal": "Hand Oog Coordinatie Totaal"
    }

    return create_default_scatterplot(
        data, column_names, x, y, color, hover_data, labels)


def evenwichtsbalk(data):
    column_names = {0: 'id', 1: 'Balance_Beam_6cm', 2: 'Balance_Beam_4_5cm',
                       3: 'Balance_Beam_3cm', 4: 'Balance_beam_totaal', 5: 'Staande_lengte'}
    x = 'Staande_lengte'
    y = 'Balance_beam_totaal'
    color = 'Balance_beam_totaal'
    hover_data = ['Balance_Beam_3cm',
                  'Balance_Beam_4_5cm', 'Balance_Beam_6cm', 'id']
    labels = {
        "Staande_lengte": "Staande lengtes in centimeters",
        "Balance_beam_totaal": "Balance Beam Totaal"
    }

    return create_default_scatterplot(
        data, column_names, x, y, color, hover_data, labels)


def zijwaarts_verplaatsen(data):
    column_names = {0: 'id', 1: 'Staande_lengte', 2: 'Zijwaarts_verplaatsen_1',
                    3: 'Zijwaarts_verplaatsen_2', 4: 'Zijwaarts_verplaatsen_totaal'}
    x = 'Staande_lengte',
    y = 'Zijwaarts_verplaatsen_totaal',
    color = 'Zijwaarts_verplaatsen_totaal',
    hover_data = ['Zijwaarts_verplaatsen_1',
                  'Zijwaarts_verplaatsen_2', 'id'],
    labels = {
        "Staande_lengte": "Staande lengtes in centimeters",
        "Zijwaarts_verplaatsen_totaal": "Zijwaarts verplaatsen Totaal"
    }
    return create_default_scatterplot(
        data, column_names, x, y, color, hover_data, labels)


def sprinten(data):
    df = pd.DataFrame([[ij for ij in i] for i in data])
    df.rename(columns={0: 'id', 1: '10_meter_sprint_1', 2: '10_meter_sprint_2', 3: '10_meter_sprint_beste',
                       4: '20_meter_sprint_1', 5: '20_meter_sprint_2', 6: '20_meter_sprint_beste',
                       7: '30_meter_sprint_1', 8: '30_meter_sprint_2', 9: '30_meter_sprint_beste',
                       10: 'Staande_lengte'},
              inplace=True)
    df.sort_values(by=['id'], ascending=[1])

    fig = make_subplots(
        rows=3, cols=1,
        subplot_titles=('Sprint 10 meter', 'Sprint 20 meter',
                        'Sprint 30 meter'),
        shared_yaxes=True)

    fig.append_trace(go.Scatter(
        y=df['10_meter_sprint_beste'],
        x=df['Staande_lengte'],
        mode='markers',
        marker=dict(color=df['10_meter_sprint_beste'], coloraxis='coloraxis')
    ), row=1, col=1)

    fig.append_trace(go.Scatter(
        y=df['20_meter_sprint_beste'],
        x=df['Staande_lengte'],
        mode='markers',
        marker=dict(color=df['20_meter_sprint_beste'], coloraxis='coloraxis')
    ), row=2, col=1)

    fig.append_trace(go.Scatter(
        y=df['30_meter_sprint_beste'],
        x=df['Staande_lengte'],
        mode='markers',
        marker=dict(color=df['30_meter_sprint_beste'], coloraxis='coloraxis')
    ), row=3, col=1)

    fig.update_layout(height=600, width=800,
                      title_text="Snelheden per afstand", showlegend=False)

    return json.dumps(fig, cls=PlotlyJSONEncoder)


def change_of_direction(data):
    df = pd.DataFrame([[ij for ij in i] for i in data])
    df.rename(columns={0: 'id', 1: 'Staande_lengte', 2: 'CoD_links_1', 3: 'CoD_links_2', 4: 'CoD_links_beste',
                       5: 'CoD_rechts_1', 6: 'CoD_rechts_2', 7: 'CoD_rechts_beste'},
              inplace=True)
    df = df.sort_values(by=['id'], ascending=[1])

    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('CoD_links_beste', 'CoD_rechts_beste'),
        shared_yaxes=True)

    fig.append_trace(go.Scatter(
        y=df['CoD_links_beste'],
        x=df['Staande_lengte'],
        mode='markers',
        marker=dict(color=df['CoD_links_beste'], coloraxis='coloraxis')
    ), row=1, col=1)

    fig.append_trace(go.Scatter(
        y=df['CoD_rechts_beste'],
        x=df['Staande_lengte'],
        mode='markers',
        marker=dict(color=df['CoD_rechts_beste'], coloraxis='coloraxis')
    ), row=1, col=2)

    fig.update_layout(height=600, width=800,
                      title_text="CoD per been", showlegend=False)

    return json.dumps(fig, cls=PlotlyJSONEncoder)
