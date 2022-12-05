from sqlalchemy import select, insert
from sqlalchemy.engine.cursor import CursorResult
import pandas as pd
from database import session_factory, engine
from database.models import Account, Han


session = session_factory()


def execute_query(query: str) -> CursorResult:
    return engine.execute(query)


# request account by username and password
def request_account(username: str, password: str):
    session = session_factory()
    return session.execute(
        select(Account.id, Account.username, Account.display_name)
        .where(Account.username == username, Account.password == password)
    ).fetchone()


# store account in database
def store_account(id: str, username: str, password, email: str, club: str):
    session = session_factory()
    newAccount = Account(id, username, password, email, club, False)
    session.add(newAccount)
    session.commit()
    return '<h1>account stored</h1>'


# request vertesprong by team_name and bvo_id
def request_vertesprong(club_code: str):
    query = f"""SELECT `id`, `Vertesprong_1`, `Vertesprong_2`, `Vertesprong_beste`, 
        `Staande_lengte`, `club_code` FROM `han` WHERE `club_code` = '{club_code}'"""
    return pd.DataFrame(execute_query(query))


# request sprinten by team_name and bvo_id
def request_sprint(club_code: str):
    return pd.DataFrame(session.execute(
        select(Han.speler_code, Han.X10_meter_sprint_beste, 
            Han.X20_meter_sprint_beste, Han.X30_meter_sprint_beste,
            Han.team_naam)
        .where(Han.club_code == club_code)
    ))

# request handoogcoordinatie by team_name and bvo_id
def request_hand_oog_coordinatie(club_code: str):
    return pd.DataFrame(session.execute(
        select(Han.speler_code, Han.Oog_hand_coordinatie_totaal,
               Han.Oog_hand_coordinatie_1, Han.Oog_hand_coordinatie_2,
               Han.Staande_lengte, Han.geboortedatum, Han.team_naam)
        .where(Han.club_code == club_code)
    ))


# request zijwaarts verplaatsen by team_name and bvo_id
def request_zijwaarts_verplaatsen(team_name: str, club_code: str):
    query = f"""SELECT `id`, `Zijwaarts_verplaatsen_1`, `Zijwaarts_verplaatsen_2`, `Zijwaarts_verplaatsen_totaal`, 
        `Staande_lengte`, `club_code` FROM `han` WHERE `team_naam` = '{team_name}' AND `club_code` = '{club_code}'"""
    return execute_query(query)


def request_evenwichtsbalk():
    return pd.DataFrame(session.execute(
        select(Han.id, Han.club_code, Account.display_name, Han.team_naam, Han.meting, Han.datum,
               Han.Balance_Beam_3cm, Han.Balance_Beam_4_5cm, Han.Balance_Beam_6cm, Han.Balance_beam_totaal)
        .where(Account.id == Han.club_code)))


def request_evenwichtsbalk_sc_2():
    return pd.DataFrame(session.execute(
        select(Han.speler_code, Han.club_code, Han.Balance_Beam_6cm, Han.Balance_Beam_4_5cm, 
        Han.Balance_Beam_3cm, Han.Balance_beam_totaal, Han.meting, Han.team_naam))
    )


# request zijwaarts springen by team_name and bvo_id
def request_zijwaarts_springen(club_code: str):
    query = f"""SELECT `id`, `Zijwaarts_springen_1`, `Zijwaarts_springen_2`, `Zijwaarts_springen_totaal`, 
        `Staande_lengte`, `club_code` FROM `han`  WHERE `club_code` = '{club_code}'"""
    return execute_query(query)


# request change of direction by team_name and bvo_id
def request_change_of_direction(club_code: str):
    # return \
    return pd.DataFrame(session.execute(
        select(Han.id, Han.CoD_links_1, Han.CoD_links_2, Han.CoD_links_beste, Han.CoD_rechts_1, Han.CoD_rechts_2,
               Han.CoD_rechts_beste, Han.Staande_lengte, Han.team_naam, Han.club_code)
        .where(Han.club_code == club_code))
    )


def request_algemene_motoriek(club_code: str):
    return pd.DataFrame(session.execute(
        select(Han.id, Account.display_name, Han.club_code, Han.speler_code, Han.team_naam, Han.meting,
               Han.Balance_Beam_3cm, Han.Balance_Beam_4_5cm, Han.Balance_Beam_6cm, Han.Balance_beam_totaal,
               Han.Zijwaarts_springen_1, Han.Zijwaarts_springen_2, Han.Zijwaarts_springen_totaal,
               Han.Zijwaarts_verplaatsen_1, Han.Zijwaarts_verplaatsen_2, Han.Zijwaarts_verplaatsen_totaal,
               Han.Oog_hand_coordinatie_1, Han.Oog_hand_coordinatie_2, Han.Oog_hand_coordinatie_totaal)
        .where(Account.id == Han.club_code and Han.club_code == club_code)
    ))


def get_zijwaarts_springen():
    return pd.DataFrame(session.execute(
        select(Account.display_name, Han.club_code, Han.team_naam, Han.meting, Han.datum,
              Han.Zijwaarts_springen_totaal)
        .where(Account.id == Han.club_code)))
