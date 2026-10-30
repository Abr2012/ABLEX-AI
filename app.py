
import streamlit as st
from google import genai

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
    font-size: 55px !important;
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
        LANGUAGES,
        index=0
    )

    st.caption(
        "Auto Detect lets ABLEX AI identify the language "
        "of your message."
    )

    if st.button("🗑️ Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.write("🌐 100 language choices")
    st.write("✨ ABLEX AI Version 3.0")

if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown("### Welcome to ABLEX AI")
st.write(
    "Ask questions, learn new things, explore ideas, "
    "or chat in your preferred language."
)

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

prompt = st.chat_input("Message ABLEX AI...")

if prompt:
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
                    "Automatically identify the language of the "
                    "user's latest message. Reply in that same language. "
                    "If the message contains multiple languages, "
                    "use the main language."
                )
            else:
                language_instruction = (
                    f"Reply in {selected_language}. "
                    "Understand the user's message even if it is "
                    "written in another language."
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
                                "You are ABLEX AI, a friendly, "
                                "intelligent and responsible AI assistant. "
                                "Give clear, helpful and accurate answers. "
                                + language_instruction
                            )
                        }
                    )

                    answer = response.text or (
                        "Sorry, I couldn't generate a response."
                    )
                    st.markdown(answer)

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

        except Exception as e:
            st.error("Sorry, ABLEX AI could not respond. Please try again.")
            st.caption(str(e))
            st.session_state.messages.pop()


