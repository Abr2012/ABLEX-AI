
import streamlit as st
import streamlit.components.v1 as components
from google import genai
import html
import json

# ---------------- APP CONFIG ----------------
st.set_page_config(
    page_title="ABLEX AI",
    page_icon="🤖",
    layout="centered"
)

MODEL = "gemini-3.5-flash-lite"

LANGUAGES = [
    "Auto Detect", "English", "Tamil", "Hindi", "Malayalam",
    "Telugu", "Kannada", "Bengali", "Marathi", "Gujarati",
    "Punjabi", "Urdu", "Odia", "Assamese", "Sanskrit",
    "Spanish", "French", "German", "Italian", "Portuguese",
    "Russian", "Japanese", "Korean", "Chinese", "Arabic",
    "Turkish", "Dutch", "Greek", "Hebrew", "Thai",
    "Vietnamese", "Indonesian", "Malay", "Filipino", "Swahili",
    "Afrikaans", "Albanian", "Amharic", "Armenian", "Azerbaijani",
    "Basque", "Belarusian", "Bosnian", "Bulgarian", "Burmese",
    "Catalan", "Cebuano", "Chichewa", "Corsican", "Croatian",
    "Czech", "Danish", "Esperanto", "Estonian", "Finnish",
    "Frisian", "Galician", "Georgian", "Haitian Creole", "Hausa",
    "Hawaiian", "Hungarian", "Icelandic", "Igbo", "Irish",
    "Javanese", "Kazakh", "Khmer", "Kinyarwanda", "Kurdish",
    "Kyrgyz", "Lao", "Latin", "Latvian", "Lithuanian",
    "Luxembourgish", "Macedonian", "Malagasy", "Maltese", "Maori",
    "Mongolian", "Nepali", "Norwegian", "Pashto", "Persian",
    "Polish", "Romanian", "Serbian", "Sesotho", "Shona",
    "Sindhi", "Sinhala", "Slovak", "Slovenian", "Somali",
    "Sundanese", "Swedish", "Tajik", "Tatar", "Ukrainian"
]

