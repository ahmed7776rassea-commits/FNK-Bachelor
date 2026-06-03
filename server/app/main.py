from fastapi import FastAPI
from app.database import engine
from app import models  
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
import os
from sqlalchemy import text
from app.routers import auth
from app.routers import fnk_antrag
from app.routers import antrag_eins,antrag_zwei_a, antrag_zwei_b, antrag_drei_a, antarg_dreib
from app.routers import home_verlauf



load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

app = FastAPI()
app.include_router(home_verlauf.router)
from app.database import SessionLocal

@app.on_event("startup")
def test_db():
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
      #  print(" Verbindung zur MySQL-Datenbank erfolgreich!") I have tested , whether my connection is established or not
    except Exception as e:
        print(" Fehler bei der Verbindung zur DB:", str(e))


app.include_router(auth.router)
app.include_router(fnk_antrag.router)
app.include_router(antrag_eins.router)
app.include_router(antrag_zwei_a.router)
app.include_router(antrag_zwei_b.router)
app.include_router(antrag_drei_a.router)
app.include_router(antarg_dreib.router)

if not os.path.exists("uploads"):
    os.makedirs("uploads")

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

models.Base.metadata.create_all(bind=engine)  
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def start():
    return {"message": "FastAPI verbunden mit MySQL erfolgreich!"}
