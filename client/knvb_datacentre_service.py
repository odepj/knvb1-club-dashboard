import client.mock_knvb_datacenter_client as mock_client
import client.knvb_datacentre_client as knvb_client
from client.mapper import flatten
from client.models.response import *


def mock_get_all_wedstrijd_resultaten():
    teams = mock_client.get_teams()
    team_uitslagen_dtos = flatten([mock_client.get_uitslagen(team.teamid, 'A') for team in teams])
    resultDAOs = ResultDAO.instanciateFromKnvbUitslagDTOs(team_uitslagen_dtos)
    print(resultDAOs[0])


def get_all_wedstrijd_resultaten():
    teams: list[KnvbTeamInfoDTO] = knvb_client.get_all_teams()
    uitslagen: list[KnvbUitslagDTO] = flatten([knvb_client.get_uitslagen_by_team_id(team_id=team.teamid) for team in teams])
    return uitslagen


mock_get_all_wedstrijd_resultaten()
get_all_wedstrijd_resultaten()


