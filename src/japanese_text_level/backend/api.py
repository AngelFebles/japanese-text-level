from fastapi import FastAPI
from pydantic import BaseModel

from japanese_text_level.systems.wk import analyze_text


class Input_Text(BaseModel):
    text: str


# 日本語を大好き

app = FastAPI()


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}


@app.post("/wanikani/")
async def get_wanikani_level(raw_text: Input_Text):

    kanji_levels, vocab_levels = analyze_text(raw_text.text)

    return {
        "kanji": kanji_levels,
        "vocab": vocab_levels,
    }
