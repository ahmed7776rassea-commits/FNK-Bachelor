from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from datetime import date
import os
import shutil
from uuid import uuid4

router = APIRouter(prefix="/promotionen", tags=["Antrag 3a promotionen"])

UPLOAD_DIR = "uploads"

@router.post("/antrag")
def create_antrag_drei_a(
    Benutzer_id: int = Form(...),
    Antragsteller_name: str = Form(...),
    Beteiligte_Universitaet: str = Form(...),
    Promovend_name: str = Form(...),
    Arbeitstitel: str = Form(...),
    Beginn_Betreuung: date = Form(...),
    Zeitraum_von: date = Form(...),
    Zeitraum_bis: date = Form(...),
    Einnahmen_nebentaetigkeit: bool = Form(...),
    nachweis: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    filename = f"{uuid4()}_{nachweis.filename}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(nachweis.file, buffer)

   
    antrag = models.Antrag(
        Benutzer_id=Benutzer_id,
        Antrag_typ=4,   # Typ 4 = Promotionen
        Status_eins="Offen",
        Status_zwei="",
        Pruefer_eins="",
        Pruefer_zwei=""
    )
    db.add(antrag)
    db.commit()
    db.refresh(antrag)

    antrag3a = models.AntragDreiA(
        antrag_Antrag_id=antrag.Antrag_id,
        Antragsteller_name=Antragsteller_name,
        Beteiligte_Universitaet=Beteiligte_Universitaet,
        Promovend_name=Promovend_name,
        Arbeitstitel=Arbeitstitel,
        Beginn_Betreuung=Beginn_Betreuung,
        Zeitraum_von=Zeitraum_von,
        Zeitraum_bis=Zeitraum_bis
    )
    db.add(antrag3a)

    file_url = f"/uploads/{filename}"
    datei = models.Datei(
        Antrag_id=antrag.Antrag_id,
        Dateipfad=file_url,
        Name=nachweis.filename  
    )
    db.add(datei)

    db.commit()

    return {
        "message": "Antrag 3a (Promotion) erfolgreich eingereicht",
        "file_url": file_url
    }
