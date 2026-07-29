import streamlit as st
import whisper
import os

st.set_page_config(page_title="RANUMA Cloud Voice AI", page_icon="🎤", layout="centered")

st.title("🚀 RANUMA - Cloud Audio Recognition")
st.write("இப்போது உங்களது வாய்ஸ் ரெகக்னிஷன் கிளவுட் சர்வரில் (Cloud Server) இயங்குகிறது!")

@st.cache_resource
def load_model():
    # கிளவுட்டில் லைட்டாக இருக்க 'tiny' அல்லது 'base' மாடல்
    return whisper.load_model("base")

with st.spinner("Whisper AI மாடல் கிளவுட்டில் லோட் ஆகிறது... தயவுசெய்து காத்த ிருக்கவும்..."):
    model = load_model()

st.success("AI மாடல் வெற்றிகரமாக ரெடியாகிவிட்டது!")

# ஆடியோ ஃபைல் அப்லோடு செய்யும் வசதி (அல்லது ரெக்கார்டு)
audio_file = st.file_uploader("உங்கள் ஆடியோ ஃபைலை (.mp3, .wav, .webm) இங்கே அப்லோடு செய்யவும்:", type=["mp3", "wav", "webm"])

if audio_file is not None:
    # தற்காலிகமாக சேமித்தல்
    with open("temp_audio.file", "wb") as f:
        f.write(audio_file.getbuffer())
    
    st.audio(audio_file, format='audio/webm')
    
    if st.button("டெக்ஸ்டாக மாற்றுக (Transcribe)"):
        with st.spinner("ப்ராசஸ் நடந்து கொண்டிருக்கிறது..."):
            result = model.transcribe("temp_audio.file", language="ta")
            st.markdown("### 📝 உங்களது டெக்ஸ்ட் முடிவு:")
            st.info(result["text"])
            
        # தற்காலிக கோடை நீக்குதல்
        if os.path.exists("temp_audio.file"):
            os.remove("temp_audio.file")
