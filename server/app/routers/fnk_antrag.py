from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import (
    Antrag, AntragEins, AntragZweiA, AntragZweiB, AntragDreiA, AntragDreiB,
    Datei, Kommentar, Benutzer
)
from datetime import datetime
from typing import Optional
import json

router = APIRouter(prefix="/fnk", tags=["FnK"])

def user_meta(u: Benutzer | None):
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


@router.get("/antraege")
def alle_antraege(db: Session = Depends(get_db)):
    rows = db.query(Antrag).order_by(Antrag.Antrag_id.desc()).all()
    out = []
    for a in rows:
        if a.Status_zwei:
            review_by = a.Pruefer_zwei
            review_status = a.Status_zwei
        elif a.Status_eins:
            review_by = a.Pruefer_eins
            review_status = a.Status_eins
        else:
            review_by = None
            review_status = "Offen"

        out.append({
            "antrag_id": a.Antrag_id,
            "antrag_typ": a.Antrag_typ,
            "status_eins": a.Status_eins,
            "status_zwei": a.Status_zwei,
            "pruefer_eins": a.Pruefer_eins,
            "pruefer_zwei": a.Pruefer_zwei,
            "review_by": review_by,
            "review_status": review_status,
            "review_line": (
                f"Bereits geprüft von: {review_by} — Status: {review_status}"
                if review_by else f"Status: {review_status}"
            ),
            "erstellungsdatum": getattr(a, "Erstellungsdatum", None),
            "benutzer": user_meta(a.Benutzer_),
        })
    return out


@router.get("/antrag/{id}")
def get_antrag_detail(id: int, db: Session = Depends(get_db)):
    a: Antrag = db.query(Antrag).filter(Antrag.Antrag_id == id).first()
    if not a:
        raise HTTPException(404, "Antrag nicht gefunden")

    typ = a.Antrag_typ
    data = {}

    if typ == 1:
        r = db.query(AntragEins).filter(AntragEins.antrag_Antrag_id == id).first()
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
        r = db.query(AntragZweiA).filter(AntragZweiA.antrag_Antrag_id == id).first()
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
        r = db.query(AntragZweiB).filter(AntragZweiB.antrag_Antrag_id == id).first()
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
        r = db.query(AntragDreiA).filter(AntragDreiA.antrag_Antrag_id == id).first()
        if r:
            data = {
               "beteiligte_universitaet": r.Beteiligte_Universitaet,
               "promovend_name": r.Promovend_name,
               "arbeitstitel": r.Arbeitstitel,
               "beginn_betreuung": r.Beginn_Betreuung,
               "zeitraum_von": r.Zeitraum_von,
               "zeitraum_bis": r.Zeitraum_bis,
            }
    elif typ == 5:
        r = db.query(AntragDreiB).filter(AntragDreiB.antrag_Antrag_id == id).first()
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

    files = db.query(Datei).filter(Datei.Antrag_id == id).all()
    files_out = [{"id": f.Id, "pfad": f.Dateipfad, "name": getattr(f, "Name", None)} for f in files]

    comments = db.query(Kommentar).filter(Kommentar.Antrag_id == id).order_by(Kommentar.Zeitpunkt).all()
    comments_out = [{"id": k.Kommentar_id, "text": k.Text_, "zeit": k.Zeitpunkt}for k in comments]

    return {
        "meta": {
            "antrag_id": a.Antrag_id,
            "antrag_typ": typ,
            "typ": typ,
            "status_eins": a.Status_eins,
            "status_zwei": a.Status_zwei,
            "pruefer_eins": a.Pruefer_eins,
            "pruefer_zwei": a.Pruefer_zwei,
            "erstellungsdatum": getattr(a, "Erstellungsdatum", None),
            "benutzer": user_meta(a.Benutzer_),
            "punkte": float(getattr(a, "Punkte", 0) or 0.0),
        },
        "data": data,
        "files": files_out,
        "kommentare": comments_out
    }


@router.post("/antrag/{id}/kommentar")
def kommentar_hinzufuegen(
    id: int,
    kommentar: str = Form(""),
    status_eins: Optional[str] = Form(None),
    status_zwei: Optional[str] = Form(None),
    pruefer_name: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    a = db.query(Antrag).filter(Antrag.Antrag_id == id).first()
    if not a:
        raise HTTPException(404, "Antrag nicht gefunden")

    if a.Pruefer_eins and a.Pruefer_zwei:
        raise HTTPException(400, "Dieser Antrag wurde bereits final geprüft.")

    pn = (pruefer_name or "").strip()

    # Phase 1
    if not a.Pruefer_eins:
        if pn:
            a.Pruefer_eins = pn[:45]
        if status_eins is not None:
            a.Status_eins = status_eins

    # Phase 2
    else:
        if pn and a.Pruefer_eins and pn.strip() == (a.Pruefer_eins or "").strip():
            raise HTTPException(400, "Der zweite Status darf nicht vom gleichen Prüfer gesetzt werden.")
        if pn:
            a.Pruefer_zwei = pn[:45]
        if status_zwei is not None:
            a.Status_zwei = status_zwei

    db.add(a)

    if kommentar and kommentar.strip():
        db.add(Kommentar(
            Antrag_id=id,
            Text_=kommentar,
            Zeitpunkt=datetime.utcnow()
        ))

    db.commit()
    return {"ok": True}