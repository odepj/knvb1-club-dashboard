import logging
from hashlib import md5

import requests

from client.util.mapper import instantiateClassFromList
from client.models.models import KnvbResponse


def _pretty_print_request(base_url, url_path, params):
    req = requests.Request(method='get', url=base_url + url_path, params=params).prepare()
    url = f'REQUEST TO:     \t{req.url}'
    method = f'method:         {req.method}'
    url_path = f'url_path:       {url_path}'
    req_params = f'request params: {params}'
    print('{}\n\t{}\n\t{}\n\t{}\n'.format(url, method, url_path, req_params))


class MockKnvbDatacentreRequestHandler:
    def __init__(self, base_url, auth_path, api_key, status_codes):
        self.base_url = base_url
        self.auth_path = auth_path
        self.api_key = api_key
        self.status_codes = status_codes

    def mock_handle(self, url_path, params=None, data_classtype=dict, mock_response=None):
        to_be_authorized = '/' + url_path.split('/')[1]

        auth_params = self._get_authorization_request_params(to_be_authorized)
        if not params:
            params = dict()
        params.update(auth_params)

        result = self._send_request(url_path, params, mock_response)
        return instantiateClassFromList(data_classtype, result.List)

    def _send_request(self, url_path, params, mock_response):
        actual_request = dict(base_url=self.base_url, url_path=url_path, params=params)
        knvb_response = _mock_incorrect_hash_response() if not mock_response else _mock_successful_response(
            mock_response, actual_request)
        self._check_request_code(knvb_response)
        return knvb_response

    def _get_authorization_request_params(self, auth_path):
        session_id = self._get_session_id()
        hash_code = self._generate_hash(auth_path, session_id)
        return {'PHPSESSID': session_id, 'hash': hash_code}

    #  pathname: Unieke pathname voor de club zoals vastgelegd in het admin interface.
    #  apiversion: Is optioneel; in sommige gevallen kan er een bepaald versie nummer van de API mee afgedwongen worden.
    def _get_session_id(self):
        # BASEURL/api/initialisatie/<super_secret_personal_path>[&apiversion=1.0]
        actual_request = dict(base_url=self.base_url, url_path=f'/initialisatie{self.auth_path}', params=dict())
        response = _mock_successful_response(_mock_initialisatie_response(), given=actual_request)
        if not response.List:
            msg = f'An error occurred while fetching a session_id, code: {response.errorcode} message: {response.message}'
            logging.error(msg)
        return response.List[0]['PHPSESSID']

    def _generate_hash(self, url_path, session_id):
        return md5(f'{self.api_key}#{url_path}#{session_id}'.encode('utf-8')).hexdigest()

    def _check_request_code(self, response: KnvbResponse):
        if response.errorcode != 1000:
            key = str(response.errorcode)
            msg = f'Client responded with an error, statuscode: {response.errorcode},' \
                  f' http response message: {response.message} \nerror message according to API doc: '
            status_code_info = self.status_codes[key] if key in self.status_codes.keys() else 'not available'
            msg = msg + status_code_info
            logging.error(msg)


def _mock_successful_response(result, given: dict = None):
    if given is None:
        given = dict(base_url='mocked.url',
                     url_path='/this_is_a_test_url_path',
                     params={'cookie_monster': 'who ate my cookie?'})

    _pretty_print_request(given['base_url'], given['url_path'], given['params'])
    return KnvbResponse(result)


def _mock_incorrect_hash_response():
    return KnvbResponse({"error": {"errorcode": "9992", "message": "Hash not correct"}})


def _mock_initialisatie_response():
    return {
        "errorcode": 1000, "message": "Ok",
        "List": [{
            "PHPSESSID": "_No_Fun_Without_PHPSESSID_",
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


def mock_teams_response():
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


def mock_uitslagen_response():
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
