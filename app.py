from flask import Flask, render_template, redirect, url_for, request, session
import json
import plotly
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
from sqlalchemy import create_engine, text


app = Flask(__name__)

connect_args = {'ssl': {'fake_flag_to_enable_tls': True}}
connect_string = 'mysql+pymysql://{}:{}@{}/{}'.format('tiggele', 'h05$rzZA$.I3084I', 'oege.ie.hva.nl', 'ztiggele')
engine = create_engine(connect_string, connect_args=connect_args)

team_naam = '"Onder 13"'
app.secret_key = 'databaseproject'

@app.route('/')
def intro():
    return render_template('intro.html')


@app.route('/login', methods=['GET', 'POST']    )
def login():
    loggedin = session.get('loggedin')
    if (loggedin):
        return redirect('/dashboard')
    errorMessage = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        with engine.begin() as conn:     
            account = conn.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,)).fetchone()
            if account:
                session['loggedin'] = True
                session['id'] = account['id']
                session['username'] = account['username']
                session['displayname'] = account['displayname']
                return render_template('dashboard.html')
            else:
                errorMessage = 'Uw gebruikersnaam of wachtwoord is fout.'
    return render_template('login.html', errorMessage=errorMessage)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('displayname', None)
    return redirect(url_for('login'))


@app.route('/dashboard')
def dashboard():
    loggedin = session.get('loggedin')
    if (loggedin):
        return render_template('dashboard.html')
    else:
        return redirect('/login')


@app.route('/dashboard/verspringen', methods=['GET', 'POST'])
def visu_vertesprong():
    bvo_id = session.get('id')
    teamSelectie = request.values.get('teamSelectie')

    if teamSelectie:
        with engine.begin() as conn:
            result = conn.execute(
                text('SELECT `id`, `Vertesprong_1`, `Vertesprong_2`, `Vertesprong_beste`, `Staande_lengte`, `bvo_id`'
                     'FROM `han`'
                     f'WHERE `team_naam` = {teamSelectie} AND `bvo_id` = {bvo_id}'.format(teamSelectie=teamSelectie, bvo_id=bvo_id)))
    else:
        with engine.begin() as conn:
            result = conn.execute(
                text('SELECT `id`, `Vertesprong_1`, `Vertesprong_2`, `Vertesprong_beste`, `Staande_lengte`, `bvo_id`'
                     'FROM `han`'
                     f'WHERE `team_naam` = {team_naam} AND `bvo_id` = {bvo_id}'.format(team_naam=teamSelectie, bvo_id=bvo_id)))

    df = pd.DataFrame([[ij for ij in i] for i in result])
    df.rename(columns={0: 'id', 1: 'Vertesprong_1', 2: 'Vertesprong_2', 3: 'Vertesprong_beste', 4: 'Staande_lengte'},
              inplace=True)
    df = df.sort_values(by=['id'], ascending=[1])

    fig = px.scatter(df,
                     x='Staande_lengte',
                     y='Vertesprong_beste',
                     color='Vertesprong_beste',
                     hover_data=['Vertesprong_1', 'Vertesprong_2', 'id'],
                     labels={
                         "Staande_lengte": "Staande lengtes in centimeters",
                         "Vertesprong_beste": "Vertesprong in meters"
                     })

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header = "Vertesprong"
    if teamSelectie:
        description = f"Resultaten van de vertesprong voor de groep {teamSelectie} jaar. ".format(
            teamSelectie=teamSelectie)
    else:
        description = f"Resultaten van de vertesprong voor de groep {team_naam} jaar. ".format(team_naam=team_naam)

    conn.close()

    return render_template('dashboard/verspringen.html', graphJSON=graphJSON, header=header, description=description)


