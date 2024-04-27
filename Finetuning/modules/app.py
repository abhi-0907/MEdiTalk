import csv
import json
import requests
import streamlit as st
from streamlit_lottie import st_lottie

# Import your custom modules
from text_to_text import translate
from meditalk_finetuned import query_meditalk
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

# Function to save data to a CSV file
def save_to_csv(data, filename):
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)

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

      # Check if bot is responding
    if st.session_state.chat_text is not None:
        play_text("", st.session_state.user_lang)  # Stop the response playback if in progress
        
    # Record prompt
    prompt_text = recognize_speech(st.session_state.user_lang)
    tran_prompt_text = translate(prompt_text, "English")
    st.session_state.prompt_text = prompt_text
    st.session_state.is_recording = False

    response = query_meditalk(tran_prompt_text)
    json.dump(response, open('response.json', 'wt'))
    tran_response = translate(response, st.session_state.user_lang)
    st.session_state.chat_text = tran_response

    # Save data to CSV file
    data = [prompt_text, response]
    filename = f"{st.session_state.user_lang}_data.csv"
    save_to_csv(data, filename)

# Define language change callback
def callback_language_change():
    st.session_state.prompt_text = None
    st.session_state.chat_text = None

with st.container():
    left, right = st.columns([2, 3])
    with left:
        st_lottie(lottie_anim, height=300, key='coding')

    with right:
        st.subheader('Hi, I am MediTalk - Medical Voice Assistant!')

        # Language selection button
        st.sidebar.subheader("Select User Language")
        st.session_state.user_lang = st.sidebar.selectbox(
            "Choose Language", list(language_codes.keys()),
            on_change=callback_language_change
        )

        st.write('Press "Record" Button to start recording your prompt')

        rec_button = st.button(
            label="Record :microphone:", type='primary',
            on_click=callback_record,
            disabled=st.session_state.is_recording)

        prompt_box = st.empty()
        if st.session_state.prompt_text:
            prompt_box.write(f'Prompt: {st.session_state.prompt_text}')

with st.container():
    st.write('---')

    message_box = st.empty()
    if st.session_state.chat_text:
        lines = st.session_state.chat_text

        for line in lines.split('.'):
            message_box.write(line)
            play_text(line, st.session_state.user_lang)
        
        message_box.write(lines)
