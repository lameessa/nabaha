import streamlit as st
from streamlit_mic_recorder import mic_recorder
from main import process_audio_file
from pydub import AudioSegment
from pydub.utils import which
import io

# تأكد أن pydub يعرف مكان ffmpeg
AudioSegment.converter = which("ffmpeg")

st.title("🎙️ Record Your Call")

# تسجيل الصوت
audio = mic_recorder(start_prompt="Start Recording", stop_prompt="Stop", use_container_width=True)

if audio:
    try:
        # محاولة تحويل الملف إلى AudioSegment
        raw_audio = AudioSegment.from_file(io.BytesIO(audio["bytes"]), format="webm")
    except:
        raw_audio = AudioSegment.from_file(io.BytesIO(audio["bytes"]))  # خليه يحاول يكتشف الصيغة

    # تحويل الصيغة إلى wav (16000Hz + قناة واحدة mono)
    raw_audio = raw_audio.set_frame_rate(16000).set_channels(1)
    raw_audio.export("recorded.wav", format="wav")

    st.success("✅ Saved as recorded.wav")

    # تمرير الملف إلى النموذج
    result = process_audio_file("recorded.wav")

    if "error" in result:
        st.error("❌ Error: " + result["error"])
    else:
        st.subheader("📝 Transcription:")
        st.write(result["text"])

        st.subheader("📊 Prediction:")
        st.write(result["prediction"])
        st.caption(f"Confidence: {result['confidence']}%")
