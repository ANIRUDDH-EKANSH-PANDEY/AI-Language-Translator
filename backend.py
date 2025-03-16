from fastapi import FastAPI
from pydantic import BaseModel
from deep_translator import GoogleTranslator  # ✅ Correct import

app = FastAPI()

class TranslationRequest(BaseModel):
    text: str
    target_language: str

@app.post("/translate")
def translate_text(request: TranslationRequest):
    try:
        # ✅ Correct usage of deep-translator
        translated_text = GoogleTranslator(source="auto", target=request.target_language).translate(request.text)
        return {"translated_text": translated_text}
    except Exception as e:
        return {"error": str(e)}

# Run the API: uvicorn backend:app --reload