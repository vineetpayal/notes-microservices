from fastapi import FastAPI, HTTPException
from pwdlib import PasswordHash
from sqlmodel import SQLModel, Field, Session, create_engine, select

password_hash = PasswordHash.recommended()

class User(SQLModel, table=True):
    user_id : int | None = Field(default = None, primary_key=True)
    username : str = Field(unique=True, index = True)
    password_hash : str
    
class Credentials(SQLModel):
    username : str
    password : str = Field(min_length=8)
    
engine = create_engine("sqlite:///auth.db")
SQLModel.metadata.create_all(engine)     
    

app = FastAPI(title="Auth service")

@app.get("/health")
def health():
    return {"service": "auth", "status": "ok"}

@app.post("/register", status_code=201)
def register(creds: Credentials):
    with Session(engine) as session:
        existing = session.exec(select(User).where(User.username == creds.username)).first()
        if existing:
            raise HTTPException(status_code=409, detail="username already taken")
        
        user = User(
            username=creds.username,
            password_hash= password_hash.hash(creds.password)
        )
        
        session.add(user)
        session.commit()
        session.refresh()
        return {"id": user.id, "username": user.username}
    
@app.post("/login")
def login(creds : Credentials):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.username == creds.username)).first()
        
        if user is None or not password_hash.verify(creds.password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid username or password")
        
        return {"message": "Login successfull"}
               
