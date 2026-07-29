import streamlit as st
import whisper
import os
import google.generativeai as genai

st.set_page_config(page_title="RANUMA Cloud Voice AI", page_icon="🎤", layout="centered")

st.title("🚀 RANUMA - Secure Voice AI")
st.write("பாதுகாப்பான Secrets முறையில் இயங்கும் AI சிஸ்டம்!")

# Streamlit Secrets-ல் இருந்து பாதுகாப்பாக கீ-ஐ எடுத்தல்
try:
    gemini_api_key = st.secrets["gemini_api_key"]
    st.success("✅ Secrets-ல் இருந்து API கீ வெற்றிகரமாக எடுக்கப்பட்டது!")
except Exception as e:
    st.error("❌ Secrets-ல் 'gemini_api_key' சரியாக அமைக்கப்படவில்லை.")

@st.cache_resource
def load_whisper_model():
    return whisper.load_model("base")

with st.spinner("Whisper AI மாடல் லோட் ஆகிறது..."):
    whisper_model = load_whisper_model()

audio_file = st.audio_input("🎤 மைக் பட்டனை அழுத்திப் பேசவும்:")

if audio_file is not None:
    audio_path = "temp_audio.wav"
    with open(audio_path, "wb") as f:
        f.write(audio_file.getbuffer())
    
    if st.button("டெக்ஸ்டாக மாற்றுக (Transcribe)"):
        with st.spinner("ப்ராசஸ் நடந்து கொண்டிருக்கிறது..."):
            raw_result = whisper_model.transcribe(audio_path, language="ta")
            spoken_text = raw_result["text"]
            
            st.markdown("### 🗣️ நீங்கள் பேசிய பேச்சுத் தமிழ்:")
            st.warning(spoken_text)
            
            try:
                genai.configure(api_key=gemini_api_key)
                gemini_model = genai.GenerativeModel('gemini-2.5-flash')
                
                prompt = f"""
                கீழே உள்ள உரை பேச்சுத் தமிழில் (Colloquial Tamil) உள்ளது. 
                அதன் அர்த்தம் சிறிதும் மாறாமல், முறையான இலக்கணப் பிழையற்ற எழுத்துத் தமிழாக (Formal Written Tamil) மாற்றித் தரவும்.
                கூடுதல் விளக்கங்கள் எதுவும் தேவையில்லை, திருத்தப்பட்ட உரையை மட்டும் தரவும்.
                
                பேச்சுத் தமிழ் உரை:
                {spoken_text}
                """
                
                response = gemini_model.generate_content(prompt)
                st.markdown("### 📝 திருத்தப்பட்ட இலக்கணத் தமிழ்:")
                st.success(response.text)
            except Exception as e:
                st.error(f"Gemini API ப்ராசஸில் பிழை: {e}")
                
        if os.path.exists(audio_path):
            os.remove(audio_path)
