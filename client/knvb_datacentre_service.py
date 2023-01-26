import client.knvb_datacentre_client as knvb_client
from client.util.mapper import flatten
from client.models.models import *


def get_all_wedstrijd_resultaten() -> list[ResultDAO]:
    teams: list[KnvbTeamInfoDTO] = knvb_client.get_all_teams()
    uitslagen: list[KnvbUitslagDTO] = flatten(
        [knvb_client.get_uitslagen_by_team_id(team_id=team.teamid, weeknummer='A') for team in teams]
    )
    return ResultDAO.instantiateFromKnvbUitslagDTOs(uitslagen)
