from fastapi import FastAPI

app = FastAPI(title="notes service")

@app.get("/health")
def health():
    return {"service": "notes", "status": "ok"}