# ---------------- DESIGN ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#080d20,#17113a,#080d20);
    color: white;
}
h1, h2, h3, p, label {
    color: white !important;
}
.stButton button {
    border-radius: 12px;
    border: 1px solid #765cff;
    background: #292052;
    color: white;
    min-height: 42px;
}
.stTextInput input, .stTextArea textarea {
    background: #171b35;
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.title("🤖 ABLEX AI")
st.caption("Your multilingual AI assistant")

# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "voice_question" not in st.session_state:
    st.session_state.voice_question = ""

if "voice_answer" not in st.session_state:
    st.session_state.voice_answer = ""

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("⚙️ Settings")

    language = st.selectbox(
        "Response language",
        LANGUAGES,
        index=0
    )

    if st.button("🗑️ Clear conversation"):
        st.session_state.messages = []
        st.session_state.voice_question = ""
        st.session_state.voice_answer = ""
        st.rerun()

    st.caption("ABLEX AI | Voice Prototype")

# ---------------- GEMINI ----------------
def ask_ablex(prompt):
    api_key = st.secrets.get("GEMINI_API_KEY", "")

    if not api_key:
        return "Gemini API key is missing. Add GEMINI_API_KEY in Streamlit Secrets."

    try:
        client = genai.Client(api_key=api_key)

        if language == "Auto Detect":
            language_instruction = (
                "Reply in the same language as the user's latest message."
            )
        else:
            language_instruction = (
                f"Reply in {language}. Keep your answer clear and helpful."
            )

        history = []
        for message in st.session_state.messages[-12:]:
            role = "user" if message["role"] == "user" else "model"
            history.append({
                "role": role,
                "parts": [{"text": message["content"]}]
            })

        response = client.models.generate_content(
            model=MODEL,
            contents=history,
            config={
                "system_instruction": (
                    "You are ABLEX AI, a friendly and helpful multilingual "
                    "AI assistant. Give accurate, clear answers. "
                    + language_instruction
                ),
                "max_output_tokens": 700
            }
        )

        return response.text or "I couldn't generate a response. Please try again."

    except Exception as error:
        return f"AI error: {error}"

# ---------------- CHAT DISPLAY ----------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------- MODES ----------------
mode = st.radio(
    "Choose your mode",
    ["💬 Text Chat", "🎙️ ABLEX Voice"],
    horizontal=True
)

# ---------------- TEXT CHAT ----------------
if mode == "💬 Text Chat":
    prompt = st.chat_input("Ask ABLEX AI anything...")

    if prompt:
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        with st.chat_message("assistant"):
            with st.spinner("ABLEX is thinking..."):
                answer = ask_ablex(prompt)
            st.markdown(answer)

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

        st.rerun()

# ---------------- VOICE MODE ----------------
else:
    st.subheader("🎙️ Talk to ABLEX AI")
    st.write("Tap the microphone, speak, and submit your question.")

    components.html("""
    <div style="
        background:#171b35;
        padding:22px;
        border-radius:16px;
        text-align:center;
        color:white;
        font-family:Arial;
    ">
      <button id="start" style="
        background:#6545df;
        color:white;
        border:0;
        border-radius:50px;
        padding:16px 28px;
        font-size:17px;
        cursor:pointer;
      ">🎙️ Start speaking</button>

      <p id="status" style="margin-top:15px">
        Microphone is ready.
      </p>

      <p id="result" style="
        background:#252344;
        padding:12px;
        border-radius:10px;
        min-height:35px;
        overflow-wrap:anywhere;
      ">Your speech will appear here.</p>

      <button id="send" style="
        background:#16856b;
        color:white;
        border:0;
        border-radius:10px;
        padding:12px 22px;
        font-size:15px;
        cursor:pointer;
      ">Send voice question</button>
    </div>

    <script>
    const startButton = document.getElementById("start");
    const sendButton = document.getElementById("send");
    const statusText = document.getElementById("status");
    const resultText = document.getElementById("result");

    let transcript = "";

    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      statusText.innerText =
        "Speech recognition is not supported. Try Google Chrome.";
      startButton.disabled = true;
    } else {
      const recognition = new SpeechRecognition();
      recognition.lang = "en-IN";
      recognition.continuous = false;
      recognition.interimResults = false;

      startButton.onclick = () => {
        transcript = "";
        resultText.innerText = "Listening...";
        statusText.innerText = "Speak now...";
        recognition.start();
      };

      recognition.onresult = (event) => {
        transcript = event.results[0][0].transcript;
        resultText.innerText = transcript;
        statusText.innerText = "Speech recognized. Press Send.";
      };

      recognition.onerror = (event) => {
        statusText.innerText = "Microphone error: " + event.error;
      };

      recognition.onend = () => {
        if (!transcript) {
          statusText.innerText = "Listening ended. Try again.";
        }
      };

      sendButton.onclick = () => {
        if (!transcript.trim()) {
          statusText.innerText = "Please speak first.";
          return;
        }

        const url = new URL(window.parent.location.href);
        url.searchParams.set("voice_question", transcript);
        window.parent.location.href = url.toString();
      };
    }
    </script>
    """, height=270)

    # Streamlit receives the question through the URL query parameter.
    received_question = st.query_params.get("voice_question", "")

    if received_question:
        st.session_state.voice_question = received_question
        st.query_params.clear()

    if st.session_state.voice_question:
        st.write("**Recognized question:**")
        st.info(st.session_state.voice_question)

        if st.button("🤖 Ask ABLEX AI", key="ask_voice"):
            question = st.session_state.voice_question

            st.session_state.messages.append({
                "role": "user",
                "content": question
            })

            with st.spinner("ABLEX is thinking..."):
                answer = ask_ablex(question)

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

            st.session_state.voice_answer = answer
            st.session_state.voice_question = ""
            st.rerun()

    if st.session_state.voice_answer:
        st.subheader("🤖 ABLEX's answer")
        st.markdown(st.session_state.voice_answer)

        # Browser speech synthesis
        speech_text = json.dumps(st.session_state.voice_answer)
        speech_language = "en-IN" if language == "Auto Detect" else "en-IN"

        components.html(
            f"""
            <script>
            const textToSpeak = {speech_text};
            const utterance = new SpeechSynthesisUtterance(textToSpeak);
            utterance.lang = {json.dumps(speech_language)};
            window.speechSynthesis.cancel();
            window.speechSynthesis.speak(utterance);
            </script>
            """,
            height=20
        )

        if st.button("🔁 Clear voice answer"):
            st.session_state.voice_answer = ""
            st.rerun()



