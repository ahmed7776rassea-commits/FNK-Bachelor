from typing import List, Optional

from sqlalchemy import DECIMAL, Date, DateTime, Enum, ForeignKeyConstraint, Index, String, Text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime
import decimal

class Base(DeclarativeBase):
    pass


class Benutzer(Base):
    __tablename__ = 'benutzer'

    Benutzer_id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    Name: Mapped[Optional[str]] = mapped_column(String(100))
    Nachname: Mapped[Optional[str]] = mapped_column(String(100))
    Email: Mapped[Optional[str]] = mapped_column(String(100))
    Rolle: Mapped[Optional[str]] = mapped_column(Enum('Admin', 'Fnk', 'Antragsteller'))

    antrag: Mapped[List['Antrag']] = relationship('Antrag', back_populates='Benutzer_')


class Antrag(Base):
    __tablename__ = 'antrag'
    __table_args__ = (
        ForeignKeyConstraint(['Benutzer_id'], ['benutzer.Benutzer_id'], name='antrag_ibfk_1'),
        Index('Benutzer_id', 'Benutzer_id')
    )

    Antrag_id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True,autoincrement=True)
    Benutzer_id: Mapped[Optional[int]] = mapped_column(INTEGER(11))
    Antrag_typ: Mapped[Optional[int]] = mapped_column(INTEGER(11))
    Status_eins: Mapped[Optional[str]] = mapped_column(String(50))
    Status_zwei: Mapped[Optional[str]] = mapped_column(String(45))
    Pruefer_eins: Mapped[Optional[str]] = mapped_column(String(45))
    Pruefer_zwei: Mapped[Optional[str]] = mapped_column(String(45))
    Punkte: Mapped[decimal.Decimal] = mapped_column(DECIMAL(3, 1), nullable=False, default=decimal.Decimal('0.0'))
    

    Benutzer_: Mapped[Optional['Benutzer']] = relationship('Benutzer', back_populates='antrag')
    antrag_drei_a: Mapped[List['AntragDreiA']] = relationship('AntragDreiA', back_populates='antrag_Antrag')
    antrag_drei_b: Mapped[List['AntragDreiB']] = relationship('AntragDreiB', back_populates='antrag_Antrag')
    antrag_eins: Mapped[List['AntragEins']] = relationship('AntragEins', back_populates='antrag_Antrag')
    antrag_zwei_a: Mapped[List['AntragZweiA']] = relationship('AntragZweiA', back_populates='antrag_Antrag')
    antrag_zwei_b: Mapped[List['AntragZweiB']] = relationship('AntragZweiB', back_populates='antrag_Antrag')
    datei: Mapped[List['Datei']] = relationship('Datei', back_populates='Antrag_')
    kommentar: Mapped[List['Kommentar']] = relationship('Kommentar', back_populates='Antrag_')


class AntragDreiA(Base):
    __tablename__ = 'antrag_drei_a'
    __table_args__ = (
        ForeignKeyConstraint(['antrag_Antrag_id'], ['antrag.Antrag_id'], name='antrag_drei_a_ibfk_1'),
        Index('antrag_Antrag_id', 'antrag_Antrag_id')
    )

    Antrag_id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    antrag_Antrag_id: Mapped[Optional[int]] = mapped_column(INTEGER(11))
    Antragsteller_name: Mapped[Optional[str]] = mapped_column(String(100))
    Beteiligte_Universitaet: Mapped[str] = mapped_column(String(255))
    Promovend_name: Mapped[str] = mapped_column(String(100))
    Arbeitstitel: Mapped[str] = mapped_column(String(255))
    Beginn_Betreuung: Mapped[datetime.date] = mapped_column(Date)
    Zeitraum_von: Mapped[datetime.date] = mapped_column(Date)
    Zeitraum_bis: Mapped[datetime.date] = mapped_column(Date)
    

    antrag_Antrag: Mapped[Optional['Antrag']] = relationship('Antrag', back_populates='antrag_drei_a')


class AntragDreiB(Base):
    __tablename__ = 'antrag_drei_b'
    __table_args__ = (
        ForeignKeyConstraint(['antrag_Antrag_id'], ['antrag.Antrag_id'], name='antrag_drei_b_ibfk_1'),
        Index('antrag_Antrag_id', 'antrag_Antrag_id')
    )

    Antrag_id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    antrag_Antrag_id: Mapped[Optional[int]] = mapped_column(INTEGER(11))
    Antragsteller_name: Mapped[Optional[str]] = mapped_column(String(100))
    Beteiligte_Universitaet: Mapped[str] = mapped_column(String(255))
    Promovend_name: Mapped[str] = mapped_column(String(100))
    Titel_Dissertation: Mapped[str] = mapped_column(String(255))
    Datum_Disp: Mapped[datetime.date] = mapped_column(Date)
    Zeitraum_von: Mapped[datetime.date] = mapped_column(Date)
    Zeitraum_bis: Mapped[datetime.date] = mapped_column(Date)
    Einnahmen_nebentaetigkeit: Mapped[Optional[int]] = mapped_column(TINYINT(1))

    antrag_Antrag: Mapped[Optional['Antrag']] = relationship('Antrag', back_populates='antrag_drei_b')


