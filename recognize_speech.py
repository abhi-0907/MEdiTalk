# recognize_speech.py
import speech_recognition as sr

def recognize_speech(user_lang):
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
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
    
    if user_lang == 'en':
        text = r.recognize_google(audio)
    else:
        text = r.recognize_google(audio, language=lang)

    return text