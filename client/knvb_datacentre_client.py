import json
import os
from hashlib import md5

import requests

from client.models.request import KnvbAuthorisedRequest
from client.models.response import KnvbResponse


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


# Additional information about the API can be found at: https://api.knvbdataservice.nl/hoofdstuk/teams/1234/results


