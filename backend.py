from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from deep_translator import GoogleTranslator
import docx

app = FastAPI()

class TranslationRequest(BaseModel):
    text: str
    target_language: str

@app.post("/translate")
def translate_text(request: TranslationRequest):
    translated_text = GoogleTranslator(source='auto', target=request.target_language).translate(request.text)
    return {"translated_text": translated_text}

@app.post("/translate-file")
async def translate_file(file: UploadFile = File(...), target_language: str = Form(...)):
    content = await file.read()

    # Extract text based on file type
    if file.filename.endswith(".txt"):
        text = content.decode("utf-8")
    elif file.filename.endswith(".docx"):
        doc = docx.Document(file.file)
        text = "\n".join([para.text for para in doc.paragraphs])
    else:
        return {"error": "Unsupported file format. Please upload a TXT, PDF, or DOCX file."}

    # Translate text
    translated_text = GoogleTranslator(source='auto', target=target_language).translate(text)

    return {"translated_text": translated_text}