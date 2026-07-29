import streamlit as st
import whisper
import os
from audiorecorder import audiorecorder

st.set_page_config(page_title="RANUMA Cloud Voice AI", page_icon="🎤", layout="centered")

st.title("🚀 RANUMA - Live Voice Recognition")
st.write("இப்போது மைக்ரோபோனில் நேரடியாகப் பேசி டெக்ஸ்டாக மாற்றலாம்!")

@st.cache_resource
def load_model():
    return whisper.load_model("base")

with st.spinner("Whisper AI மாடல் லோட் ஆகிறது... காத்திருக்கவும்..."):
    model = load_model()

st.success("AI மாடல் ரெடியாகிவிட்டது!")

st.write("### 🎤 மைக்ரோபோனில் பேச கீழே உள்ள பட்டனை அழுத்தவும்:")
# லைவ் மைக் ரெக்கார்டர்
audio = audiorecorder("பதிவு செய்ய Start அழுத்தவும்", "நிறுத்த Stop அழுத்தவும்")

if len(audio) > 0:
    # ஆடியோவை தற்காலிகமாக சேமித்தல்
    audio_path = "recorded_audio.wav"
    audio.export(audio_path, format="wav")
    
    st.audio(audio_path)
    
    if st.button("டெக்ஸ்டாக மாற்றுக (Transcribe)"):
        with st.spinner("ப்ராசஸ் நடந்து கொண்டிருக்கிறது..."):
            result = model.transcribe(audio_path, language="ta")
            st.markdown("### 📝 உங்களது டெக்ஸ்ட் முடிவு:")
            st.info(result["text"])
            
        if os.path.exists(audio_path):
            os.remove(audio_path)
