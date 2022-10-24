from sqlalchemy import create_engine
from sqlalchemy.engine.cursor import CursorResult


connect_args = {'ssl': {'fake_flag_to_enable_tls': True}}
connect_string = 'mysql+pymysql://{}:{}@{}/{}'.format(
    'tiggele', 'h05$rzZA$.I3084I', 'oege.ie.hva.nl', 'ztiggele')

engine = create_engine(connect_string, connect_args=connect_args)


def execute_query(query: str) -> CursorResult:
    return engine.execute(query)


# request account by username and password
def request_account(username: str, password: str):
    query = f"SELECT * FROM `accounts` WHERE `username` = '{username}' AND `password` = '{password}'"
    return execute_query(query).fetchone()


# request vertesprong by team_name and bvo_id
def request_vertesprong(team_name: str, bvo_id: str):
    query = f"""SELECT `id`, `Vertesprong_1`, `Vertesprong_2`, `Vertesprong_beste`, 
        `Staande_lengte`, `bvo_id` FROM `han` WHERE `team_naam` = '{team_name}' AND `bvo_id` = '{bvo_id}'"""
    return execute_query(query)


# request sprinten by team_name and bvo_id
def request_sprinten(team_name: str, bvo_id: str):
    query = f"""SELECT `id`, `X10_meter_sprint_1`, `X10_meter_sprint_2`, `X10_meter_sprint_beste`, 
        `X20_meter_sprint_1`, `X20_meter_sprint_2`, `X20_meter_sprint_beste`, 
        `X30_meter_sprint_1`, `X30_meter_sprint_2`, `X30_meter_sprint_beste`,
        `Staande_lengte`, `bvo_id` FROM `han` WHERE `team_naam` = '{team_name}' AND `bvo_id` = '{bvo_id}'"""
    return execute_query(query)


# request zijwaarts springen by team_name and bvo_id
def request_zijwaarts_springen(team_name: str, bvo_id: str):
    query = f"""SELECT `id`, `Zijwaarts_springen_1`, `Zijwaarts_springen_2`, `Zijwaarts_springen_totaal`, 
        `Staande_lengte`, `bvo_id` FROM `han` WHERE `team_naam` = '{team_name}' AND `bvo_id` = '{bvo_id}'"""
    return execute_query(query)


# request handoogcoordinatie by team_name and bvo_id
def request_hand_oog_coordinatie(team_name: str, bvo_id: str):
    query = f"""SELECT `id`, `Oog_hand_coordinatie_1`, `Oog_hand_coordinatie_2`, `Oog_hand_coordinatie_Totaal`, 
        `Lengte_bovenlichaam`, `bvo_id` FROM `han` WHERE `team_naam` = '{team_name}' AND `bvo_id` = '{bvo_id}'"""
    return execute_query(query)


# request evenwichtsbalk by team_name and bvo_id
def request_evenwichtsbalk(team_name: str, bvo_id: str):
    query = f"""SELECT `id`, `Balance_Beam_6cm`, `Balance_Beam_4_5cm`, `Balance_Beam_3cm`, `Balance_beam_totaal`,
    `Staande_lengte`, `bvo_id` FROM `han` WHERE `team_naam` = '{team_name}' AND `bvo_id` = '{bvo_id}'"""
    return execute_query(query)


# request zijwaarts verplaatsen by team_name and bvo_id
def request_zijwaarts_verplaatsen(team_name: str, bvo_id: str):
    query = f"""SELECT `id`, `Zijwaarts_verplaatsen_1`, `Zijwaarts_verplaatsen_2`, `Zijwaarts_verplaatsen_totaal`, 
        `Staande_lengte`, `bvo_id` FROM `han` WHERE `team_naam` = '{team_name}' AND `bvo_id` = '{bvo_id}'"""
    return execute_query(query)


# request change of direction by team_name and bvo_id
def request_change_of_direction(team_name: str, bvo_id: str):
    query = f"""SELECT `id`, `CoD_links_1`, `CoD_links_2`, `CoD_links_beste`,
        `CoD_rechts_1`, `CoD_rechts_2`, `CoD_rechts_beste`,
        `Staande_lengte`, `bvo_id` FROM `han` WHERE `team_naam` = '{team_name}' AND `bvo_id` = '{bvo_id}'"""
    return execute_query(query)
