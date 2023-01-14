from datetime import date, time


def _do(obj, cls):
    print(obj)
    print(cls)
    return cls(obj)


def _instantiateFromList(cls, List):
    if isinstance(List[0], type(dict)):
        return list(map(lambda x: cls(**x), List))

    return [_do(x, cls) for x in List]


def flatten(S):
    if S == []:
        return S
    if isinstance(S[0], list):
        return flatten(S[0]) + flatten(S[1:])
    return S[:1] + flatten(S[1:])


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

        # return list(map(lambda x: cls(*x), df.values.tolist()))

    def __str__(self) -> str:
        return f'MatchID: {self.MatchID}\n Datum: {self.Datum}\n ThuisClub: {self.ThuisClub}\n UitClub: {self.UitClub}\n PuntenTeam1: {self.PuntenTeam1}\n PuntenTeam2: {self.PuntenTeam2}\n PuntenTeam1Verl: {self.PuntenTeam1Verl}\n PuntenTeam2Verl: {self.PuntenTeam2Verl}\n PuntenTeam1Strafsch: {self.PuntenTeam1Strafsch}\n PuntenTeam2Strafsch: {self.PuntenTeam2Strafsch}\n Bijzonderheden: {self.Bijzonderheden}\n'

    @classmethod
    def instanciateFromKnvbUitslagDTOs(cls, knvbUitslagDTOs):
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
        self.knvbUitslagenDTOs: list = _instantiateFromList(cls=KnvbUitslagDTO, List=List)


class KnvbResponse:
    def __init__(self, errorcode: int, message: str, List: list = None):
        print('init KnvbResponse')
        self.errorcode: int = errorcode
        self.message: str = message
        self.List: list = _instantiateFromList(cls=dict, List=List)

    # def __init__(self, error):
    #     self.__init__(errorcode=error['errorcode'], message=error['message'])

    def __str__(self) -> str:
        return f'errorcode: {self.errorcode}, message: {self.message}, uitslagen: {self.List}'
