import json
import os

from dotenv import load_dotenv

from client.models.response import *

from client.KnvbDatacenterRequestHandler import KnvbDatacenterRequestHandler

# Additional information about the API can be found at: https://api.knvbdataservice.nl/hoofdstuk/teams/1234/results

"""
RESPONSE FORMAT ZOALS AFGESPROKEN MET SANDRO
{
        "MatchID":"9656058",
        "Datum":"2015-10-11",
        "ThuisClub":"VVA\/Spartaan 1",
        "UitClub":"Zilvermeeuwen 1",
        "PuntenTeam1":"0",
        "PuntenTeam2":"1",
        "PuntenTeam1Verl":"NULL",
        "PuntenTeam2Verl":"NULL",
        "PuntenTeam1Strafsch":"NULL",
        "PuntenTeam2Strafsch":"NULL",
        "Bijzonderheden":"AFG",
    }
"""

load_dotenv()

_BASE_URL = os.getenv('BASE_URL')
_AUTH_PATH = os.getenv('AUTH_URL')
_API_KEY = os.getenv('API_KEY')
_STATUS_CODES = json.loads(os.getenv('STATUS_CODES'))


requestHandler = KnvbDatacenterRequestHandler(_BASE_URL, _AUTH_PATH, _API_KEY, _STATUS_CODES)


def get_all_teams() -> list[KnvbTeamInfoDTO]:
    result = requestHandler.handle(url_path='/teams', data_classtype=KnvbTeamInfoDTO)
    if not result:
        return []
    return result


# Example: /teams/<teamid>/results?[weeknummer=12][&comptype=R|B|N|V&]PHPSESSID=<12345>&hash=<abbccdde200394>
def get_uitslagen_by_team_id(team_id, weeknummer='A', comptype=None) -> list[KnvbUitslagDTO]:
    """Input parameters\n
    ##teamid: Uniek Team ID. Let op, team moet team van club zijn.\n
    #weeknummer: week waarvan de uitslagen worden opgehaald (1-52, A) (optioneel) (A = begin seizoen tot huidige week)\n
    #comptype: Competitie type R = Regulier, B = Beker, N = Nacompetitie, V = Vriendschappelijke Competitie, default = R"""

    url = f'/teams/{team_id}/results'
    params = {'weeknummer': weeknummer}

    if comptype is not None:
        params = params.update({'comptype': comptype})

    result = requestHandler.handle(url_path=url, params=params, data_classtype=KnvbUitslagDTO)
    if not result:
        return []
    return result
