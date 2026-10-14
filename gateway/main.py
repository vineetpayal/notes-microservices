from fastapi import FastAPI

app = FastAPI(title="gateway service")

@app.get("/health")
def health():
    return {"service": "gateway", "status": "ok"}