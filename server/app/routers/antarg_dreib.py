from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from datetime import date
import os
import shutil
from uuid import uuid4

router = APIRouter(prefix="/fnk", tags=["Antrag 3b Abschluss Promotion"])

UPLOAD_DIR = "uploads"

@router.post("/abschluss")
def create_antrag_drei_b(
    Benutzer_id: int = Form(...),
    Antragsteller_name: str = Form(...),
    Beteiligte_Universitaet: str = Form(...),
    Promovend_name: str = Form(...),
    Titel_Dissertation: str = Form(...),
    Datum_Disp: date = Form(...),
    Zeitraum_von: date = Form(...),
    Zeitraum_bis: date = Form(...),
    Einnahmen_nebentaetigkeit: bool = Form(...),
    nachweis: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    
    if nachweis.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Nur PDF-Dateien sind erlaubt.")

    
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    filename = f"{uuid4()}_{nachweis.filename}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(nachweis.file, buffer)
    antrag = models.Antrag(
        Benutzer_id=Benutzer_id,
        Antrag_typ=5,            
        Status_eins="Offen",
        Status_zwei="",
        Pruefer_eins="",
        Pruefer_zwei=""
    )
    db.add(antrag)
    db.commit()
    db.refresh(antrag)

    antrag3b = models.AntragDreiB(
        antrag_Antrag_id=antrag.Antrag_id,
        Antragsteller_name=Antragsteller_name,
        Beteiligte_Universitaet=Beteiligte_Universitaet,
        Promovend_name=Promovend_name,
        Titel_Dissertation=Titel_Dissertation,
        Datum_Disp=Datum_Disp,
        Zeitraum_von=Zeitraum_von,
        Zeitraum_bis=Zeitraum_bis,
        Einnahmen_nebentaetigkeit=int(bool(Einnahmen_nebentaetigkeit))
    )
    db.add(antrag3b)
    file_url = f"/uploads/{filename}"
    datei = models.Datei(
        Antrag_id=antrag.Antrag_id,
        Dateipfad=file_url,
        Name=nachweis.filename
    )
    db.add(datei)

    db.commit()

    return {
        "message": "Antrag 3b (Abschluss Promotion) erfolgreich eingereicht",
        "antrag_id": antrag.Antrag_id,
        "file_url": file_url
    }
