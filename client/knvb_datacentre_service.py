import json

import client.knvb_datacentre_client as knvb_datacenter_client
import client.mock as mock_client
from client.models.response import *


def get_all_wedstrijd_resultaten():
    teams = mock_client.get_teams()
    team_uitslagen_dtos = flatten([mock_client.get_uitslagen(team.teamid, 'A') for team in teams])
    resultDAOs = ResultDAO.instanciateFromKnvbUitslagDTOs(team_uitslagen_dtos)
    for dao in resultDAOs:
        print(dao)

get_all_wedstrijd_resultaten()
