import streamlit as st
import  requests
import json
import io
from requests_toolbelt.multipart.encoder import MultipartEncoder
import speech_recognition as sr

recognizer = sr.Recognizer()
url = "https://innovative-project-kidney-frontend.onrender.com/kidneyrun"

st.set_page_config(page_title="Kidney Tomography Analyzer", page_icon="+")
st.markdown(
    """
    <style>
    html, body, #root {
    background: transparent !important;
 }

    * {
    background: transparent !important;
   }
   .stApp {
        background-image: url("https://www.shutterstock.com/shutterstock/videos/3584510353/thumb/4.jpg?ip=x480") !important;
         background-size: cover !important;
        background-position: center !important;
        background-repeat: no-repeat !important;
    }
    [data-testid="stAudioInputWaveformTimeCode"] {
        display: none !important;
        visibility: hidden !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown("### Kidney Tomography Analyzer")


if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "bot", "content": "Hi! How can I assist you?"}]

for msg in st.session_state.messages:
    if msg["role"] == "bot":
        with st.chat_message("assistant"):
            st.write(msg["content"])
    else:
        with st.chat_message("user"):
            st.write(msg["content"])

st.markdown("------------------------------------", unsafe_allow_html=True)
uploaded_file = st.file_uploader("->", type=["png", "jpg"], label_visibility="collapsed", key="uploader_small")
audio_data = st.audio_input("VOICE INPUT")
user_input = st.chat_input("Type your query...") 
if audio_data is not None:
    audio_file = io.BytesIO(audio_data.getbuffer())
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio)
            st.success(f"You said: **{text}**")
            user_input=text
        except sr.UnknownValueError:
            st.error("Sorry, I couldn't understand the audio.")
        except sr.RequestError:
            st.error("Speech Recognition API unavailable.")

if uploaded_file!=None and user_input!=None:
    st.session_state.messages.append({"role": "bot", "content": f"Your file '{uploaded_file.name}' has been uploaded and is being processed."})
    st.session_state.messages.append({"role": "user", "content": user_input})
    multipart_data = MultipartEncoder(
    fields={
        "promptt": json.dumps({"prompt": user_input}),
        "file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)
    })
    headers = {"Content-Type": multipart_data.content_type}
    bot_response = bytes(json.loads(requests.post(url, data=multipart_data, headers=headers).json()), "utf-8").decode("unicode_escape").replace('\\n', '\n')
    st.session_state.messages.append({"role": "bot", "content": bot_response})
    st.rerun()
elif user_input!=None:
    st.session_state.messages.append({"role": "user", "content": user_input})
    multipart_data = MultipartEncoder(
    fields={
        "promptt": json.dumps({"prompt": user_input})
    })
    headers = {"Content-Type": multipart_data.content_type}
    bot_response = bytes(json.loads(requests.post(url, data=multipart_data, headers=headers).json()), "utf-8").decode("unicode_escape").replace('\\n', '\n')
    print(bot_response,type(bot_response))
    st.session_state.messages.append({"role": "bot", "content": bot_response})
    user_input=None
    st.rerun()
