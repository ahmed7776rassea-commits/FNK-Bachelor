from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from datetime import date
from decimal import Decimal
from typing import List
import os
import shutil
from uuid import uuid4

router = APIRouter(prefix="/drittmittel", tags=["Drittmittel"])

UPLOAD_DIR = "uploads"


def _punkte_antrag1(eingesetzt: int) -> int:
    if eingesetzt >= 50000: return 5
    if eingesetzt >= 40000: return 4
    if eingesetzt >= 30000: return 3
    if eingesetzt >= 20000: return 2
    if eingesetzt >= 10000: return 1
    return 0


@router.post("/antrag")
def create_drittmittel_antrag(
    Benutzer_id: int = Form(...),
    name: str = Form(...),
    fachbereich: str = Form(...),
    titel: str = Form(...),
    von: date = Form(...),
    bis: date = Form(...),
    mittelgeber: str = Form(...),
    gesamt_htw: int = Form(...),
    zugeordnet_antragsteller: int = Form(...),
    verfuegbar_zum_antragszeitpunkt: int = Form(...),
    eingesetzt_im_semester: int = Form(...),
    nebentaetigkeit: bool = Form(False),
    zulage: bool = Form(False),
    nachweise: List[UploadFile] = File(...),  
    db: Session = Depends(get_db),
):
   
    for f in nachweise:
        if f.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="Nur PDF-Dateien sind erlaubt.")

    punkte_int = _punkte_antrag1(eingesetzt_im_semester)
    punkte = Decimal(str(punkte_int))

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    
    antrag = models.Antrag(
        Benutzer_id=Benutzer_id,
        Antrag_typ=1,
        Status_eins="Offen",
        Status_zwei="",
        Pruefer_eins="",
        Pruefer_zwei="",
        Punkte=punkte,
    )
    db.add(antrag)
    db.commit()
    db.refresh(antrag)

    
    antrag1 = models.AntragEins(
        antrag_Antrag_id=antrag.Antrag_id,
        Antragsteller_name=name,
        Fachbereich=fachbereich,
        Ermaessigung_SWS=Decimal("0.0"),
        Titel_des_Vorhabens=titel,
        Beginn=von,
        Ende=bis,
        Drittmittelgeber=mittelgeber,
        Drittmittel_gesamt_HTW=Decimal(str(gesamt_htw)),
        Drittmittel_zugeordnet=Decimal(str(zugeordnet_antragsteller)),
        Drittmittel_verfuegbar=Decimal(str(verfuegbar_zum_antragszeitpunkt)),
        Drittmittel_eingesetzt_semester=Decimal(str(eingesetzt_im_semester)),
        Einnahmen_nebentaetigkeit=1 if nebentaetigkeit else 0,
    )
    db.add(antrag1)
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
        "message": "Antrag erfolgreich gespeichert",
        "antrag_id": antrag.Antrag_id,
        "punkte": float(punkte),
        "anzahl_dateien": len(nachweise),
    }
