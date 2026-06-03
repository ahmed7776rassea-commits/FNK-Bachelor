from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import json

from app.database import get_db
from app.models import (
    Antrag, AntragEins, AntragZweiA, AntragZweiB, AntragDreiA, AntragDreiB,
    Datei, Kommentar, Benutzer
)

router = APIRouter(prefix="/verlauf", tags=["Verlauf"])


def _user_meta(u: Benutzer | None):
    if not u:
        return None
    return {"name": u.Name, "nachname": u.Nachname, "email": u.Email}


def _parse_json_maybe(value):
    if value is None:
        return None
    if isinstance(value, (dict, list)):
        return value
    if isinstance(value, str):
        try:
            return json.loads(value)
        except Exception:
            return value
    return value


def _antrag_detail_payload(db: Session, antrag: Antrag) -> Dict[str, Any]:
    typ = antrag.Antrag_typ
    data: Dict[str, Any] = {}
    if typ == 1:
        r = (
            db.query(AntragEins)
            .filter(AntragEins.antrag_Antrag_id == antrag.Antrag_id)
            .first()
        )
        if r:
            data = {
                "titel": r.Titel_des_Vorhabens,
                "fachbereich": r.Fachbereich,
                "beginn": r.Beginn,
                "ende": r.Ende,
                "drittmittelgeber": r.Drittmittelgeber,
                "gesamtmittel": r.Drittmittel_gesamt_HTW,
                "zugeordnet": r.Drittmittel_zugeordnet,
                "verfuegbar": r.Drittmittel_verfuegbar,
                "eingesetzt": r.Drittmittel_eingesetzt_semester,
                "nebentaetigkeit": r.Einnahmen_nebentaetigkeit,
            }
    elif typ == 2:
        r = (
            db.query(AntragZweiA)
            .filter(AntragZweiA.antrag_Antrag_id == antrag.Antrag_id)
            .first()
        )
        if r:
            data = {
                "titel_veroeffentlichung": r.Titel_veroeffentlichung,
                "fachbereich": r.Fachbereich,
                "bibliographische_angaben": r.Bibliographische_angaben,
                "erscheinungsdatum": r.Erscheinungsdatum,
                "alleinautor": r.Alleinautor,
                "koautor": r.Koautor,
                "peer_review": r.Peer_Review,
                "drittbegutachtung": r.Drittbegutachtung,
                "einnahmen_nebentaetigkeit": r.Einnahmen_nebentaetigkeit,
            }
    elif typ == 3:
        r = (
            db.query(AntragZweiB)
            .filter(AntragZweiB.antrag_Antrag_id == antrag.Antrag_id)
            .first()
        )
        if r:
            data = {
                "titel_praesentation": r.Titel_praesentation,
                "fachbereich": r.Fachbereich,
                "erscheinungsdatum": r.Erscheinungsdatum,
                "beteiligung": r.Beteiligung,
                "format_a": r.Format_A,
                "format_b": r.Format_B,
                "format_c": r.Format_C,
                "zusatz_optionen": _parse_json_maybe(r.Zusatz_optionen),
                "einnahmen_nebentaetigkeit": r.Einnahmen_nebentaetigkeit,
            }

    elif typ == 4:
        r = (
            db.query(AntragDreiA)
            .filter(AntragDreiA.antrag_Antrag_id == antrag.Antrag_id)
            .first()
        )
        if r:
            data = {
                "antragsteller_name": r.Antragsteller_name,
                "beteiligte_universitaet": r.Beteiligte_Universitaet,
                "promovend_name": r.Promovend_name,
                "arbeitstitel": r.Arbeitstitel,
                "beginn_betreuung": r.Beginn_Betreuung,
                "zeitraum_von": r.Zeitraum_von,
                "zeitraum_bis": r.Zeitraum_bis,
            }

    elif typ == 5:
        r = (
            db.query(AntragDreiB)
            .filter(AntragDreiB.antrag_Antrag_id == antrag.Antrag_id)
            .first()
        )
        if r:
            data = {
                "antragsteller_name": r.Antragsteller_name,
                "beteiligte_universitaet": r.Beteiligte_Universitaet,
                "promovend_name": r.Promovend_name,
                "titel_dissertation": r.Titel_Dissertation,
                "datum_disp": r.Datum_Disp,
                "zeitraum_von": r.Zeitraum_von,
                "zeitraum_bis": r.Zeitraum_bis,
                "einnahmen_nebentaetigkeit": r.Einnahmen_nebentaetigkeit,
            }

    
    files = db.query(Datei).filter(Datei.Antrag_id == antrag.Antrag_id).all()
    files_out = [
        {"id": f.Id, "pfad": f.Dateipfad, "name": getattr(f, "Name", None)} for f in files
    ]


    comments = (
        db.query(Kommentar)
        .filter(Kommentar.Antrag_id == antrag.Antrag_id)
        .order_by(Kommentar.Zeitpunkt)
        .all()
    )
    comments_out = [
        {"id": k.Kommentar_id, "text": k.Text_, "zeit": k.Zeitpunkt, "pruefer_name": None}
        for k in comments
    ]

    return {
        "meta": {
            "antrag_id": antrag.Antrag_id,
            "typ": antrag.Antrag_typ,
            "antrag_typ": antrag.Antrag_typ,
            "status_eins": antrag.Status_eins,
            "status_zwei": antrag.Status_zwei,
            "pruefer_eins": antrag.Pruefer_eins,
            "pruefer_zwei": antrag.Pruefer_zwei,
            "erstellungsdatum": getattr(antrag, "Erstellungsdatum", None),
            "benutzer": _user_meta(antrag.Benutzer_),
            "punkte": float(antrag.Punkte or 0.0),
        },
        "data": data,
        "files": files_out,
        "kommentare": comments_out,
    }


@router.get("/me/{benutzer_id}")
def my_antraege(benutzer_id: int, db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    rows = (
        db.query(Antrag)
        .filter(Antrag.Benutzer_id == benutzer_id)
        .order_by(getattr(Antrag, "Erstellungsdatum", Antrag.Antrag_id).desc())
        .all()
    )
    out = []
    for a in rows:
        last_comment = (
            db.query(Kommentar)
            .filter(Kommentar.Antrag_id == a.Antrag_id)
            .order_by(Kommentar.Zeitpunkt.desc())
            .first()
        )
        out.append(
            {
                "Antrag_id": a.Antrag_id,
                "Antrag_typ": a.Antrag_typ,
                "Status_eins": a.Status_eins,
                "Status_zwei": a.Status_zwei,
                "Punkte": float(a.Punkte or 0.0),
                "Erstellungsdatum": getattr(a, "Erstellungsdatum", None),
                "Letzter_Kommentar": {
                    "text": (last_comment.Text_ if last_comment else None),
                    "zeit": (last_comment.Zeitpunkt if last_comment else None),
                },
            }
        )
    return out


@router.get("/me/{benutzer_id}/antrag/{antrag_id}")
def my_antrag_detail(benutzer_id: int, antrag_id: int, db: Session = Depends(get_db)) -> Dict[str, Any]:
    a = db.query(Antrag).filter(Antrag.Antrag_id == antrag_id).first()
    if not a:
        raise HTTPException(404, "Antrag nicht gefunden")
    if a.Benutzer_id != benutzer_id:
        raise HTTPException(403, "Nicht erlaubt")
    return _antrag_detail_payload(db, a)
