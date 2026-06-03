from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Question(BaseModel):
    text: str
    max_words: int = 50


@app.post("/echo")
def echo(payload: Question):
    return {"you_asked": payload.text, "max_words": payload.max_words}
