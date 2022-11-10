from sqlalchemy import select
from sqlalchemy.engine.cursor import CursorResult
import pandas as pd
from database import session_factory, engine
from database.models import Account, Han


def execute_query(query: str) -> CursorResult:
    return engine.execute(query)


# request account by username and password
def request_account(username: str, password: str):
    session = session_factory()
    return session.execute(
        select(Account.id, Account.username, Account.display_name)
        .where(Account.username == username, Account.password == password)
    ).fetchone()


# request vertesprong by team_name and bvo_id
def request_vertesprong(team_name: str, club_code: str):
    query = f"""SELECT `id`, `Vertesprong_1`, `Vertesprong_2`, `Vertesprong_beste`, 
        `Staande_lengte`, `club_code` FROM `han` WHERE `team_naam` = '{team_name}' AND `club_code` = '{club_code}'"""
    return execute_query(query)


# request sprinten by team_name and bvo_id
def request_sprinten(team_name: str, club_code: str):
    query = f"""SELECT `id`, `X10_meter_sprint_1`, `X10_meter_sprint_2`, `X10_meter_sprint_beste`, 
        `X20_meter_sprint_1`, `X20_meter_sprint_2`, `X20_meter_sprint_beste`, 
        `X30_meter_sprint_1`, `X30_meter_sprint_2`, `X30_meter_sprint_beste`,
        `Staande_lengte`, `club_code` FROM `han` WHERE `team_naam` = '{team_name}' AND `club_code` = '{club_code}'"""
    return execute_query(query)


# request handoogcoordinatie by team_name and bvo_id
def request_hand_oog_coordinatie(team_name: str, club_code: str):
    query = f"""SELECT `id`, `Oog_hand_coordinatie_1`, `Oog_hand_coordinatie_2`, `Oog_hand_coordinatie_Totaal`, 
        `Zithoogte`, `club_code` FROM `han` WHERE `team_naam` = '{team_name}' AND `club_code` = '{club_code}'"""

    return execute_query(query)


# request zijwaarts verplaatsen by team_name and bvo_id
def request_zijwaarts_verplaatsen(team_name: str, club_code: str):
    query = f"""SELECT `id`, `Zijwaarts_verplaatsen_1`, `Zijwaarts_verplaatsen_2`, `Zijwaarts_verplaatsen_totaal`, 
        `Staande_lengte`, `club_code` FROM `han` WHERE `team_naam` = '{team_name}' AND `club_code` = '{club_code}'"""
    return execute_query(query)


# request evenwichtsbalk by team_name and bvo_id
def request_evenwichtsbalk(team_name: str, club_code: str):
    session =  session_factory()
    #return
    return session.execute(
        select(Han.id,  Han.Balance_Beam_6cm, Han.Balance_Beam_4_5cm, Han.Balance_Beam_3cm, Han.Balance_beam_totaal,
    Han.Staande_lengte, Han.club_code)
    .where(Han.team_naam == team_name, Han.club_code == club_code)
    )


# request zijwaarts springen by team_name and bvo_id
def request_zijwaarts_springen(team_name: str, club_code: str):
    query = f"""SELECT `id`, `Zijwaarts_springen_1`, `Zijwaarts_springen_2`, `Zijwaarts_springen_totaal`, 
        `Staande_lengte`, `club_code` FROM `han` WHERE `team_naam` = '{team_name}' AND `club_code` = '{club_code}'"""
    return execute_query(query)


# request change of direction by team_name and bvo_id
def request_change_of_direction(team_name: str, club_code: str):
    session = session_factory()
    # return \
    return session.execute(
        select(Han.id, Han.CoD_links_1, Han.CoD_links_2, Han.CoD_links_beste, Han.CoD_rechts_1, Han.CoD_rechts_2,
               Han.CoD_rechts_beste, Han.Staande_lengte, Han.club_code)
        .where(Han.team_naam == team_name, Han.club_code == club_code)
    )
