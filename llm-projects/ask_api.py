from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Kundan's LLM API", version="0.1")


class AskRequest(BaseModel):
    question: str
    temperature: float = 0.7


class AskResponse(BaseModel):
    question: str
    answer: str
    model: str


@app.get("/")
def home():
    return {"status": "online", "message": "LLM API ready"}


@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    fake_answer = (
        f"(placeholder) Tumne poocha:'{req.question}'. Day 5 mein mai asli jawab dunga!"
    )
    return AskResponse(
        question=req.question,
        answer=fake_answer,
        model="placeholder-v0",
    )
