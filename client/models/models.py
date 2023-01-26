from datetime import date, time

from client.util.mapper import instantiateClassFromList


class ResultDAO:
    def __init__(self, MatchID, Datum, ThuisClub, UitClub, PuntenTeam1, PuntenTeam2, PuntenTeam1Verl,
                 PuntenTeam2Verl, PuntenTeam1Strafsch, PuntenTeam2Strafsch, Bijzonderheden):
        self.MatchID = MatchID
        self.Datum = Datum
        self.ThuisClub = ThuisClub
        self.UitClub = UitClub
        self.PuntenTeam1 = PuntenTeam1
        self.PuntenTeam2 = PuntenTeam2
        self.PuntenTeam1Verl = PuntenTeam1Verl
        self.PuntenTeam2Verl = PuntenTeam2Verl
        self.PuntenTeam1Strafsch = PuntenTeam1Strafsch
        self.PuntenTeam2Strafsch = PuntenTeam2Strafsch
        self.Bijzonderheden = Bijzonderheden

    def __str__(self) -> str:
        return f'MatchID: {self.MatchID}\n Datum: {self.Datum}\n ThuisClub: {self.ThuisClub}\n UitClub: {self.UitClub}\n PuntenTeam1: {self.PuntenTeam1}\n PuntenTeam2: {self.PuntenTeam2}\n PuntenTeam1Verl: {self.PuntenTeam1Verl}\n PuntenTeam2Verl: {self.PuntenTeam2Verl}\n PuntenTeam1Strafsch: {self.PuntenTeam1Strafsch}\n PuntenTeam2Strafsch: {self.PuntenTeam2Strafsch}\n Bijzonderheden: {self.Bijzonderheden}\n'

    @classmethod
    def instantiateFromKnvbUitslagDTOs(cls, knvbUitslagDTOs):
        return [cls(knvbUitslagDto.MatchID,
                    knvbUitslagDto.Datum,
                    knvbUitslagDto.ThuisClub,
                    knvbUitslagDto.UitClub,
                    knvbUitslagDto.PuntenTeam1,
                    knvbUitslagDto.PuntenTeam2,
                    knvbUitslagDto.PuntenTeam1Verl,
                    knvbUitslagDto.PuntenTeam2Verl,
                    knvbUitslagDto.PuntenTeam1Strafsch,
                    knvbUitslagDto.PuntenTeam2Strafsch,
                    knvbUitslagDto.Bijzonderheden) for knvbUitslagDto in knvbUitslagDTOs]


class KnvbTeamInfoDTO:
    def __init__(self, teamid, teamname, speeldag, categorie, regulierecompetitie, bekercompetitie, nacompetitie):
        self.teamid = teamid
        self.teamname = teamname
        self.speeldag = speeldag
        self.categorie = categorie
        self.regulierecompetitie = regulierecompetitie
        self.bekercompetitie = bekercompetitie
        self.nacompetitie = nacompetitie

    def __str__(self) -> str:
        return f'teamid: {self.teamid},\n teamname: {self.teamname},\n speeldag: {self.speeldag},\n categorie: {self.categorie},\n regulierecompetitie: {self.regulierecompetitie},\n bekercompetitie: {self.bekercompetitie},\n nacompetitie: {self.nacompetitie}\n'


class KnvbUitslagDTO:
    def __init__(self, MatchID: int, WedstrijdNummer: int, Datum: date, Tijd: time, ThuisClub: str, ThuisLogo: str,
                 ThuisTeamID: int, UitClub: str, UitLogo: str, UitTeamID: int, PuntenTeam1: int, PuntenTeam2: int,
                 PuntenTeam1Verl: int = None, PuntenTeam2Verl: int = None, PuntenTeam1Strafsch: int = None,
                 PuntenTeam2Strafsch: int = None, Bijzonderheden: str = "", Scheidsrechter: str = "",
                 CompType: str = "", CompNummer: str = "", WedstrijdDag: int = None):
        self.MatchID = MatchID
        self.WedstrijdNummer = WedstrijdNummer
        self.Datum = Datum
        self.Tijd = Tijd
        self.ThuisClub = ThuisClub
        self.ThuisLogo = ThuisLogo
        self.ThuisTeamID = ThuisTeamID
        self.UitClub = UitClub
        self.UitLogo = UitLogo
        self.UitTeamID = UitTeamID
        self.PuntenTeam1 = PuntenTeam1
        self.PuntenTeam2 = PuntenTeam2
        self.PuntenTeam1Verl = PuntenTeam1Verl
        self.PuntenTeam2Verl = PuntenTeam2Verl
        self.PuntenTeam1Strafsch = PuntenTeam1Strafsch
        self.PuntenTeam2Strafsch = PuntenTeam2Strafsch
        self.Bijzonderheden = Bijzonderheden
        self.Scheidsrechter = Scheidsrechter
        self.CompType = CompType
        self.CompNummer = CompNummer
        self.WedstrijdDag = WedstrijdDag

    def __str__(self) -> str:
        return f'MatchID: {self.MatchID}, Datum: {self.Datum}, ThuisClub: {self.ThuisClub}, UitClub: {self.UitClub}'


class KnvbResponse:
    def __init__(self, data):
        data = data['error'] if 'error' in data.keys() else data
        self.errorcode: int = data['errorcode']
        self.message: str = data['message']
        self.List: list = instantiateClassFromList(cls=dict, List=data['List']) if 'List' in data.keys() else None

    def __str__(self) -> str:
        return f"KnvbResponse: {'{'}errorcode: {self.errorcode}, message: \"{self.message}\", list: {self.List}{'}'}"
