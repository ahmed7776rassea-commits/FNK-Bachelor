from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from datetime import datetime
from typing import List
import os, shutil
from uuid import uuid4

router = APIRouter(prefix="/veroeffentlichung", tags=["Antrag 2a  Veröffentlichung"])
UPLOAD_DIR = "uploads"

@router.post("/antrag")
def create_antrag_zwei_a(
    Benutzer_id: int = Form(...),
    Antragsteller_name: str = Form(...),
    Fachbereich: str = Form(...),
    Ermaessigung_SWS: float = Form(...),
    Titel_veroeffentlichung: str = Form(...),
    Alleinautor: bool = Form(...),
    Koautor: bool = Form(...),
    Bibliographische_angaben: str = Form(...),
    Erscheinungsdatum: datetime = Form(...),
    Peer_Review: bool = Form(...),
    Drittbegutachtung: bool = Form(...),
    Einnahmen_nebentaetigkeit: bool = Form(...),
    nachweise: List[UploadFile] = File(...),   
    db: Session = Depends(get_db)
):
    
    for f in nachweise:
        if f.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="Nur PDF-Dateien sind erlaubt.")

    
    autor = 2.0 if Alleinautor else 1.0 if Koautor else 0.0
    begut = 2.0 if Peer_Review else 0.5 if Drittbegutachtung else 0.0
    punkte = min(4.0, autor + begut)

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    antrag = models.Antrag(
        Benutzer_id=Benutzer_id,
        Antrag_typ=2,
        Status_eins="Offen",
        Status_zwei="",
        Pruefer_eins="",
        Pruefer_zwei="",
        Punkte=punkte,
    )
    db.add(antrag)
    db.commit()
    db.refresh(antrag)
    antrag2a = models.AntragZweiA(
        antrag_Antrag_id=antrag.Antrag_id,
        Antragsteller_name=Antragsteller_name,
        Fachbereich=Fachbereich,
        Ermaessigung_SWS=Ermaessigung_SWS,
        Titel_veroeffentlichung=Titel_veroeffentlichung,
        Alleinautor=int(Alleinautor),
        Koautor=int(Koautor),
        Bibliographische_angaben=Bibliographische_angaben,
        Erscheinungsdatum=Erscheinungsdatum,
        Peer_Review=int(Peer_Review),
        Drittbegutachtung=int(Drittbegutachtung),
        Einnahmen_nebentaetigkeit=int(Einnahmen_nebentaetigkeit)
    )
    db.add(antrag2a)
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
        "message": "Antrag 2a erfolgreich eingereicht",
        "antrag_id": antrag.Antrag_id,
        "punkte": float(punkte),
        "anzahl_dateien": len(nachweise),
    }
