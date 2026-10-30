
import streamlit as st
import streamlit.components.v1 as components
from google import genai
import json

st.set_page_config(
    page_title="ABLEX AI",
    page_icon="🤖",
    layout="wide"
)

LANGUAGES = [
    "Auto Detect", "English", "Tamil", "Hindi", "Malayalam",
    "Telugu", "Kannada", "Bengali", "Marathi", "Gujarati",
    "Punjabi", "Urdu", "Odia", "Assamese", "Nepali",
    "Sinhala", "Arabic", "French", "Spanish", "German",
    "Italian", "Portuguese", "Russian", "Japanese", "Korean",
    "Chinese", "Thai", "Vietnamese", "Indonesian", "Malay",
    "Turkish", "Dutch", "Greek", "Hebrew", "Persian",
    "Swahili", "Afrikaans", "Albanian", "Amharic", "Armenian",
    "Azerbaijani", "Basque", "Belarusian", "Bosnian", "Bulgarian",
    "Burmese", "Catalan", "Croatian", "Czech", "Danish",
    "Estonian", "Filipino", "Finnish", "Georgian", "Haitian Creole",
    "Hausa", "Hungarian", "Icelandic", "Igbo", "Irish",
    "Javanese", "Kazakh", "Khmer", "Kinyarwanda", "Kurdish",
    "Kyrgyz", "Lao", "Latvian", "Lithuanian", "Luxembourgish",
    "Macedonian", "Malagasy", "Maltese", "Mongolian", "Oromo",
    "Pashto", "Polish", "Romanian", "Serbian", "Slovak",
    "Slovenian", "Somali", "Sundanese", "Swedish", "Tajik",
    "Tatar", "Tibetan", "Turkmen", "Ukrainian", "Uzbek",
    "Welsh", "Wolof", "Xhosa", "Yoruba", "Zulu",
    "Māori", "Samoan", "Tongan", "Quechua", "Galician"
]

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #080d20, #111b38);
    color: white;
}
h1 {
    background: linear-gradient(90deg, #35c9ff, #a66cff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
[data-testid="stChatMessage"] {
    background: #172442;
    border-radius: 15px;
    padding: 12px;
}
.stButton button {
    background: linear-gradient(90deg, #168cff, #8755ff);
    color: white;
    border: none;
    border-radius: 12px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.title("🤖 ABLEX AI")
st.caption("Your intelligent multilingual AI assistant")

with st.sidebar:
    st.header("⚙️ Settings")
    selected_language = st.selectbox(
        "🌍 Response language",
        LANGUAGES
    )

    st.divider()
    st.write("✨ ABLEX AI LIVE")
    st.write("🌐 100 language choices")

    if st.button("🗑️ Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "voice_answer" not in st.session_state:
    st.session_state.voice_answer = ""

if "voice_language" not in st.session_state:
    st.session_state.voice_language = "en-US"

st.markdown("### Welcome to ABLEX AI")
st.write("Chat by typing or try ABLEX LIVE voice mode.")

mode = st.radio(
    "Choose your mode",
    ["Text Chat", "🎙️ ABLEX LIVE"],
    horizontal=True
)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def ask_ablex(prompt):
    api_key = st.secrets.get("GEMINI_API_KEY", "")

    if not api_key:
        st.error("Gemini API key is missing. Check Streamlit Secrets.")
        return

    try:
        client = genai.Client(api_key=api_key)

        if selected_language == "Auto Detect":
            language_instruction = (
                "Detect the language of the user's latest message "
                "and reply in that same language."
            )
        else:
            language_instruction = (
                f"Reply in {selected_language}."
            )

        conversation = []
        for msg in st.session_state.messages[-12:]:
            role = "user" if msg["role"] == "user" else "model"
            conversation.append({
                "role": role,
                "parts": [{"text": msg["content"]}]
            })

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=conversation,
            config={
                "system_instruction": (
                    "You are ABLEX AI, a friendly, intelligent and "
                    "responsible AI assistant. Give clear and accurate "
                    "answers. " + language_instruction
                )
            }
        )

        answer = response.text or "Sorry, please try again."

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

        return answer

    except Exception as error:
        st.error("ABLEX AI could not respond. Please try again.")
        st.caption(str(error))
        return None


if mode == "Text Chat":
    prompt = st.chat_input("Message ABLEX AI...")

    if prompt:
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("ABLEX AI is thinking..."):
                answer = ask_ablex(prompt)
                if answer:
                    st.markdown(answer)

else:
    st.markdown("### 🎙️ ABLEX LIVE VOICE")
    st.write(
        "Press Start Listening, speak your question, and ABLEX AI "
        "will answer aloud automatically."
    )

    components.html("""
    <div style="
        background:#172442;
        padding:22px;
        border-radius:18px;
        text-align:center;
        color:white;
        font-family:Arial;
    ">
      <div style="font-size:42px;">🎙️</div>
      <h3>ABLEX LIVE</h3>
      <p id="status">Ready to listen</p>
      <button id="start" style="
        background:linear-gradient(90deg,#168cff,#8755ff);
        color:white;border:0;padding:13px 22px;
        border-radius:12px;font-size:16px;cursor:pointer;">
        Start Listening
      </button>
      <button id="stop" style="
        background:#b83250;color:white;border:0;
        padding:13px 22px;border-radius:12px;
        font-size:16px;cursor:pointer;margin-left:8px;">
        Stop
      </button>
      <p id="heard" style="margin-top:18px;"></p>
      <p style="font-size:12px;color:#b9c6df;">
        Your browser may ask for microphone permission.
      </p>
    </div>

    <script>
    const statusText = document.getElementById("status");
    const heardText = document.getElementById("heard");
    const startButton = document.getElementById("start");
    const stopButton = document.getElementById("stop");

    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    let recognition;
    let listening = false;

    function speak(text) {
      if (!("speechSynthesis" in window)) {
        statusText.innerText = "Speech output is not supported.";
        return;
      }

      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = "en-US";
      utterance.onend = () => {
        if (listening) {
          statusText.innerText =
            "Reply finished. Press Start Listening for your next question.";
        }
      };
      window.speechSynthesis.speak(utterance);
    }

    if (!SpeechRecognition) {
      statusText.innerText =
        "Speech recognition is unavailable in this browser.";
      startButton.disabled = true;
    } else {
      recognition = new SpeechRecognition();
      recognition.lang = "en-US";
      recognition.continuous = false;
      recognition.interimResults = false;

      recognition.onstart = () => {
        statusText.innerText = "Listening...";
      };

      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        heardText.innerText = "You said: " + transcript;
        statusText.innerText =
          "Your question was heard. Send it in the chat below.";
        window.parent.postMessage({
          type: "ABLEX_VOICE_TEXT",
          text: transcript
        }, "*");
      };

      recognition.onerror = (event) => {
        statusText.innerText = "Microphone error: " + event.error;
      };

      recognition.onend = () => {
        if (listening) {
          statusText.innerText =
            "Listening stopped. Press Start Listening again.";
        }
      };

      startButton.onclick = () => {
        listening = true;
        try {
          recognition.start();
        } catch (e) {
          statusText.innerText = "Please try starting again.";
        }
      };

      stopButton.onclick = () => {
        listening = false;
        recognition.stop();
        window.speechSynthesis.cancel();
        statusText.innerText = "Voice mode stopped.";
      };
    }
    </script>
    """, height=300)

    st.info(
        "Voice mode prototype: speech recognition happens in the browser. "
        "The recognized question must still be submitted to Gemini by the "
        "Streamlit app. This embedded interface does not yet connect that "
        "browser event to the Python chat automatically."
    )

    voice_prompt = st.text_input(
        "Your recognized voice question",
        key="voice_question"
    )

    if st.button("Send voice question"):
        if voice_prompt.strip():
            st.session_state.messages.append({
                "role": "user",
                "content": voice_prompt
            })

            with st.spinner("ABLEX AI is thinking..."):
                answer = ask_ablex(voice_prompt)

            if answer:
                st.session_state.voice_answer = answer
                st.markdown("### ABLEX AI says")
                st.write(answer)

                components.html(
                    """
                    <script>
                    const answer = %s;
                    const utterance =
                        new SpeechSynthesisUtterance(answer);
                    utterance.lang = "en-US";
                    window.speechSynthesis.cancel();
                    window.speechSynthesis.speak(utterance);
                    </script>
                    """ % json.dumps(answer),
                    height=0
                )


