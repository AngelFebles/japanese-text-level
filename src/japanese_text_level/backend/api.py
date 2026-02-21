from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from japanese_text_level.systems.wk import analyze_text


class InputText(BaseModel):
    input: str


# 日本語を大好き

app = FastAPI()

app.add_middleware(
    CORSMiddleware,  # type: ignore[arg-type]
    allow_origins=["http://localhost:5173"],  # React port
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.get("/")
# async def root():
#     return {"message": "Hello World"}


@app.post("/wanikani/")
async def get_wanikani_level(raw_text: InputText):

    kanji_levels, vocab_levels = analyze_text(raw_text.input)

    return {
        "kanji": kanji_levels,
        "vocab": vocab_levels,
    }