@app.route('/dashboard/sprint', methods=['GET', 'POST'])
def visu_sprint():
    bvo_id = session.get('id')
    teamSelectie = request.values.get('teamSelectie')

    if teamSelectie:
        with engine.begin() as conn:
            result = conn.execute(
                text('SELECT `id`, `X10_meter_sprint_1`, `X10_meter_sprint_2`, `X10_meter_sprint_beste`,'
                     '`X20_meter_sprint_1`, `X20_meter_sprint_2`, `X20_meter_sprint_beste`,'
                     '`X30_meter_sprint_1`, `X30_meter_sprint_2`, `X30_meter_sprint_beste`,'
                     '`Staande_lengte`, `bvo_id`'
                     'FROM `han`'
                     f'WHERE `team_naam` = {teamSelectie} AND `bvo_id` = {bvo_id}'.format(teamSelectie=teamSelectie, bvo_id=bvo_id)))
    else:
        with engine.begin() as conn:
            result = conn.execute(
                text('SELECT `id`, `X10_meter_sprint_1`, `X10_meter_sprint_2`, `X10_meter_sprint_beste`,'
                     '`X20_meter_sprint_1`, `X20_meter_sprint_2`, `X20_meter_sprint_beste`,'
                     '`X30_meter_sprint_1`, `X30_meter_sprint_2`, `X30_meter_sprint_beste`,'
                     '`Staande_lengte`, `bvo_id`'
                     'FROM `han`'
                     f'WHERE `team_naam` = {team_naam} AND `bvo_id` = {bvo_id}'.format(team_naam=team_naam, bvo_id=bvo_id)))

    df = pd.DataFrame([[ij for ij in i] for i in result])
    df.rename(columns={0: 'id', 1: '10_meter_sprint_1', 2: '10_meter_sprint_2', 3: '10_meter_sprint_beste',
                       4: '20_meter_sprint_1', 5: '20_meter_sprint_2', 6: '20_meter_sprint_beste',
                       7: '30_meter_sprint_1', 8: '30_meter_sprint_2', 9: '30_meter_sprint_beste',
                       10: 'Staande_lengte'},
              inplace=True)
    df.sort_values(by=['id'], ascending=[1])

    fig = make_subplots(
        rows=3, cols=1,
        subplot_titles=('Sprint 10 meter', 'Sprint 20 meter', 'Sprint 30 meter'),
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

    fig.update_layout(height=600, width=800, title_text="Snelheden per aftand", showlegend=False)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header = "Sprint per afstand"
    if teamSelectie:
        description = f"Resultaten van de sprint voor de groep {teamSelectie} jaar. ".format(teamSelectie=teamSelectie)
    else:
        description = f"Resultaten van de sprint voor de groep {team_naam} jaar. ".format(team_naam=team_naam)

    conn.close()

    return render_template('dashboard/sprint.html', graphJSON=graphJSON, header=header, description=description)


@app.route('/dashboard/zijwaartsspringen', methods=['GET', 'POST'])
def visu_sprong_zij():
    bvo_id = session.get('id')
    teamSelectie = request.values.get('teamSelectie')

    if teamSelectie:
        with engine.begin() as conn:
            result = conn.execute(text('SELECT `id`, `Zijwaarts_springen_1`, `Zijwaarts_springen_2`,'
                                       '`Zijwaarts_springen_totaal`, `Staande_lengte`, `bvo_id`'
                                       'FROM `han`'
                                       f'WHERE `team_naam` = {teamSelectie} AND `bvo_id` = {bvo_id}'.format(teamSelectie=teamSelectie, bvo_id=bvo_id)))
    else:
        with engine.begin() as conn:
            result = conn.execute(text('SELECT `id`, `Zijwaarts_springen_1`, `Zijwaarts_springen_2`,'
                                       '`Zijwaarts_springen_totaal`, `Staande_lengte`, `bvo_id`'
                                       'FROM `han`'
                                       f'WHERE `team_naam` = {team_naam} AND `bvo_id` = {bvo_id}'.format(team_naam=team_naam, bvo_id=bvo_id)))

    df = pd.DataFrame([[ij for ij in i] for i in result])
    df.rename(columns={0: 'id', 1: 'Zijwaarts_springen_1', 2: 'Zijwaarts_springen_2', 3: 'Zijwaarts_springen_totaal',
                       4: 'Staande_lengte'},
              inplace=True)
    df = df.sort_values(by=['id'], ascending=[1])

    fig = px.scatter(df,
                     x='Staande_lengte',
                     y='Zijwaarts_springen_totaal',
                     color='Zijwaarts_springen_totaal',
                     hover_data=['Zijwaarts_springen_1', 'Zijwaarts_springen_2', 'id'],
                     labels={
                         "Staande_lengte": "Staande lengte in centimeters",
                         "Zijwaarts_springen_totaal": "Zijwaarts springen in meters"
                     })

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header = "Zijwaartse sprong"
    if teamSelectie:
        description = f"Resultaten van de zijwaarste sprong voor de groep {teamSelectie} jaar. ".format(
            teamSelectie=teamSelectie)
    else:
        description = f"Resultaten van de zijwaarste sprong voor de groep {team_naam} jaar. ".format(
            team_naam=team_naam)

    conn.close()

    return render_template('dashboard/zijwaartsspringen.html', graphJSON=graphJSON, header=header,
                           description=description)


@app.route('/dashboard/handoogcoordinatie', methods=['GET', 'POST'])
def visu_handoogc():
    bvo_id = session.get('id')
    teamSelectie = request.values.get('teamSelectie')

    if teamSelectie:
        with engine.begin() as conn:
            result = conn.execute(text('SELECT `id`, `Oog_hand_coordinatie_1`, `Oog_hand_coordinatie_2`,'
                                       '`Oog_hand_coordinatie_Totaal`, `Lengte_bovenlichaam`, `bvo_id`'
                                       'FROM `han`'
                                       f'WHERE `team_naam` = {teamSelectie} AND `bvo_id` = {bvo_id}'.format(teamSelectie=teamSelectie, bvo_id=bvo_id)))
    else:
        with engine.begin() as conn:
            result = conn.execute(text('SELECT `id`, `Oog_hand_coordinatie_1`, `Oog_hand_coordinatie_2`,'
                                       '`Oog_hand_coordinatie_Totaal`, `Lengte_bovenlichaam`, `bvo_id`'
                                       'FROM `han`'
                                       f'WHERE `team_naam` = {team_naam} AND `bvo_id` = {bvo_id}'.format(team_naam=team_naam, bvo_id=bvo_id)))

    df = pd.DataFrame([[ij for ij in i] for i in result])
    df.rename(columns={0: 'id', 1: 'Oog_hand_coordinatie_1', 2: 'Oog_hand_coordinatie_2',
                       3: 'Oog_hand_coordinatie_Totaal', 4: 'Lengte_bovenlichaam'},
              inplace=True)
    df = df.sort_values(by=['id'], ascending=[1])

    fig = px.scatter(df,
                     x='Lengte_bovenlichaam',
                     y='Oog_hand_coordinatie_Totaal',
                     color='Oog_hand_coordinatie_Totaal',
                     hover_data=['Oog_hand_coordinatie_1', 'Oog_hand_coordinatie_2', 'id'],
                     labels={
                         "Lengte_bovenlichaam": "Lengte bovenlichaam in centimeters",
                         "Oog_hand_coordinatie_Totaal": "Hand Oog Coordinatie Totaal"
                     })

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header = "Hand-Oog Coordinatie"
    if teamSelectie:
        description = f"Resultaten van de hand-oog coordinatie voor de groep {teamSelectie} jaar. ".format(teamSelectie=teamSelectie)
    else:
        description = f"Resultaten van de hand-oog coordinatie voor de groep {team_naam} jaar. ".format(team_naam=team_naam)

    conn.close()

    return render_template('dashboard/handoogcoordinatie.html', graphJSON=graphJSON, header=header, description=description)


@app.route('/dashboard/evenwichtsbalk', methods=['GET', 'POST'])
def visu_balance_beam():
    bvo_id = session.get('id')
    teamSelectie = request.values.get('teamSelectie')

    if teamSelectie:
        with engine.begin() as conn:
            result = conn.execute(text('SELECT `id`, `Balance_Beam_6cm`, `Balance_Beam_4_5cm`, `Balance_Beam_3cm`,'
                                       '`Balance_beam_totaal`, `Staande_lengte`, `bvo_id`'
                                       'FROM `han`'
                                       f'WHERE `team_naam` = {teamSelectie} AND `bvo_id` = {bvo_id}'.format(teamSelectie=teamSelectie, bvo_id=bvo_id)))
    else:
        with engine.begin() as conn:
            result = conn.execute(text('SELECT `id`, `Balance_Beam_6cm`, `Balance_Beam_4_5cm`, `Balance_Beam_3cm`,'
                                       '`Balance_beam_totaal`, `Staande_lengte`, `bvo_id`'
                                       'FROM `han`'
                                       f'WHERE `team_naam` = {team_naam} AND `bvo_id` = {bvo_id}'.format(team_naam=team_naam, bvo_id=bvo_id)))

    df = pd.DataFrame([[ij for ij in i] for i in result])
    df.rename(columns={0: 'id', 1: 'Balance_Beam_6cm', 2: 'Balance_Beam_4_5cm',
                       3: 'Balance_Beam_3cm', 4: 'Balance_beam_totaal', 5: 'Staande_lengte'},
              inplace=True)
    df = df.sort_values(by=['id'], ascending=[1])

    fig = px.scatter(df,
                     x='Staande_lengte',
                     y='Balance_beam_totaal',
                     color='Balance_beam_totaal',
                     hover_data=['Balance_Beam_3cm', 'Balance_Beam_4_5cm', 'Balance_Beam_6cm', 'id'],
                     labels={
                         "Staande_lengte": "Staande lengtes in centimeters",
                         "Balance_beam_totaal": "Balance Beam Totaal"
                     })

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header = "Evenwichtsbalk"
    if teamSelectie:
        description = f"Resultaten van de evenwichtsbalk voor de groep {teamSelectie} jaar. ".format(teamSelectie=teamSelectie)
    else:
        description = f"Resultaten van de evenwichtsbalk voor de groep {team_naam} jaar. ".format(team_naam=team_naam)

    conn.close()

    return render_template('dashboard/evenwichtsbalk.html', graphJSON=graphJSON, header=header, description=description)


@app.route('/dashboard/zijwaartsverplaatsen', methods=['GET', 'POST'])
def visu_zijwaarts_verplaats():
    bvo_id = session.get('id')
    teamSelectie = request.values.get('teamSelectie')

    if teamSelectie:
        with engine.begin() as conn:
            result = conn.execute(
                text('SELECT `id`, `Staande_lengte`, `Zijwaarts_verplaatsen_1`, `Zijwaarts_verplaatsen_2`,'
                     '`Zijwaarts_verplaatsen_totaal`, `bvo_id`'
                     'FROM `han`'
                     f'WHERE `team_naam` = {teamSelectie} AND `bvo_id` = {bvo_id}'.format(teamSelectie=teamSelectie, bvo_id=bvo_id)))
    else:
        with engine.begin() as conn:
            result = conn.execute(
                text('SELECT `id`, `Staande_lengte`, `Zijwaarts_verplaatsen_1`, `Zijwaarts_verplaatsen_2`,'
                     '`Zijwaarts_verplaatsen_totaal`, `bvo_id`'
                     'FROM `han`'
                     f'WHERE `team_naam` = {team_naam} AND `bvo_id` = {bvo_id}'.format(team_naam=team_naam, bvo_id=bvo_id)))

    df = pd.DataFrame([[ij for ij in i] for i in result])
    df.rename(columns={0: 'id', 1: 'Staande_lengte', 2: 'Zijwaarts_verplaatsen_1',
                       3: 'Zijwaarts_verplaatsen_2', 4: 'Zijwaarts_verplaatsen_totaal'},
              inplace=True)
    df = df.sort_values(by=['id'], ascending=[1])

    fig = px.scatter(df,
                     x='Staande_lengte',
                     y='Zijwaarts_verplaatsen_totaal',
                     color='Zijwaarts_verplaatsen_totaal',
                     hover_data=['Zijwaarts_verplaatsen_1', 'Zijwaarts_verplaatsen_2', 'id'],
                     labels={
                         "Staande_lengte": "Staande lengtes in centimeters",
                         "Zijwaarts_verplaatsen_totaal": "Zijwaarts verplaatsen Totaal"
                     })

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header = "Zijwaarts Verplaatsen"
    if teamSelectie:
        description = f"Resultaten van het zijwaarts verplaatsen voor de groep {teamSelectie} jaar. ".format(teamSelectie=teamSelectie)
    else:
        description = f"Resultaten van het zijwaarts verplaatsen voor de groep {team_naam} jaar. ".format(team_naam=team_naam)

    conn.close()

    return render_template('dashboard/zijwaartsverplaatsen.html', graphJSON=graphJSON, header=header, description=description)


@app.route('/dashboard/cod', methods=['GET', 'POST'])
def visu_CoD():
    bvo_id = session.get('id')
    teamSelectie = request.values.get('teamSelectie')

    if teamSelectie:
        with engine.begin() as conn:
            result = conn.execute(text('SELECT `id`, `Staande_lengte`, `CoD_links_1`, `CoD_links_2`, `CoD_links_beste`,'
                                       '`CoD_rechts_1`, `CoD_rechts_2`, `CoD_rechts_beste`, `bvo_id`'
                                       'FROM `han`'
                                       f'WHERE `team_naam` = {teamSelectie} AND `bvo_id` = {bvo_id}'.format(teamSelectie=teamSelectie, bvo_id=bvo_id)))
    else:
        with engine.begin() as conn:
            result = conn.execute(text('SELECT `id`, `Staande_lengte`, `CoD_links_1`, `CoD_links_2`, `CoD_links_beste`,'
                                       '`CoD_rechts_1`, `CoD_rechts_2`, `CoD_rechts_beste`, `bvo_id`'
                                       'FROM `han`'
                                       f'WHERE `team_naam` = {team_naam} AND `bvo_id` = {bvo_id}'.format(team_naam=team_naam, bvo_id=bvo_id)))

    df = pd.DataFrame([[ij for ij in i] for i in result])
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

    fig.update_layout(height=600, width=800, title_text="CoD per been", showlegend=False)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header = "CoD Scores per been"
    if teamSelectie:
        description = f"Resultaten van de CoD voor de groep {teamSelectie} jaar. ".format(teamSelectie=teamSelectie)
    else:
        description = f"Resultaten van de CoD voor de groep {team_naam} jaar. ".format(team_naam=team_naam)

    conn.close()

    return render_template('dashboard/cod.html', graphJSON=graphJSON, header=header, description=description)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
