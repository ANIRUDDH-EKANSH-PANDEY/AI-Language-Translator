from fastapi import FastAPI
from pydantic import BaseModel
from googletrans import Translator

app = FastAPI()
translator = Translator()

class TranslationRequest(BaseModel):
    text: str
    target_language: str

@app.post("/translate")
def translate_text(request: TranslationRequest):
    translated_text = translator.translate(request.text, dest=request.target_language).text
    return {"translated_text": translated_text}

# Run the API: uvicorn backend:app --reload