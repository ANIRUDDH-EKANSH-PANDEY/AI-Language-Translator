from backend import translate_text, TranslationRequest

def test_translation():
    request = TranslationRequest(text="Hello", target_language="fr")
    response = translate_text(request)
    assert "Bonjour" in response["translated_text"]

# Run test using: pytest test_api.py