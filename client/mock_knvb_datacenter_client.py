import logging
import os
from hashlib import md5

from dotenv import load_dotenv

from client.models.response import *

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


# Input parameters
#    teamid: Uniek Team ID. Let op, team moet team van club zijn.
#    weeknummer: week waarvan de uitslagen worden opgehaald (1-52, A) (optioneel) (A = begin seizoen tot huidige week)
#    comptype: Competitie type R = Regulier, B = Beker, N = Nacompetitie, V = Vriendschappelijke Competitie, default = R
def get_uitslagen(team_id, weeknummer, comptype=None) -> list[KnvbUitslagDTO]:
    authorized_url = _BASE_URL + _mock_get_auth_query_parameters(auth_path='/teams')
    params = {'teamid': team_id, 'weeknummer': weeknummer}
    if comptype is not None:
        params = params.update({'comptype': comptype})
    # response = requests.get(url=authorized_url, params=params)
    response = _mock_successful_response(dict(url=authorized_url, params=params), _mock_uitslagen_response())
    return list(map(lambda x: KnvbUitslagDTO(**x), response.List))


def get_teams() -> list[KnvbTeamInfoDTO]:
    authorized_url = _BASE_URL + _mock_get_auth_query_parameters(auth_path='/teams')
    # response = requests.get(url=authorized_url)
    response = _mock_successful_response(authorized_url, _mock_teams_response())
    return list(map(lambda x: KnvbTeamInfoDTO(**x), response.List))


def _mock_successful_response(given, result):
    return KnvbResponse(result)


def _mock_expired_session_response(given, result):
    return KnvbResponse(result)


def _mock_get_auth_query_parameters(auth_path):
    php_sess_id = _get_session_id(False)
    hash_code = _generate_hash(auth_path, php_sess_id)

    # example result: /teams?PHPSESSID=<12345>&hash=<abbccdde200394>
    return f'{auth_path}?PHPSESSID={php_sess_id}&hash={hash_code}'


# #Input parameters
#    pathname: Unieke pathname voor de club zoals vastgelegd in het admin interface.
#    apiversion: Is optioneel; in sommige gevallen kan er een bepaald versie nummer van de API mee afgedwongen worden.
def _get_session_id(successful=True):
    # BASEURL/api/initialisatie/<pathname>[&apiversion=1.0]
    auth_url = _AUTH_PATH
    if successful:
        auth_resp = _mock_successful_response(auth_url, _mock_initialisatie_response())
        return auth_resp.List[0]['PHPSESSID']
    else:
        auth_resp = _mock_expired_session_response(auth_url,
                                                   {"error": {"errorcode": "9992", "message": "Hash not correct"}})
        msg = f'Error auth invalid, code: {auth_resp.errorcode}, message: {auth_resp.message}'
        logging.error(msg)


def _generate_hash(url_path, session_id):
    api_key = _API_KEY
    string = f'{api_key}#{url_path}#{session_id}'.encode('utf-8')
    return md5(string).hexdigest()


def _mock_initialisatie_response():
    return {
        "errorcode": 1000, "message": "Ok",
        "List": [{
            "PHPSESSID": "s39fu9pq33990qhvbj97sl1g47",
            "clubnaam": "zvv ZILVERMEEUWEN - ZAANDAM",
            "apiversion": "1.0",
            "changed": "2015-09-28 12:35:15",
            "changelog": "http:\/\/api.knvbdatacentre.nl\/api\/changes?version=1.0",
            "logo": "http:\/\/bin617.website-voetbal.nl\/sites\/voetbal.nl\/files\/knvblogos\/BBFX33T.jpg",
            "kleuren": {
                "foreground": "ffffff",
                "background1": "0000ff",
                "background2": "5656ff",
                "verloop": "1"
            }, "rss": [{
                "bron": "http:\/\/www.forza-almere.nl\/?feed=rss2",
                "rssdefault": 1, "prof_rss": 1
            }, {
                "bron": "http:\/\/optioneel.cms.nl\/?feed=admin",
                "rssdefault": 0, "prof_rss": 0
            }], "twitter": [{
                "type": "account",
                "value": "@vvzilvermeeuwen"
            }], "twittertags": ["a",
                                "b",
                                "c"], "appsponsors": [{
                "naam": "FOEKENS",
                "url": "http:\/\/www.foekens.nl",
                "banner": "http:\/\/knvbdatacentre.nl\/sites\/all\/themes\/knvbdatacentre\/images\/appsponsor\/1384978675.JPG"
            }, {
                "naam": "Vonk Sports",
                "url": "http:\/\/www.vonksports.nl\/",
                "banner": "http:\/\/knvbdatacentre.nl\/sites\/all\/themes\/knvbdatacentre\/images\/appsponsor\/1411842644.JPG"
            }]
        }]
    }


