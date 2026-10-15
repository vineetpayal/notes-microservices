from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Field, Session, create_engine, select

class Note(SQLModel, table=True):
    id : int | None = Field(default=None, primary_key=True)
    title : str
    content : str
    

engine = create_engine("sqlite:///notes.db")
SQLModel.metadata.create_all(engine)    


app = FastAPI(title="notes service")

@app.get("/health")
def health():
    return {"service": "notes", "status": "ok"}

@app.post("/notes")
def create_note(note: Note):
    with Session(engine) as session:
        session.add(note)
        session.commit()
        session.refresh()
        return note
    
@app.get("/notes")
def list_notes():
    with Session(engine) as session:
        return session.exec(select(Note)).all()  
    
@app.get("/notes/{note_id}")
def get_note(id : int):
    with Session(engine) as session:
        note = session.get(Note, id)
        
        if note is None:
            raise HTTPException(status_code=404, detail="Note not found")
        
        return note
        
        