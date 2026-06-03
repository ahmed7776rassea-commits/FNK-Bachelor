from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from datetime import datetime
from uuid import uuid4
from typing import List
import os, shutil, json

router = APIRouter(prefix="/praesentation", tags=["Antrag 2b Präsentation/Publikation"])
UPLOAD_DIR = "uploads"

def _punkte_antrag_2b(
    beteiligung: str,
    format_: str,
    a_option: str,
    a_katalog: bool,
    b_option: str,
    b_katalog: bool
) -> float:
    beteiligung_pts = 2 if beteiligung == "allein" else 1 if beteiligung == "zusammen" else 2 if beteiligung == "direction" else 0
    format_pts = 0.0
    if format_ == "A":
        if a_option == "ausserhalb_gt3":
            format_pts = 2.0
        elif a_option in ("htw_gt3", "ausserhalb_leq3"):
            format_pts = 1.0
        if a_katalog:
            format_pts += 0.5
    elif format_ == "B":
        if b_option == "wettbewerb":
            format_pts = 2.0
        elif b_option == "einladung":
            format_pts = 1.0
        if b_katalog:
            format_pts += 0.5
    elif format_ == "C":
        format_pts = 0.5
    total = beteiligung_pts + format_pts
    return min(4.5, total)

@router.post("/antrag")
def create_antrag_zwei_b(
    Benutzer_id: int = Form(...),
    Antragsteller_name: str = Form(...),
    Fachbereich: str = Form(...),
    Titel_praesentation: str = Form(...),
    Erscheinungsdatum: datetime = Form(...),
    Beteiligung: str = Form(...),
    Format: str = Form(...),
    A_Option: str = Form(""),
    A_Katalog: bool = Form(False),
    B_Option: str = Form(""),
    B_Katalog: bool = Form(False),
    Einnahmen_nebentaetigkeit: bool = Form(...),
    nachweise: List[UploadFile] = File(...),  
    db: Session = Depends(get_db)
):
    for f in nachweise:
        if f.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="Nur PDF-Dateien sind erlaubt.")
    punkte = _punkte_antrag_2b(
        beteiligung=Beteiligung,
        format_=Format,
        a_option=A_Option,
        a_katalog=A_Katalog,
        b_option=B_Option,
        b_katalog=B_Katalog
    )

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    antrag = models.Antrag(
        Benutzer_id=Benutzer_id,
        Antrag_typ=3,
        Status_eins="Offen",
        Status_zwei="",
        Pruefer_eins="",
        Pruefer_zwei="",
        Punkte=punkte
    )
    db.add(antrag)
    db.commit()
    db.refresh(antrag)
    zusatz = {
        "Format": Format,
        "A_Option": A_Option,
        "A_Katalog": bool(A_Katalog),
        "B_Option": B_Option,
        "B_Katalog": bool(B_Katalog)
    }
    antrag2b = models.AntragZweiB(
        antrag_Antrag_id=antrag.Antrag_id,
        Antragsteller_name=Antragsteller_name,
        Fachbereich=Fachbereich,
        Titel_praesentation=Titel_praesentation,
        Erscheinungsdatum=Erscheinungsdatum.date() if isinstance(Erscheinungsdatum, datetime) else Erscheinungsdatum,
        Beteiligung=Beteiligung,
        Format_A=1 if Format == "A" else 0,
        Format_B=1 if Format == "B" else 0,
        Format_C=1 if Format == "C" else 0,
        Zusatz_optionen=json.dumps(zusatz, ensure_ascii=False),
        Einnahmen_nebentaetigkeit=int(bool(Einnahmen_nebentaetigkeit))
    )
    db.add(antrag2b)
    db.commit()
    for f in nachweise:
        filename = f"{uuid4()}_{f.filename}"
        filepath = os.path.join(UPLOAD_DIR, filename)
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(f.file, buffer)

        file_url = f"/uploads/{filename}"
        datei = models.Datei(
            Antrag_id=antrag.Antrag_id,
            Dateipfad=file_url,
            Name=f.filename
        )
        db.add(datei)

    db.commit()

    return {
        "message": "Antrag 2b erfolgreich eingereicht",
        "antrag_id": antrag.Antrag_id,
        "punkte": float(punkte),
        "anzahl_dateien": len(nachweise)
    }