def _mock_teams_response():
    return {
        "errorcode": 1000,
        "message": "Ok, Team Listing follows",
        "List": [
            {
                "teamid": "122561",
                "teamname": "Zilvermeeuwen 1",
                "speeldag": "ZO",
                "categorie": "Senioren",
                "regulierecompetitie": "J",
                "bekercompetitie": "J",
                "nacompetitie": "N"
            }, {
                "teamid": "122564",
                "teamname": "Zilvermeeuwen 2",
                "speeldag": "ZO",
                "categorie": "Senioren",
                "regulierecompetitie": "J",
                "bekercompetitie": "J",
                "nacompetitie": "N"
            }
        ]
    }


def _mock_uitslagen_response():
    return {
        "errorcode": 1000,
        "message": "Ok",
        "List": [{
            "MatchID": "9656058",
            "WedstrijdNummer": "5245",
            "Datum": "2015-10-11",
            "Tijd": "1430",
            "ThuisClub": "VVA\/Spartaan 1",
            "ThuisLogo": "http:\/\/bin617.website-voetbal.nl\/sites\/voetbal.nl\/files\/knvblogos\/BBCZ30P.png",
            "ThuisTeamID": "111467",
            "UitClub": "Zilvermeeuwen 1",
            "UitLogo": "http:\/\/bin617.website-voetbal.nl\/sites\/voetbal.nl\/files\/knvblogos\/BBFX33T.jpg",
            "UitTeamID": "122561",
            "PuntenTeam1": "0",
            "PuntenTeam2": "1",
            "PuntenTeam1Verl": "NULL",
            "PuntenTeam2Verl": "NULL",
            "PuntenTeam1Strafsch": "NULL",
            "PuntenTeam2Strafsch": "NULL",
            "Bijzonderheden": "AFG",
            "Scheidsrechter": "",
            "CompType": "R",
            "CompNummer": "W1-0512**-12-418659!",
            "WedstrijdDag": "6"
        }, {
            "MatchID": "9655949",
            "WedstrijdNummer": "5136",
            "Datum": "2015-10-04",
            "Tijd": "1400",
            "ThuisClub": "Zilvermeeuwen 1",
            "ThuisLogo": "http:\/\/bin617.website-voetbal.nl\/sites\/voetbal.nl\/files\/knvblogos\/BBFX33T.jpg",
            "ThuisTeamID": "122561",
            "UitClub": "SCH'44 1",
            "UitLogo": "http:\/\/bin617.website-voetbal.nl\/sites\/voetbal.nl\/files\/knvblogos\/BBCC519.png",
            "UitTeamID": "102251",
            "PuntenTeam1": "2",
            "PuntenTeam2": "3",
            "PuntenTeam1Verl": "NULL",
            "PuntenTeam2Verl": "NULL",
            "PuntenTeam1Strafsch": "NULL",
            "PuntenTeam2Strafsch": "NULL",
            "Bijzonderheden": "",
            "Scheidsrechter": "",
            "CompType": "R",
            "CompNummer": "W1-0512**-12-418659!",
            "WedstrijdDag": "5"
        }]
    }
