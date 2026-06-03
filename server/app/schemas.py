from pydantic import BaseModel, EmailStr
from typing import Optional, Union
from datetime import date, datetime
from decimal import Decimal

class BenutzerOut(BaseModel):
    Benutzer_id: int
    Name: Optional[str]
    Nachname: Optional[str]
    Email: Optional[EmailStr]
    Rolle: Optional[str]
    class Config: orm_mode = True

class DateiOut(BaseModel):
    Id: int
    Antrag_id: int
    Dateipfad: Optional[str]
    Name: Optional[str]
    class Config: orm_mode = True

class KommentarOut(BaseModel):
    Kommentar_id: int
    Antrag_id: int
    Text_: Optional[str]
    Zeitpunkt: Optional[datetime]
    class Config: orm_mode = True

class AntragOut(BaseModel):
    Antrag_id: int
    Benutzer_id: Optional[int]
    Antrag_typ: Optional[int]
    Status_eins: Optional[str]
    Status_zwei: Optional[str]
    Pruefer_eins: Optional[str]
    Pruefer_zwei: Optional[str]
    Punkte: Optional[Decimal]
    class Config: orm_mode = True

# ----- Antrag 1 -----
class AntragEinsOut(BaseModel):
    Antrag_id: int
    antrag_Antrag_id: Optional[int]
    Antragsteller_name: Optional[str]
    Fachbereich: Optional[str]
    Ermaessigung_SWS: Optional[Decimal]
    Titel_des_Vorhabens: Optional[str]
    Beginn: Optional[date]
    Ende: Optional[date]
    Drittmittelgeber: Optional[str]
    Drittmittel_gesamt_HTW: Optional[Decimal]
    Drittmittel_zugeordnet: Optional[Decimal]
    Drittmittel_verfuegbar: Optional[Decimal]
    Drittmittel_eingesetzt_semester: Optional[Decimal]
    Einnahmen_nebentaetigkeit: Optional[int]
    class Config: orm_mode = True

# ----- Antrag 2a -----
class AntragZweiAOut(BaseModel):
    Antrag_id: int
    antrag_Antrag_id: Optional[int]
    Antragsteller_name: Optional[str]
    Fachbereich: Optional[str]
    Ermaessigung_SWS: Optional[Decimal]
    Titel_veroeffentlichung: Optional[str]
    Alleinautor: Optional[int]
    Koautor: Optional[int]
    Bibliographische_angaben: Optional[str]
    Erscheinungsdatum: Optional[date]
    Peer_Review: Optional[int]
    Drittbegutachtung: Optional[int]
    Einnahmen_nebentaetigkeit: Optional[int]
    class Config: orm_mode = True

# ----- Antrag 2b -----
class AntragZweiBOut(BaseModel):
    Antrag_id: int
    antrag_Antrag_id: Optional[int]
    Antragsteller_name: Optional[str]
    Fachbereich: Optional[str]
    Titel_praesentation: Optional[str]
    Erscheinungsdatum: Optional[date]
    Beteiligung: Optional[str]
    Format_A: Optional[int]
    Format_B: Optional[int]
    Format_C: Optional[int]
    Zusatz_optionen: Optional[Union[str, dict]]
    Einnahmen_nebentaetigkeit: Optional[int]
    class Config: orm_mode = True

# ----- Antrag 3a -----
class AntragDreiAOut(BaseModel):
    Antrag_id: int
    antrag_Antrag_id: Optional[int]
    Antragsteller_name: Optional[str]
    Beteiligte_Universitaet: Optional[str]
    Promovend_name: Optional[str]
    Arbeitstitel: Optional[str]
    Beginn_Betreuung: Optional[date]
    Zeitraum_von: Optional[date]
    Zeitraum_bis: Optional[date]
    class Config: orm_mode = True

# ----- Antrag 3b -----
class AntragDreiBOut(BaseModel):
    Antrag_id: int
    antrag_Antrag_id: Optional[int]
    Antragsteller_name: Optional[str]
    Beteiligte_Universitaet: Optional[str]
    Promovend_name: Optional[str]
    Titel_Dissertation: Optional[str]
    Datum_Disp: Optional[date]
    Zeitraum_von: Optional[date]
    Zeitraum_bis: Optional[date]
    Einnahmen_nebentaetigkeit: Optional[int]
    class Config: orm_mode = True

