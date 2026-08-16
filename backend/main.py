from fastapi import FastAPI

app = FastAPI(title="DocuAgent API")

@app.get("/health")
def health_check():
    return {"status": "ok"}