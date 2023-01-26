import json
import os

from dotenv import load_dotenv

from client.models.models import *
from client.knvb_datacentre_request_handler import KnvbDatacentreRequestHandler

"""
    Additional information about the API can be found at: https://api.knvbdataservice.nl/hoofdstuk/teams/1234/results
"""

load_dotenv()

_BASE_URL = os.getenv('BASE_URL')
_AUTH_PATH = os.getenv('AUTH_URL')
_API_KEY = os.getenv('API_KEY')
_STATUS_CODES = json.loads(os.getenv('STATUS_CODES'))

requestHandler = KnvbDatacentreRequestHandler(_BASE_URL, _AUTH_PATH, _API_KEY, _STATUS_CODES)


def get_all_teams() -> list[KnvbTeamInfoDTO]:
    return requestHandler.handle(url_path='/teams', data_classtype=KnvbTeamInfoDTO)


def get_uitslagen_by_team_id(team_id, weeknummer='A', comptype=None) -> list[KnvbUitslagDTO]:
    """Input parameters\n
    ##teamid: Uniek Team ID. Let op, team moet team van club zijn.\n
    #weeknummer: week waarvan de uitslagen worden opgehaald (1-52, A) (optioneel) (A = begin seizoen tot huidige week)\n
    #comptype: Competitie type R = Regulier, B = Beker, N = Nacompetitie, V = Vriendschappelijke Competitie, default = R"""

    url = f'/teams/{team_id}/results'
    params = {'weeknummer': weeknummer}

    if comptype is not None:
        params.update({'comptype': comptype})

    return requestHandler.handle(url_path=url, params=params, data_classtype=KnvbUitslagDTO)
