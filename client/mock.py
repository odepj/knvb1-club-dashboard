import os
from hashlib import md5


def _mock_resp(input, output):
    return output


def _mock_uitslagen_response():
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


# #Initialisatie
#   #PathName -> Unieke pathname voor de club zoals vastgelegd in het admin interface.
#   #PHPSESSID (request-param) -> https://api.voetbaldatacentre.nl/api/initialisatie/<PathName>

#    #Session ID als salt gebruikt voor de MD5 hash, welke verder gebruik maakt van de statische key die door voetbaldatacentre wordt verstrekt.
#    #_'KEY' is hierbij:
#     #De 'secret key' die aan app ontwikkelaars is verstrekt, of
#     #De API sleutel die de sitebeheerder via het admin interface kan verkrijgen indien het API product besteld is.
#   #Voorbeeld: md5('mobapi_static_key#clubs/BB44ABC/results#eff1a8d6311bb132338681570456fbcd')
#   #hash (request-param) -> md5(key#/teams#session_id) == md5('<key>#<url_path>#<session_id>');

# #Input parameters
#    pathname: Unieke pathname voor de club zoals vastgelegd in het admin interface.
#    apiversion: Deze parameter is optioneel; in sommige gevallen kan er een bepaald versie nummer van de API mee afgedwongen worden.
def _mock_get_auth_query_parameters():
    # https://api.voetbaldatacentre.nl/api/initialisatie/<pathname>[&apiversion=1.0]
    auth_path = '/unique_path_name'
    api_key = os.getenv('VOETBAL_DATACENTRE_API_KEY')

    php_sess_id = _mock_resp(auth_path, 'A_PHPSESSID_CODE')
    hash = md5(f'{api_key}#{auth_path}#{php_sess_id}')
    return
