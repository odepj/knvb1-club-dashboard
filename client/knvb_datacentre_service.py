import json

from client.knvb_datacentre_client import fetch_wedstrijd_resultaten, KnvbDatacentreClient
from client.models.response import KnvbResponse


def get_wedstrijd_resultaten(club: str, team: str):
    api_response = fetch_wedstrijd_resultaten()
    result = KnvbResponse(**json.loads(api_response))

    res = KnvbDatacentreClient.get_team_information()

    return result


print(*get_wedstrijd_resultaten("", "").List)
