from deep_translator import GoogleTranslator

def translate(text, user_lang):
    language_codes = {
    "English": "en",
    "Hindi": "hi",
    "Bengali": "bn",
    "Spanish": "es",
    "Chinese (Simplified)": "zh-CN",
    "Russian": "ru",
    "Japanese": "ja",
    "Korean": "ko",
    "German": "de",
    "French": "fr",
    "Tamil": "ta",
    "Telugu": "te",
    "Kannada": "kn",
    "Gujarati": "gu",
    "Punjabi": "pa"
    }
    lang = language_codes[user_lang]
    if lang != 'en':
        return GoogleTranslator(source='auto', target=lang).translate(text)
    else:
        return text


