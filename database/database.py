import pandas as pd
from sqlalchemy import select
from sqlalchemy.engine.cursor import CursorResult

from database import session_factory, engine
from database.models import Account, Han


# Execute a sql statement by passing a query
def execute_query(query: str) -> CursorResult:
    return engine.execute(query)


# request account by username and password
def request_account(username: str, password: str):
    session = session_factory()
    result = session.execute(
        select(Account.id, Account.username, Account.display_name)
        .where(Account.username == username, Account.password == password)
    ).fetchone()
    session.close()
    return result
    

# store account in database
def store_account(id: str, username: str, password, email: str, club: str):
    session = session_factory()
    newAccount = Account(id, username, password, email, club, False)
    session.add(newAccount)
    session.commit()
    session.close()
    return '<h1>account stored</h1>'


def request_bvo():
    query = f"""SELECT DISTINCT acc.display_name, han.bvo_naam FROM accounts AS acc 
            INNER JOIN han on acc.id = han.bvo_naam"""
    return pd.DataFrame(execute_query(query))


# request vertesprong by team_name and bvo_id
def request_vertesprong(bvo_naam: str):
    session = session_factory()
    result = pd.DataFrame(session.execute(
        select(Han.id, Account.display_name, Han.geboortedatum, Han.bvo_naam, Han.seizoen, Han.Testdatum, Han.speler_id,
               Han.team_naam, Han.reeks_naam, Han.geboortedatum, Han.Staande_lengte, Han.Vertesprong_1,
               Han.Vertesprong_2, Han.Vertesprong_beste
               )
        .where(Account.id == Han.bvo_naam)
        .where(Han.bvo_naam == bvo_naam)))
    session.close()
    return result


# request sprinten by team_name and bvo_id
def request_sprint(bvo_naam: str):
    session = session_factory()
    result = pd.DataFrame(session.execute(
        select(Han.id, Account.display_name, Han.geboortedatum, Han.bvo_naam, Han.seizoen, Han.Testdatum, Han.speler_id,
               Han.team_naam, Han.reeks_naam, Han.geboortedatum, Han.Staande_lengte, Han.X10_meter_sprint_beste,
               Han.X20_meter_sprint_beste, Han.X30_meter_sprint_beste,
               )
        .where(Account.id == Han.bvo_naam)
        .where(Han.bvo_naam == bvo_naam)))
    session.close()
    return result


# request change of direction by team_name and bvo_id
def request_change_of_direction(bvo_naam: str):
    session = session_factory()
    result = pd.DataFrame(session.execute(
        select(Han.id, Account.display_name, Han.geboortedatum, Han.bvo_naam, Han.seizoen, Han.Testdatum, Han.speler_id,
               Han.team_naam, Han.reeks_naam, Han.geboortedatum, Han.Staande_lengte,
               Han.CoD_links_1, Han.CoD_links_2, Han.CoD_links_beste, Han.CoD_rechts_1, Han.CoD_rechts_2,
               Han.CoD_rechts_beste)
        .where(Account.id == Han.bvo_naam)
        .where(Han.bvo_naam == bvo_naam)
    ))
    session.close()
    return result


# request algemene motoriek by team_name and bvo_id
def request_algemene_motoriek(bvo_naam: str):
    session = session_factory()
    result = pd.DataFrame(session.execute(
        select(Han.id, Account.display_name, Han.geboortedatum, Han.bvo_naam, Han.seizoen, Han.Testdatum, Han.speler_id,
               Han.team_naam, Han.reeks_naam, Han.geboortedatum, Han.Staande_lengte,
               Han.Balance_Beam_3cm, Han.Balance_Beam_4_5cm, Han.Balance_Beam_6cm, Han.Balance_beam_totaal,
               Han.Zijwaarts_springen_1, Han.Zijwaarts_springen_2, Han.Zijwaarts_springen_totaal,
               Han.Zijwaarts_verplaatsen_1, Han.Zijwaarts_verplaatsen_2, Han.Zijwaarts_verplaatsen_totaal,
               Han.Oog_hand_coordinatie_1, Han.Oog_hand_coordinatie_2, Han.Oog_hand_coordinatie_totaal
               )
        .where(Account.id == Han.bvo_naam)
        .where(Han.bvo_naam == bvo_naam)
    ))
    session.close()
    return result
