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


def request_bvo():
    query = f"""SELECT DISTINCT acc.display_name, han.bvo_naam FROM accounts AS acc 
            INNER JOIN han on acc.id = han.bvo_naam"""
    return pd.DataFrame(execute_query(query))


# request vertesprong by team_name and bvo_id
def request_vertesprong(bvo_naam: str):
    return pd.DataFrame(session.execute(
        select(Han.speler_id, Han.Vertesprong_1, 
            Han.Vertesprong_2, Han.Vertesprong_beste,
            Han.team_naam, Han.Staande_lengte, Han.bvo_naam, 
            Han.geboortedatum, Han.seizoen)
        .where(Han.bvo_naam == bvo_naam)))


# request sprinten by team_name and bvo_id
def request_sprint(bvo_naam: str):
    return pd.DataFrame(session.execute(
        select(Han.speler_id, Han.X10_meter_sprint_beste, 
            Han.X20_meter_sprint_beste, Han.X30_meter_sprint_beste,
            Han.team_naam, Han.geboortedatum, Han.seizoen)
        .where(Han.bvo_naam == bvo_naam)
    ))

# request handoogcoordinatie by team_name and bvo_id
def request_hand_oog_coordinatie(bvo_naam: str):
    return pd.DataFrame(session.execute(
        select(Han.speler_id, Han.Oog_hand_coordinatie_totaal,
               Han.Oog_hand_coordinatie_1, Han.Oog_hand_coordinatie_2,
               Han.Staande_lengte, Han.geboortedatum, Han.team_naam)
        .where(Han.bvo_naam == bvo_naam)
    ))


# request zijwaarts verplaatsen by team_name and bvo_id
def request_zijwaarts_verplaatsen(team_name: str, bvo_naam: str):
    query = f"""SELECT `id`, `Zijwaarts_verplaatsen_1`, `Zijwaarts_verplaatsen_2`, `Zijwaarts_verplaatsen_totaal`, 
        `Staande_lengte`, `bvo_naam` FROM `han` WHERE `team_naam` = '{team_name}' AND `bvo_naam` = '{bvo_naam}'"""
    return execute_query(query)


def request_evenwichtsbalk():
    return pd.DataFrame(session.execute(
        select(Han.id, Han.bvo_naam, Account.display_name, Han.team_naam, Han.reeks_naam, Han.Testdatum,
               Han.Balance_Beam_3cm, Han.Balance_Beam_4_5cm, Han.Balance_Beam_6cm, Han.Balance_beam_totaal)
        .where(Account.id == Han.bvo_naam)))


def request_evenwichtsbalk_sc_2():
    return pd.DataFrame(session.execute(
        select(Han.speler_id, Han.bvo_naam, Han.Balance_Beam_6cm, Han.Balance_Beam_4_5cm, 
        Han.Balance_Beam_3cm, Han.Balance_beam_totaal, Han.reeks_naam, Han.team_naam))
    )


# request zijwaarts springen by team_name and bvo_id
def request_zijwaarts_springen(bvo_naam: str):
    query = f"""SELECT `id`, `Zijwaarts_springen_1`, `Zijwaarts_springen_2`, `Zijwaarts_springen_totaal`, 
        `Staande_lengte`, `bvo_naam` FROM `han`  WHERE `bvo_naam` = '{bvo_naam}'"""
    return execute_query(query)


# request change of direction by team_name and bvo_id
def request_change_of_direction(bvo_naam: str):
    # return \
    return pd.DataFrame(session.execute(
        select(Han.id, Han.CoD_links_1, Han.CoD_links_2, Han.CoD_links_beste, Han.CoD_rechts_1, Han.CoD_rechts_2,
               Han.CoD_rechts_beste, Han.Staande_lengte, Han.team_naam, Han.bvo_naam, Han.geboortedatum, Han.seizoen)
        .where(Han.bvo_naam == bvo_naam))
    )


def request_algemene_motoriek(bvo_naam: str):
    return pd.DataFrame(session.execute(
        select(Han.id, Account.display_name, Han.geboortedatum, Han.bvo_naam, Han.seizoen, Han.speler_id, Han.team_naam, Han.reeks_naam,
               Han.Balance_Beam_3cm, Han.Balance_Beam_4_5cm, Han.Balance_Beam_6cm, Han.Balance_beam_totaal,
               Han.Zijwaarts_springen_1, Han.Zijwaarts_springen_2, Han.Zijwaarts_springen_totaal,
               Han.Zijwaarts_verplaatsen_1, Han.Zijwaarts_verplaatsen_2, Han.Zijwaarts_verplaatsen_totaal,
               Han.Oog_hand_coordinatie_1, Han.Oog_hand_coordinatie_2, Han.Oog_hand_coordinatie_totaal)
        .where(Account.id == Han.bvo_naam and Han.bvo_naam == bvo_naam)
    ))


def get_zijwaarts_springen():
    return pd.DataFrame(session.execute(
        select(Account.display_name, Han.bvo_naam, Han.team_naam, Han.reeks_naam, Han.Testdatum,
              Han.Zijwaarts_springen_totaal)
        .where(Account.id == Han.bvo_naam)))
