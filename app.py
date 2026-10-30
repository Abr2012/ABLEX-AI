
import streamlit as st
from streamlit_mic_recorder import speech_to_text
from google import genai
import json

st.set_page_config(
    page_title="ABLEX AI",
    page_icon="🤖",
    layout="centered"
)

MODEL = "gemini-3.5-flash-lite"

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

if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_voice" not in st.session_state:
    st.session_state.last_voice = ""

if "voice_answer" not in st.session_state:
    st.session_state.voice_answer = ""

with st.sidebar:
    st.header("⚙️ Settings")
    language = st.selectbox("Response language", LANGUAGES)

    if st.button("🗑️ Clear conversation"):
        st.session_state.messages = []
        st.session_state.last_voice = ""
        st.session_state.voice_answer = ""
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
        return

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
    ["💬 Text Chat", "🎙️ ABLEX Voice"],
    horizontal=True
)

if mode == "💬 Text Chat":
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Ask ABLEX AI anything...")

    if prompt:
        with st.spinner("ABLEX is thinking..."):
            send_question(prompt)
        st.rerun()

else:
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

        speech_text = json.dumps(st.session_state.voice_answer)
        speech_language = "en-IN"

        st.components.v1.html(
            f"""
            <script>
            const answer = {speech_text};
            const speak = () => {{
                window.speechSynthesis.cancel();
                const utterance = new SpeechSynthesisUtterance(answer);
                utterance.lang = {json.dumps(speech_language)};
                window.speechSynthesis.speak(utterance);
            }};
            speak();
            </script>
            """,
            height=0
        )

        if st.button("🔁 Clear answer"):
            st.session_state.voice_answer = ""
            st.rerun()



