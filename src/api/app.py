from fastapi import FastAPI
from pydantic import BaseModel
from src.assistant import ask
from src.core.database import init_db

app = FastAPI(title="search-files API", version="0.2.0")

class QueryIn(BaseModel):
    q: str

@app.on_event("startup")
def startup():
    init_db()

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/search")
def search(payload: QueryIn):
    return {"result": ask(payload.q)}