from fastapi import FastAPI

app = FastAPI(title="Ask service")

@app.get("/health")
def health():
    return {"service": "ask", "status": "ok"}