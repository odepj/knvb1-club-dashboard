import pandas as pd
from sqlalchemy import Column, Integer, String, Boolean, Float, Date

from database import Base


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(String(20), primary_key=True)
    username = Column(String(255))
    password = Column(String(255))
    email = Column(String(255))
    display_name = Column(String(255))
    is_admin = Column(Boolean(False))

    def __init__(self, id, username, password, email, display_name, is_admin, *args, **kwargs):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.display_name = display_name
        self.is_admin = is_admin
        super().__init__(*args, **kwargs)

    @classmethod
    def instantiate_from_dataframe(cls, df: pd.DataFrame) -> list:
        return list(map(lambda x: cls(*x), df.values.tolist()))


class Han(Base):
    __tablename__ = 'han'

    id = Column(Integer, primary_key=True)
    speler_code = Column(String(20))
    team_naam = Column(String(20))
    meting = Column(String(20))
    Staande_lengte = Column(Float())
    Zittende_lengte = Column(Float())
    Beenlengte = Column(Float())
    Zithoogte = Column(Float())
    Gewicht = Column(Float())
    Maturity_Offset = Column(Float())
    Balance_Beam_6cm = Column(Float())
    Balance_Beam_4_5cm = Column(Float())
    Balance_Beam_3cm = Column(Float())
    Balance_beam_totaal = Column(Float())
    Zijwaarts_springen_1 = Column(Float())
    Zijwaarts_springen_2 = Column(Float())
    Zijwaarts_springen_totaal = Column(Float())
    Zijwaarts_verplaatsen_1 = Column(Float())
    Zijwaarts_verplaatsen_2 = Column(Float())
    Zijwaarts_verplaatsen_totaal = Column(Float())
    Oog_hand_coordinatie_1 = Column(Float())
    Oog_hand_coordinatie_2 = Column(Float())
    Oog_hand_coordinatie_totaal = Column(Float())
    X10_meter_sprint_1 = Column(Float())
    X10_meter_sprint_2 = Column(Float())
    X10_meter_sprint_beste = Column(Float())
    X20_meter_sprint_1 = Column(Float())
    X20_meter_sprint_2 = Column(Float())
    X20_meter_sprint_beste = Column(Float())
    X30_meter_sprint_1 = Column(Float())
    X30_meter_sprint_2 = Column(Float())
    X30_meter_sprint_beste = Column(Float())
    CoD_links_1 = Column(Float())
    CoD_links_2 = Column(Float())
    CoD_links_beste = Column(Float())
    CoD_rechts_1 = Column(Float())
    CoD_rechts_2 = Column(Float())
    CoD_rechts_beste = Column(Float())
    Vertesprong_1 = Column(Float())
    Vertesprong_2 = Column(Float())
    Vertesprong_beste = Column(Float())
    club_code = Column(String(20))
    datum = Column(Date())
    geboortedatum = Column(Date())

    def __init__(self, speler_code, team_naam, meting, Staande_lengte, Zittende_lengte, Beenlengte, Zithoogte,
                 Gewicht, Maturity_Offset, Balance_Beam_6cm, Balance_Beam_4_5cm, Balance_Beam_3cm, Balance_beam_totaal,
                 Zijwaarts_springen_1, Zijwaarts_springen_2, Zijwaarts_springen_totaal, Zijwaarts_verplaatsen_1,
                 Zijwaarts_verplaatsen_2, Zijwaarts_verplaatsen_totaal, Oog_hand_coordinatie_1, Oog_hand_coordinatie_2,
                 Oog_hand_coordinatie_totaal, X10_meter_sprint_1, X10_meter_sprint_2, X10_meter_sprint_beste,
                 X20_meter_sprint_1, X20_meter_sprint_2, X20_meter_sprint_beste, X30_meter_sprint_1, X30_meter_sprint_2,
                 X30_meter_sprint_beste, CoD_links_1, CoD_links_2, CoD_links_beste, CoD_rechts_1, CoD_rechts_2,
                 CoD_rechts_beste, Vertesprong_1, Vertesprong_2, Vertesprong_beste, club_code, datum, geboortedatum,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.speler_code = speler_code
        self.team_naam = team_naam
        self.meting = meting
        self.Staande_lengte = Staande_lengte
        self.Zittende_lengte = Zittende_lengte
        self.Beenlengte = Beenlengte
        self.Zithoogte = Zithoogte
        self.Gewicht = Gewicht
        self.Maturity_Offset = Maturity_Offset
        self.Balance_Beam_6cm = Balance_Beam_6cm
        self.Balance_Beam_4_5cm = Balance_Beam_4_5cm
        self.Balance_Beam_3cm = Balance_Beam_3cm
        self.Balance_beam_totaal = Balance_beam_totaal
        self.Zijwaarts_springen_1 = Zijwaarts_springen_1
        self.Zijwaarts_springen_2 = Zijwaarts_springen_2
        self.Zijwaarts_springen_totaal = Zijwaarts_springen_totaal
        self.Zijwaarts_verplaatsen_1 = Zijwaarts_verplaatsen_1
        self.Zijwaarts_verplaatsen_2 = Zijwaarts_verplaatsen_2
        self.Zijwaarts_verplaatsen_totaal = Zijwaarts_verplaatsen_totaal
        self.Oog_hand_coordinatie_1 = Oog_hand_coordinatie_1
        self.Oog_hand_coordinatie_2 = Oog_hand_coordinatie_2
        self.Oog_hand_coordinatie_Totaal = Oog_hand_coordinatie_totaal
        self.X10_meter_sprint_1 = X10_meter_sprint_1
        self.X10_meter_sprint_2 = X10_meter_sprint_2
        self.X10_meter_sprint_beste = X10_meter_sprint_beste
        self.X20_meter_sprint_1 = X20_meter_sprint_1
        self.X20_meter_sprint_2 = X20_meter_sprint_2
        self.X20_meter_sprint_beste = X20_meter_sprint_beste
        self.X30_meter_sprint_1 = X30_meter_sprint_1
        self.X30_meter_sprint_2 = X30_meter_sprint_2
        self.X30_meter_sprint_beste = X30_meter_sprint_beste
        self.CoD_links_1 = CoD_links_1
        self.CoD_links_2 = CoD_links_2
        self.CoD_links_beste = CoD_links_beste
        self.CoD_rechts_1 = CoD_rechts_1
        self.CoD_rechts_2 = CoD_rechts_2
        self.CoD_rechts_beste = CoD_rechts_beste
        self.Vertesprong_1 = Vertesprong_1
        self.Vertesprong_2 = Vertesprong_2
        self.Vertesprong_beste = Vertesprong_beste
        self.club_code = club_code
        self.datum = datum
        self.geboortedatum = geboortedatum

    @classmethod
    def instantiate_from_dataframe(cls, df: pd.DataFrame) -> list:
        return list(map(lambda x: cls(*x), df.values.tolist()))
