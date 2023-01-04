import json
import os
from hashlib import md5

import requests

from client.models.request import KnvbAuthorisedRequest
from client.models.response import KnvbResponse


# #Initialisatie
#   #PathName -> Unieke pathname voor de club zoals vastgelegd in het admin interface.
#   #PHPSESSID (request-param) -> https://api.voetbaldatacentre.nl/api/initialisatie/<PathName>

#    Session ID als salt gebruikt voor de MD5 hash, welke verder gebruik maakt van de statische key die door voetbaldatacentre wordt verstrekt.
#   'key' is hierbij:
#     De 'secret key' die aan app ontwikkelaars is verstrekt, of
#     De API sleutel die de sitebeheerder via het admin interface kan verkrijgen indien het API product besteld is.
#   #Voorbeeld: md5('mobapi_static_key#clubs/BB44ABC/results#eff1a8d6311bb132338681570456fbcd')
#   #hash (request-param) -> md5(key#/teams#session_id) == md5('<key>#<url_path>#<session_id>');

# #Input parameters
#    pathname: Unieke pathname voor de club zoals vastgelegd in het admin interface.
#    apiversion: Deze parameter is optioneel; in sommige gevallen kan er een bepaald versie nummer van de API mee afgedwongen worden.

#
# #Output parameters

#    error: Error code als er een fout was
#    OF
#    PHPSESSID: Session ID
#    clubnaam: Volledige naam van club
#    apiversion: Versie van de API
#    changed: Datum en tijd waarop de laatste wijziging heeft plaatsgevonden
#    changelog: URL van changelog waar aanwezige versie van de API kunnen worden gecontroleerd
#    logo: URL van clublogo
#    kleuren: Een array van kleuren die ingesteld zijn voor de app
#    rss: nvt
#    twitter: nvt
#    twittertags: nvt
#    appsponsor: nvt

# #Req teams
# #Input parameters

#    PHPSESSID: Session ID verkregen uit initialisatie
#    hash: Hash berekend aan client side
base_url = os.getenv('VOETBAL_DATACENTRE_CLIENT_BASEURL')
headers = {'HTTP_X_APIKEY': os.getenv('VOETBAL_DATACENTRE_API_KEY')}


def _get_team_information(request_template: KnvbAuthorisedRequest, additional_information):
    requests.get(base_url + "/teams")


    return 'stuff'

    # #Output parameters

    #   {
    #       "errorcode":1000,"message":"Ok, Team Listing follows",
    #       "List":[
    #           {
    #               "teamid":"122561",
    #               "teamname":"Zilvermeeuwen 1",
    #               "speeldag":"ZO",
    #               "categorie":"Senioren",
    #               "regulierecompetitie":"J",
    #               "bekercompetitie":"J",
    #               "nacompetitie":"N"
    #           },{
    #               "teamid":"122564",
    #               "teamname":"Zilvermeeuwen 2",
    #               "speeldag":"ZO",
    #               "categorie":"Senioren",
    #               "regulierecompetitie":"J",
    #               "bekercompetitie":"J",
    #               "nacompetitie":"N"
    #           }
    #       ]
    #   }
    #

    # #Req uitslagen
    #
    # https://api.voetbaldatacentre.nl/api/teams/<teamid>/results?[weeknummer=12][&comptype=R|B|N|V&]PHPSESSID=<12345>&hash=<abbccdde200394>
    # #Input parameters
    #
    #     PHPSESSID: Session ID verkregen uit initialisatie
    #     hash: Hash berekend aan client side
    #     teamid: Uniek Team ID. Let op, team moet team van club zijn.
    #     weeknummer: week waarvan de uitslagen worden opgehaald (1-52, A) (optioneel)
    #     comptype: Competitie type R = Regulier, B = Beker, N = Nacompetitie, V = Vriendschappelijke Competitie

    # #Output -> KnvbUitslagenDTO


KNVB_API = 'https://api.voetbaldatacentre.nl/'

print(requests.get('https://api.voetbaldatacentre.nl/api/initialisatie/clubs/BB44ABC/results',
                   headers={'HTTP_X_APIKEY': '12'}).json())


def _get_authorised_template_request():
    # #https://api.voetbaldatacentre.nl/api/initialisatie/EXAMPLE_PATH
    session_url = os.getenv('VOETBAL_DATACENTRE_CLIENT_BASEURL') + os.getenv('VOETBAL_DATACENTRE_API_URL_PATH')
    headers = {'HTTP_X_APIKEY': os.getenv('VOETBAL_DATACENTRE_API_KEY')}
    result = requests.get(session_url, headers=headers)

    # Print result for now
    print('session request result:', result)

    return KnvbAuthorisedRequest(information="")


def _mock_fetch():
    return """{
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
}"""


# Additional information about the API can be found at: https://api.knvbdataservice.nl/hoofdstuk/teams/1234/results
class KnvbDatacentreClient:
    def fetch_wedstrijd_resultaten(self):
        req = _get_authorised_template_request()
        res = _get_team_information(req, additional_information="")
        return _mock_fetch()