class AntragEins(Base):
    __tablename__ = 'antrag_eins'
    __table_args__ = (
        ForeignKeyConstraint(['antrag_Antrag_id'], ['antrag.Antrag_id'], name='antrag_eins_ibfk_1'),
        Index('antrag_Antrag_id', 'antrag_Antrag_id')
    )

    Antrag_id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    antrag_Antrag_id: Mapped[Optional[int]] = mapped_column(INTEGER(11))
    Antragsteller_name: Mapped[Optional[str]] = mapped_column(String(100))
    Fachbereich: Mapped[Optional[str]] = mapped_column(String(100))
    Ermaessigung_SWS: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(2, 1))
    Titel_des_Vorhabens: Mapped[Optional[str]] = mapped_column(String(255))
    Beginn: Mapped[Optional[datetime.date]] = mapped_column(Date)
    Ende: Mapped[Optional[datetime.date]] = mapped_column(Date)
    Drittmittelgeber: Mapped[Optional[str]] = mapped_column(String(255))
    Drittmittel_gesamt_HTW: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(10, 2))
    Drittmittel_zugeordnet: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(10, 2))
    Drittmittel_verfuegbar: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(10, 2))
    Drittmittel_eingesetzt_semester: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(10, 2))
    Einnahmen_nebentaetigkeit: Mapped[Optional[int]] = mapped_column(TINYINT(1))

    antrag_Antrag: Mapped[Optional['Antrag']] = relationship('Antrag', back_populates='antrag_eins')


class AntragZweiA(Base):
    __tablename__ = 'antrag_zwei_a'
    __table_args__ = (
        ForeignKeyConstraint(['antrag_Antrag_id'], ['antrag.Antrag_id'], name='antrag_zwei_a_ibfk_1'),
        Index('antrag_Antrag_id', 'antrag_Antrag_id')
    )

    Antrag_id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    antrag_Antrag_id: Mapped[Optional[int]] = mapped_column(INTEGER(11))
    Antragsteller_name: Mapped[Optional[str]] = mapped_column(String(100))
    Fachbereich: Mapped[Optional[str]] = mapped_column(String(100))
    Ermaessigung_SWS: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(2, 1))
    Titel_veroeffentlichung: Mapped[Optional[str]] = mapped_column(String(255))
    Alleinautor: Mapped[Optional[int]] = mapped_column(TINYINT(1))
    Koautor: Mapped[Optional[int]] = mapped_column(TINYINT(1))
    Bibliographische_angaben: Mapped[Optional[str]] = mapped_column(Text)
    Erscheinungsdatum: Mapped[Optional[datetime.date]] = mapped_column(Date)
    Peer_Review: Mapped[Optional[int]] = mapped_column(TINYINT(1))
    Drittbegutachtung: Mapped[Optional[int]] = mapped_column(TINYINT(1))
    Einnahmen_nebentaetigkeit: Mapped[Optional[int]] = mapped_column(TINYINT(1))

    antrag_Antrag: Mapped[Optional['Antrag']] = relationship('Antrag', back_populates='antrag_zwei_a')


class AntragZweiB(Base):
    __tablename__ = 'antrag_zwei_b'
    __table_args__ = (
        ForeignKeyConstraint(['antrag_Antrag_id'], ['antrag.Antrag_id'], name='antrag_zwei_b_ibfk_1'),
        Index('antrag_Antrag_id', 'antrag_Antrag_id')
    )

    Antrag_id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    antrag_Antrag_id: Mapped[Optional[int]] = mapped_column(INTEGER(11))
    Antragsteller_name: Mapped[Optional[str]] = mapped_column(String(100))
    Fachbereich: Mapped[Optional[str]] = mapped_column(String(100))
    Titel_praesentation: Mapped[Optional[str]] = mapped_column(Text)
    Erscheinungsdatum: Mapped[Optional[datetime.date]] = mapped_column(Date)
    Beteiligung: Mapped[Optional[str]] = mapped_column(String(50))
    Format_A: Mapped[Optional[int]] = mapped_column(TINYINT(1))
    Format_B: Mapped[Optional[int]] = mapped_column(TINYINT(1))
    Format_C: Mapped[Optional[int]] = mapped_column(TINYINT(1))
    Zusatz_optionen: Mapped[Optional[str]] = mapped_column(Text)
    Einnahmen_nebentaetigkeit: Mapped[Optional[int]] = mapped_column(TINYINT(1))

    antrag_Antrag: Mapped[Optional['Antrag']] = relationship('Antrag', back_populates='antrag_zwei_b')


class Datei(Base):
    __tablename__ = 'datei'
    __table_args__ = (
        ForeignKeyConstraint(['Antrag_id'], ['antrag.Antrag_id'], name='datei_ibfk_1'),
        Index('Antrag_id', 'Antrag_id')
    )

    Id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    Antrag_id: Mapped[Optional[int]] = mapped_column(INTEGER(11))
    Dateipfad: Mapped[Optional[str]] = mapped_column(String(255))
    Name: Mapped[Optional[str]] = mapped_column(String(255))

    Antrag_: Mapped[Optional['Antrag']] = relationship('Antrag', back_populates='datei')


class Kommentar(Base):
    __tablename__ = 'kommentar'
    __table_args__ = (
        ForeignKeyConstraint(['Antrag_id'], ['antrag.Antrag_id'], name='kommentar_ibfk_1'),
        Index('Antrag_id', 'Antrag_id')
    )

    Kommentar_id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    Antrag_id: Mapped[Optional[int]] = mapped_column(INTEGER(11))
    Text_: Mapped[Optional[str]] = mapped_column('Text', Text)
    Zeitpunkt: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    Antrag_: Mapped[Optional['Antrag']] = relationship('Antrag', back_populates='kommentar')
