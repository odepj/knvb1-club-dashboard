from datetime import date, time


def _instantiateFromList(List):
    return list(map(lambda x: KnvbUitslagDTO(**x), List))


class KnvbTeamInfoDTO:
    def __init__(self, teamid, teamname, speeldag, categorie, regulierecompetitie, bekercompetitie, nacompetitie):
        self.teamid = teamid
        self.teamname = teamname
        self.speeldag = speeldag
        self.categorie = categorie
        self.regulierecompetitie = regulierecompetitie
        self.bekercompetitie = bekercompetitie
        self.nacompetitie = nacompetitie


class KnvbUitslagDTO:
    def __init__(self,
                 MatchID: int,
                 WedstrijdNummer: int,
                 Datum: date,
                 Tijd: time,
                 ThuisClub: str,
                 ThuisLogo: str,
                 ThuisTeamID: int,
                 UitClub: str,
                 UitLogo: str,
                 UitTeamID: int,
                 PuntenTeam1: int,
                 PuntenTeam2: int,
                 PuntenTeam1Verl: int = None,
                 PuntenTeam2Verl: int = None,
                 PuntenTeam1Strafsch: int = None,
                 PuntenTeam2Strafsch: int = None,
                 Bijzonderheden: str = "",
                 Scheidsrechter: str = "",
                 CompType: str = "",
                 CompNummer: str = "",
                 WedstrijdDag: int = None):
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


class KnvbTeamInfoResponse:
    def __init__(self, errorcode: int, message: str, List: list):
        self.errorcode: int = errorcode
        self.message: str = message
        self.knvbUitslagenDTOs: list = _instantiateFromList(List=List)


class KnvbResponse:
    def __init__(self, errorcode: int, message: str, List: list):
        self.errorcode: int = errorcode
        self.message: str = message
        self.List: list = _instantiateFromList(List=List)

    def __str__(self) -> str:
        return f'errorcode: {self.errorcode}, message: {self.message}, uitslagen: {self.List}'
