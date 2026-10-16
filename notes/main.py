from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import SQLModel, Field, Session, create_engine, select
import jwt

SECRET_KEY = "dev-secret-change-me"   # must match the auth service

class NoteIn(SQLModel):
    title : str
    content : str

class Note(NoteIn, table=True):
    id : int | None = Field(default=None, primary_key=True)
    owner : str = Field(index=True)
    

engine = create_engine("sqlite:///notes.db")
SQLModel.metadata.create_all(engine)    


app = FastAPI(title="notes service")
bearer = HTTPBearer()

def current_user(creds : HTTPAuthorizationCredentials = Depends(bearer)) ->str:
    try:
        payload = jwt.decode(
            creds.credentials, 
            SECRET_KEY, 
            algorithms=["HS256"]
        )
        
    except jwt.PyJWTError:
        raise HTTPException(status_code=401,  detail="Invalid or expired token")
    return payload["sub"]

@app.get("/health")
def health():
    return {"service": "notes", "status": "ok"}

@app.post("/notes")
def create_note(data: NoteIn, user : str = Depends(current_user)):
    note = Note(**data.model_dump(), owner = user)
    with Session(engine) as session:
        session.add(note)
        session.commit()
        session.refresh(note)
        return note
    
@app.get("/notes")
def list_notes(user : str = Depends(current_user)):
    with Session(engine) as session:
        return session.exec(select(Note).where(Note.owner == user)).all()  
    
@app.get("/notes/{note_id}")
def get_note(note_id : int, user : str = Depends(current_user)):
    with Session(engine) as session:
        note = session.get(Note, note_id)
        
        if note is None or note.owner != user:
            raise HTTPException(status_code=404, detail="Note not found")
        
        return note
        
        