import streamlit as st
from streamlit_mic_recorder import mic_recorder

st.title("🎙️ Record Your Call")

audio = mic_recorder(start_prompt="Start Recording", stop_prompt="Stop", use_container_width=True)

if audio:
    with open("recorded.wav", "wb") as f:
        f.write(audio["bytes"])
    st.success("✅ Saved as recorded.wav")
