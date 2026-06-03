from fastapi import APIRouter, HTTPException, Form, Depends
from sqlalchemy.orm import Session
from ldap3 import Server, Connection, SIMPLE, SUBTREE
from app.database import SessionLocal
from app import models

router = APIRouter(prefix="/auth", tags=["Authentifizierung"])

LDAP_SERVER = "login-dc-01.login.htw-berlin.de"
LDAP_DOMAIN = "Login"
SEARCH_BASE = "dc=login,dc=htw-berlin,dc=de"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login")
def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user_dn = f"{LDAP_DOMAIN}\\{username}"
    try:
        server = Server(LDAP_SERVER, use_ssl=True)
        conn = Connection(server, user=user_dn, password=password, authentication=SIMPLE, auto_bind=True)

        search_filter = f"(sAMAccountName={username})"
        conn.search(SEARCH_BASE, search_filter, SUBTREE, attributes=["givenName","sn","mail", ])
        if not conn.entries:
            raise HTTPException(status_code=401, detail="Benutzer nicht gefunden")

        entry = conn.entries[0]
        vorname = entry.givenName.value or ""
        nachname = entry.sn.value or ""
        email = entry.mail.value or f"{username}@htw-berlin.de"
        db_user = db.query(models.Benutzer).filter(models.Benutzer.Email == email).first()
        if db_user:
         rolle = db_user.Rolle
        else:
         rolle = entry.title.value or "Antragsteller"
        if not db_user:
            db_user = models.Benutzer(
                Name=vorname,
                Nachname=nachname,
                Email=email,
                Rolle=rolle
            )
            db.add(db_user)
            db.commit()
            db.refresh(db_user)

        conn.unbind()

        return {
            "message": "Login erfolgreich",
            "benutzer_id": db_user.Benutzer_id,
            "name": vorname,
            "nachname": nachname,
            "email": email,
            "rolle": rolle,     
        }

    except Exception as e:
      print("Fehler beim Login:", str(e))
      raise HTTPException(detail=f"Fehler beim Login: {str(e)}")


