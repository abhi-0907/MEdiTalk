import pygame
from gtts import gTTS
from io import BytesIO
import time

def play_text(text, user_lang):

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
    # Create a gTTS object
    if not text:
        return
    tts = gTTS(text=text, lang=lang, slow=False)
    # Use BytesIO to avoid saving the audio to a file
    audio_stream = BytesIO()
    tts.write_to_fp(audio_stream)
    audio_stream.seek(0)
    # Initialize pygame mixer
    pygame.mixer.init()
    # Load the audio stream
    pygame.mixer.music.load(audio_stream)
    # Play the audio
    pygame.mixer.music.play()
    # Wait for the audio to finish playing
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
    # Clean up
    pygame.mixer.quit()
