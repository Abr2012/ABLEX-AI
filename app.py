
import streamlit as st
import streamlit.components.v1 as components
from streamlit_mic_recorder import speech_to_text
from google import genai
from pathlib import Path

st.set_page_config(
    page_title="ABLEX AI",
    page_icon="🤖",
    layout="centered"
)

MODEL = "gemini-3.5-flash-lite"

# Connect the local browser voice component
live_voice_component = components.declare_component(
    "ablex_live_voice",
    path=str(Path(__file__).parent / "ablex_voice")
)

LANGUAGES = [
    "Auto Detect", "English", "Tamil", "Hindi", "Malayalam",
    "Telugu", "Kannada", "Bengali", "Marathi", "Gujarati",
    "Punjabi", "Urdu", "Odia", "Sanskrit", "Spanish",
    "French", "German", "Italian", "Portuguese", "Russian",
    "Japanese", "Korean", "Chinese", "Arabic", "Turkish",
    "Dutch", "Greek", "Hebrew", "Thai", "Vietnamese",
    "Indonesian", "Malay", "Filipino", "Swahili", "Afrikaans",
    "Albanian", "Amharic", "Armenian", "Azerbaijani", "Basque",
    "Belarusian", "Bosnian", "Bulgarian", "Burmese", "Catalan",
    "Cebuano", "Chichewa", "Corsican", "Croatian", "Czech",
    "Danish", "Esperanto", "Estonian", "Finnish", "Frisian",
    "Galician", "Georgian", "Haitian Creole", "Hausa", "Hawaiian",
    "Hungarian", "Icelandic", "Igbo", "Irish", "Javanese",
    "Kazakh", "Khmer", "Kinyarwanda", "Kurdish", "Kyrgyz",
    "Lao", "Latin", "Latvian", "Lithuanian", "Luxembourgish",
    "Macedonian", "Malagasy", "Maltese", "Maori", "Mongolian",
    "Nepali", "Norwegian", "Pashto", "Persian", "Polish",
    "Romanian", "Serbian", "Sesotho", "Shona", "Sindhi",
    "Sinhala", "Slovak", "Slovenian", "Somali", "Sundanese",
    "Swedish", "Tajik", "Tatar", "Ukrainian"
]

