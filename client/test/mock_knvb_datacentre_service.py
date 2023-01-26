import mock_knvb_datacentre_client as mock_client
from client.models.models import ResultDAO
from client.util.mapper import flatten


def mock_get_all_wedstrijd_resultaten():
    teams = mock_client.mock_get_all_teams()
    team_uitslagen_dtos = flatten([mock_client.mock_get_uitslagen_by_team_id(team.teamid) for team in teams])
    resultDAOs = ResultDAO.instantiateFromKnvbUitslagDTOs(team_uitslagen_dtos)

    for team in teams:
        print(team)
    for result in resultDAOs:
        print(result)


mock_get_all_wedstrijd_resultaten()
