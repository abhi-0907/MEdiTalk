import json
import requests
import streamlit as st
from streamlit_lottie import st_lottie


# Import your custom modules
from text_to_text import translate
from Medi_talk import get_answer
from recognize_speech import recognize_speech
from play_text import play_text

# Constants
LOTTIE_URL = 'https://lottie.host/97b3731e-68ac-4429-83d0-d2b5fc3d145e/DpFQUzOmYL.json'

# Language codes
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

# Create the animation
def load_lottie(url):
    r = requests.get(url)
    if r.status_code != 200:
        return
    return r.json()

lottie_anim = load_lottie(LOTTIE_URL)

st.set_page_config(page_title="MEdiTalk - Medical Voice Bot", page_icon='', layout='centered')

# Initialize session state
if "is_recording" not in st.session_state:
    st.session_state.is_recording = False
if "prompt_text" not in st.session_state:
    st.session_state.prompt_text = None
if "chat_text" not in st.session_state:
    st.session_state.chat_text = None
if "user_lang" not in st.session_state:
    st.session_state.user_lang = "en"  # Default language is English

# Define button callbacks
def callback_record():
    st.session_state.is_recording = True
    prompt_box.write("Recording started ...")

    # Record prompt
    prompt_text = recognize_speech(st.session_state.user_lang)
    st.session_state.prompt_text = prompt_text

    st.session_state.is_recording = False

    response = get_answer(prompt_text)
    json.dump(response, open('response.json', 'wt'))

    st.session_state.chat_text = response

##################
with st.container():
    left, right = st.columns([2, 3])
    with left:
        st_lottie(lottie_anim, height=300, key='coding')

    with right:
        st.subheader('Hi, I am MediTalk - Medical Voice Assistant!')

        # Language selection button
        st.sidebar.subheader("Select User Language")
        st.session_state.user_lang = st.sidebar.selectbox("Choose Language", list(language_codes.keys()))

        st.write('Press, Record to start recording your prompt')

        rec_button = st.button(
            label="Record :microphone:", type='primary',
            on_click=callback_record,
            disabled=st.session_state.is_recording)

        prompt_box = st.empty()
        if st.session_state.prompt_text:
            prompt_box.write(f'Prompt: {st.session_state.prompt_text}')

##########################
with st.container():
    st.write('---')

    message_box = st.empty()
    if st.session_state.chat_text:
        lines = st.session_state.chat_text

        for line in lines.split('.'):
            message_box.write(line)
            play_text(line, st.session_state.user_lang)
        
        message_box.write(lines)
            
