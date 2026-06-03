from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from datetime import datetime
import os
import shutil
from uuid import uuid4

router = APIRouter(prefix="/drittmittel", tags=["Drittmittel"])

UPLOAD_DIR = "uploads"

@router.post("/antrag")
def create_drittmittel_antrag(
    name: str = Form(...),
    fachbereich: str = Form(...),
    titel: str = Form(...),
    von: datetime = Form(...),
    bis: datetime = Form(...),
    mittelgeber: str = Form(...),
    gesamtmittel: int = Form(...),
    zugewiesen: int = Form(...),
    verfuegbar: int = Form(...),
    eingesetzt: int = Form(...),
    nebentaetigkeit: bool = Form(...),
    zulage: bool = Form(...),
    datum: datetime = Form(...),
    nachweis: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # 💾 Speicher die Datei
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    dateiname = f"{uuid4()}_{nachweis.filename}"
    dateipfad = os.path.join(UPLOAD_DIR, dateiname)

    with open(dateipfad, "wb") as buffer:
        shutil.copyfileobj(nachweis.file, buffer)

    # ✅ Erstelle Antrag
    antrag = models.Antrag(
        Antrag_typ=1,
        Status="Offen",
        Erstellungsdatum=datetime.utcnow(),
        fachbereich=fachbereich,
        titel=titel,
        von=von,
        bis=bis,
        mittelgeber=mittelgeber,
        gesamtmittel=gesamtmittel,
        zugewiesen=zugewiesen,
        verfuegbar=verfuegbar,
        eingesetzt=eingesetzt,
        datum=datum,
        projektThema=titel,
        zusammenfassung="",
        Benutzer_id=1  # ⚠️ später dynamisch setzen (z.B. aus Session oder JWT)
    )
    db.add(antrag)
    db.commit()
    db.refresh(antrag)

    # ✅ Datei speichern
    neue_datei = models.Datei(
        Antrag_id=antrag.Antrag_id,
        Dateipfad=dateipfad
    )
    db.add(neue_datei)
    db.commit()

    return {"message": "Antrag erfolgreich gespeichert", "antrag_id": antrag.Antrag_id}
