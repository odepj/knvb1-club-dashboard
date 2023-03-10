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

    id = Column(Integer, primary_key=True, autoincrement=True)
    allocatie_id = Column(Integer())
    speler_id = Column(String(20))
    team_naam = Column(String(20))
    reeks_naam = Column(String(20))
    Staande_lengte = Column(Float())
    Zittende_lengte = Column(Float())
    Beenlengte = Column(Float())
    Zithoogte = Column(Float())
    Gewicht = Column(Float())
    Maturity_Offset = Column(Float())
    Balance_Beam_6cm = Column(Integer())
    Balance_Beam_4_5cm = Column(Integer())
    Balance_Beam_3cm = Column(Integer())
    Balance_beam_totaal = Column(Integer())
    Zijwaarts_springen_1 = Column(Integer())
    Zijwaarts_springen_2 = Column(Integer())
    Zijwaarts_springen_totaal = Column(Integer())
    Zijwaarts_verplaatsen_1 = Column(Integer())
    Zijwaarts_verplaatsen_2 = Column(Integer())
    Zijwaarts_verplaatsen_totaal = Column(Integer())
    Oog_hand_coordinatie_1 = Column(Integer())
    Oog_hand_coordinatie_2 = Column(Integer())
    Oog_hand_coordinatie_totaal = Column(Integer())
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
    bvo_naam = Column(String(20))
    Testdatum = Column(Date())
    geboortedatum = Column(Date())
    reeks_id = Column(Integer())
    seizoen = Column(String(20))

    def __init__(self,
                    allocatie_id, speler_id, team_naam, reeks_naam, Staande_lengte, Zittende_lengte, Beenlengte, 
                    Zithoogte, Gewicht, Maturity_Offset, Balance_Beam_6cm, Balance_Beam_4_5cm,
                    Balance_Beam_3cm, Balance_beam_totaal, Zijwaarts_springen_1, Zijwaarts_springen_2, 
                    Zijwaarts_springen_totaal, Zijwaarts_verplaatsen_1, Zijwaarts_verplaatsen_2, 
                    Zijwaarts_verplaatsen_totaal, Oog_hand_coordinatie_1, Oog_hand_coordinatie_2, 
                    Oog_hand_coordinatie_totaal, X10_meter_sprint_1, X10_meter_sprint_2, X10_meter_sprint_beste,
                    X20_meter_sprint_1, X20_meter_sprint_2, X20_meter_sprint_beste, X30_meter_sprint_1, 
                    X30_meter_sprint_2, X30_meter_sprint_beste, CoD_links_1, CoD_links_2, CoD_links_beste, 
                    CoD_rechts_1, CoD_rechts_2, CoD_rechts_beste, Vertesprong_1, Vertesprong_2, 
                    Vertesprong_beste, bvo_naam, Testdatum, geboortedatum, reeks_id, seizoen, *args, **kwargs):
        self.allocatie_id = allocatie_id
        self.speler_id = speler_id
        self.team_naam = team_naam
        self.reeks_naam = reeks_naam
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
        self.Oog_hand_coordinatie_totaal = Oog_hand_coordinatie_totaal
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
        self.bvo_naam = bvo_naam
        self.Testdatum = Testdatum
        self.geboortedatum = geboortedatum
        self.reeks_id = reeks_id
        self.seizoen = seizoen
        super().__init__(*args, **kwargs)

    @classmethod
    def instantiate_from_dataframe(cls, df: pd.DataFrame) -> list:
        return list(map(lambda x: cls(*x), df.values.tolist()))
