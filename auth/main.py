from fastapi import FastAPI

app = FastAPI(title="Auth service")

@app.get("/health")
def health():
    return {"service": "auth", "status": "ok"}

