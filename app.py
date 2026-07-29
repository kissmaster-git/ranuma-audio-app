import streamlit as st
import whisper
import os

st.set_page_config(page_title="RANUMA Cloud Voice AI", page_icon="🎤", layout="centered")

st.title("🚀 RANUMA - Audio Recognition")
st.write("இப்போது ஆடியோ பதிவேற்றம் செய்து அல்லது பேசி டெக்ஸ்டாக மாற்றலாம்!")

@st.cache_resource
def load_model():
    return whisper.load_model("base")

with st.spinner("Whisper AI மாடல் லோட் ஆகிறது... காத்திருக்கவும்..."):
    model = load_model()

st.success("AI மாடல் ரெடியாகிவிட்டது!")

# Streamlit இன்-பில்ட் மைக்ரோபோன் வசதி (எந்த எரரும் வராது)
audio_file = st.audio_input("🎤 மைக் பட்டனை அழுத்திப் பேசவும்:")

if audio_file is not None:
    st.audio(audio_file)
    
    # தற்காலிகமாக சேமித்தல்
    audio_path = "temp_audio.wav"
    with open(audio_path, "wb") as f:
        f.write(audio_file.getbuffer())
    
    if st.button("டெக்ஸ்டாக மாற்றுக (Transcribe)"):
        with st.spinner("ப்ராசஸ் நடந்து கொண்டிருக்கிறது..."):
            result = model.transcribe(audio_path, language="ta")
            st.markdown("### 📝 உங்களது டெக்ஸ்ட் முடிவு:")
            st.info(result["text"])
            
        if os.path.exists(audio_path):
            os.remove(audio_path)