SPEECH_CODES = {
    "English": "en-IN",
    "Tamil": "ta-IN",
    "Hindi": "hi-IN",
    "Malayalam": "ml-IN",
    "Telugu": "te-IN",
    "Kannada": "kn-IN",
    "Bengali": "bn-IN",
    "Marathi": "mr-IN",
    "Gujarati": "gu-IN",
    "Punjabi": "pa-IN",
    "Urdu": "ur-PK",
    "Spanish": "es-ES",
    "French": "fr-FR",
    "German": "de-DE",
    "Italian": "it-IT",
    "Japanese": "ja-JP",
    "Korean": "ko-KR",
    "Chinese": "zh-CN",
    "Arabic": "ar-SA"
}

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#080d20,#17113a,#080d20);
    color: white;
}
h1,h2,h3,p,label {
    color: white !important;
}
.stButton button {
    background: #292052;
    color: white;
    border: 1px solid #765cff;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

st.title("🤖 ABLEX AI")
st.caption("Your multilingual AI assistant")

# Session state
defaults = {
    "messages": [],
    "last_voice": "",
    "voice_answer": "",
    "live_answer": "",
    "live_answer_id": 0,
    "last_live_event_id": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

with st.sidebar:
    st.header("⚙️ Settings")
    language = st.selectbox("Response language", LANGUAGES)

    if st.button("🗑️ Clear conversation"):
        st.session_state.messages = []
        st.session_state.last_voice = ""
        st.session_state.voice_answer = ""
        st.session_state.live_answer = ""
        st.session_state.live_answer_id = 0
        st.session_state.last_live_event_id = None
        st.rerun()


def ask_ablex():
    api_key = st.secrets.get("GEMINI_API_KEY", "")

    if not api_key:
        return "GEMINI_API_KEY is missing from Streamlit Secrets."

    if language == "Auto Detect":
        instruction = "Reply in the same language as the latest user message."
    else:
        instruction = f"Reply in {language}."

    contents = []

    for message in st.session_state.messages[-12:]:
        contents.append({
            "role": "user" if message["role"] == "user" else "model",
            "parts": [{"text": message["content"]}]
        })

    try:
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model=MODEL,
            contents=contents,
            config={
                "system_instruction":
                    "You are ABLEX AI, a friendly and helpful assistant. "
                    + instruction,
                "max_output_tokens": 700
            }
        )

        return response.text or "I couldn't generate a response."

    except Exception as error:
        return f"Gemini error: {error}"


def send_question(question):
    question = question.strip()

    if not question:
        return ""

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    answer = ask_ablex()

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    return answer


mode = st.radio(
    "Choose your mode",
    [
        "💬 Text Chat",
        "🎙️ ABLEX Voice",
        "🔴 ABLEX Live Voice"
    ],
    horizontal=True
)


# TEXT CHAT
if mode == "💬 Text Chat":

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Ask ABLEX AI anything...")

    if prompt:
        with st.spinner("ABLEX is thinking..."):
            send_question(prompt)

        st.rerun()


# ORIGINAL ONE-TURN VOICE MODE
elif mode == "🎙️ ABLEX Voice":

    st.subheader("🎙️ Talk to ABLEX AI")
    st.write("Tap the microphone, speak, and wait for transcription.")

    spoken_text = speech_to_text(
        language="en",
        start_prompt="🎙️ Start recording",
        stop_prompt="⏹️ Stop recording",
        just_once=True,
        use_container_width=True,
        key="ablex_microphone"
    )

    if spoken_text:
        st.success("Speech recognized!")
        st.write("**You said:**", spoken_text)

        if spoken_text != st.session_state.last_voice:
            st.session_state.last_voice = spoken_text

    if st.session_state.last_voice:
        if st.button("🤖 Send to ABLEX AI"):
            with st.spinner("ABLEX is thinking..."):
                answer = send_question(st.session_state.last_voice)
                st.session_state.voice_answer = answer
                st.session_state.last_voice = ""

            st.rerun()

    if st.session_state.voice_answer:
        st.subheader("🤖 ABLEX's reply")
        st.write(st.session_state.voice_answer)

        import json

        speech_text = json.dumps(st.session_state.voice_answer)
        speech_language = "en-IN"

        st.components.v1.html(
            f"""
            <script>
            const answer = {speech_text};
            const utterance = new SpeechSynthesisUtterance(answer);
            utterance.lang = {json.dumps(speech_language)};
            window.speechSynthesis.cancel();
            window.speechSynthesis.speak(utterance);
            </script>
            """,
            height=0
        )

        if st.button("🔁 Clear answer"):
            st.session_state.voice_answer = ""
            st.rerun()


# NEW LIVE VOICE MODE
else:

    st.subheader("🔴 ABLEX Live Voice")
    st.write(
        "Start a conversation. ABLEX will answer aloud and "
        "attempt to listen again after each answer."
    )

    speech_language = SPEECH_CODES.get(language, "en-IN")

    voice_result = live_voice_component(
        answer=st.session_state.live_answer,
        answer_id=st.session_state.live_answer_id,
        speech_language=speech_language,
        key="ablex_live_component"
    )

    if isinstance(voice_result, dict):
        spoken_question = voice_result.get("text", "").strip()
        event_id = voice_result.get("event_id")

        if (
            spoken_question
            and event_id is not None
            and event_id != st.session_state.last_live_event_id
        ):
            st.session_state.last_live_event_id = event_id

            with st.spinner("🤖 ABLEX is thinking..."):
                answer = send_question(spoken_question)

            st.session_state.live_answer = answer
            st.session_state.live_answer_id += 1

            st.rerun()

    st.divider()

    st.subheader("💬 Conversation")

    for message in st.session_state.messages[-12:]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


