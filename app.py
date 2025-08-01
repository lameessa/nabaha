import streamlit as st
from streamlit_mic_recorder import mic_recorder
from main import process_audio_file
from pydub import AudioSegment
import io
import os

# ✅ Force ffmpeg path for pydub (set only ONCE and early)
ffmpeg_path = r"C:\ffmpeg\bin\ffmpeg.exe"
if not os.path.exists(ffmpeg_path):
    raise FileNotFoundError(f"ffmpeg not found at: {ffmpeg_path}")

AudioSegment.converter = ffmpeg_path


# --- Initialize session state ---
if "page" not in st.session_state:
    st.session_state.page = "home"

if "result" not in st.session_state:
    st.session_state.result = None

# --- Page: Home ---
if st.session_state.page == "home":
    st.title("📞 Vishing Detection App")

    st.markdown("### Choose an option:")
    if st.button("📊 View Risk Assessment Table"):
        st.session_state.page = "risk_table"
        st.rerun()

    if st.button("🎙️ Record a Phone Call"):
        st.session_state.page = "record"
        st.rerun()

# --- Page: Risk Table ---
elif st.session_state.page == "risk_table":
    st.title("📊 Static Risk Assessment Table")
    st.markdown("This is a sample table showing risk types and their descriptions.")

    st.table({
        "Risk Type": ["رمز تحقق", "بنك", "تهديد", "رقم بطاقة", "معلومات حساسة", "مكالمة عادية", "تخويف", "طلب تحويل"],
        "Description": [
            "طلب رمز تحقق أو OTP",
            "ذكر اسم بنك أو مؤسسة مالية",
            "وجود تهديد أو إنذار",
            "طلب رقم بطاقة ائتمانية",
            "طلب معلومات شخصية أو حساسة",
            "مكالمة لا تحتوي على محتوى خطير",
            "استخدام لغة تخويف أو تهديد",
            "طلب تحويل مالي أو بنكي"
        ]
    })

    if st.button("🔙 Back to Home"):
        st.session_state.page = "home"
        st.rerun()

# --- Page: Record ---
elif st.session_state.page == "record":
    st.title("🎙️ Record Your Phone Call")

    audio = mic_recorder(start_prompt="Start Recording", stop_prompt="Stop", use_container_width=True)

    if audio:
        try:
            raw_audio = AudioSegment.from_file(io.BytesIO(audio["bytes"]), format="webm")
        except:
            raw_audio = AudioSegment.from_file(io.BytesIO(audio["bytes"]))  # auto format

        raw_audio = raw_audio.set_frame_rate(16000).set_channels(1)
        raw_audio.export("recorded.wav", format="wav")

        st.success("✅ Audio saved successfully!")

        result = process_audio_file("recorded.wav")

        if "error" in result:
            st.error("❌ Error: " + result["error"])
        else:
            st.session_state.result = result

            st.subheader("📝 Transcription:")
            st.write(result["text"])

            st.subheader("📊 Prediction:")
            st.write(result["prediction"])
            st.caption(f"Confidence: {result['confidence']}%")

            if st.button("➡️ Go to Results"):
                st.session_state.page = "results"
                st.rerun()

    if st.button("🔙 Back to Home"):
        st.session_state.page = "home"
        st.rerun()

# --- Page: Results ---
elif st.session_state.page == "results":
    st.title("📋 Call Risk Analysis Results")

    if st.session_state.result:
        st.write("### 📝 Transcription")
        st.write(st.session_state.result["text"])

        st.write("### 📊 Prediction")
        st.write(st.session_state.result["prediction"])
        st.caption(f"Confidence: {st.session_state.result['confidence']}%")
    else:
        st.warning("No result available. Please record a call first.")

    if st.button("🔙 Back to Home"):
        st.session_state.page = "home"
        st.rerun()
