import json

from client.knvb_datacentre_client import fetch_wedstrijd_resultaten, KnvbDatacentreClient
from client.models.response import KnvbResponse


class KnvbService:

    def __init__(self):
        knvb_client = KnvbDatacentreClient()

    def get_wedstrijd_resultaten(club: str, team: str):
        api_response = fetch_wedstrijd_resultaten()
        result = KnvbResponse(**json.loads(api_response))

        res = KnvbDatacentreClient.fetch_wedstrijd_resultaten()

        print(*res("", "").List)
        return result

