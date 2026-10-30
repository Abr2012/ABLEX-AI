
import streamlit as st
from google import genai
from streamlit_mic_recorder import speech_to_text

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

    st.caption("Choose Auto Detect to reply in your message language.")

    if st.button("🗑️ Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.write("🌐 100 language choices")
    st.write("✨ ABLEX AI Version 4.0")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "voice_text" not in st.session_state:
    st.session_state.voice_text = ""

st.markdown("### Welcome to ABLEX AI")
st.write("Ask questions, learn, explore ideas, and chat in your language.")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("📚 Learning\n\nUnderstand difficult topics.")

with col2:
    st.info("💡 Ideas\n\nExplore creative ideas.")

with col3:
    st.info("💻 Coding\n\nLearn programming.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input and microphone
chat_col, mic_col = st.columns([9, 1])

with chat_col:
    typed_prompt = st.chat_input("Message ABLEX AI...")

with mic_col:
    st.write("")
    st.write("")
    voice_result = speech_to_text(
        language="en",
        start_prompt="🎤",
        stop_prompt="⏹️",
        just_once=True,
        key="voice_input"
    )

if voice_result:
    st.session_state.voice_text = voice_result

if st.session_state.voice_text:
    st.info("🎤 Recognized speech: " + st.session_state.voice_text)

    if st.button("Send voice message"):
        st.session_state.pending_prompt = st.session_state.voice_text
        st.session_state.voice_text = ""
        st.rerun()

if typed_prompt:
    st.session_state.pending_prompt = typed_prompt

if "pending_prompt" in st.session_state:
    prompt = st.session_state.pending_prompt
    del st.session_state.pending_prompt

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    api_key = st.secrets.get("GEMINI_API_KEY", "")

    if not api_key:
        st.error("Gemini API key is missing. Check Streamlit Secrets.")
    else:
        try:
            client = genai.Client(api_key=api_key)

            if selected_language == "Auto Detect":
                language_instruction = (
                    "Detect the language of the latest user message "
                    "and reply in that same language."
                )
            else:
                language_instruction = (
                    f"Reply in {selected_language}, even if the "
                    "user writes in another language."
                )

            conversation = []

            for msg in st.session_state.messages[-12:]:
                role = "user" if msg["role"] == "user" else "model"
                conversation.append({
                    "role": role,
                    "parts": [{"text": msg["content"]}]
                })

            with st.chat_message("assistant"):
                with st.spinner("ABLEX AI is thinking..."):
                    response = client.models.generate_content(
                        model="gemini-3.5-flash-lite",
                        contents=conversation,
                        config={
                            "system_instruction": (
                                "You are ABLEX AI, a friendly, intelligent "
                                "and responsible AI assistant. Give clear, "
                                "helpful and accurate answers. "
                                + language_instruction
                            )
                        }
                    )

                    answer = response.text or "Please try again."
                    st.markdown(answer)

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

        except Exception as e:
            st.error("ABLEX AI could not respond. Please try again.")
            st.caption(str(e))
            st.session_state.messages.pop()


