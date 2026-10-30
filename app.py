
import streamlit as st
from google import genai

st.set_page_config(
    page_title="ABLEX AI",
    page_icon="🤖",
    layout="wide"
)

# FUTURISTIC DESIGN
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #080d1c, #11152b);
    color: #ffffff;
}
[data-testid="stSidebar"] {
    background: #10162b;
}
.main-title {
    font-size: 48px;
    font-weight: 900;
    background: linear-gradient(90deg, #00d4ff, #a855f7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.subtitle {
    color: #aab5d0;
    font-size: 17px;
}
div.stButton > button {
    background: linear-gradient(90deg, #087cff, #8b42e8);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 10px 20px;
}
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown(
    '<div class="main-title">✦ ABLEX AI</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="subtitle">Your intelligent universe starts here.</div>',
    unsafe_allow_html=True
)

st.write("")

# API CONNECTION
try:
    api_key = st.secrets.get("GEMINI_API_KEY", "")
except Exception:
    api_key = ""

if not api_key:
    st.error("Gemini API key is missing. Check Streamlit Secrets.")
    st.stop()

client = genai.Client(api_key=api_key)

# CHAT MEMORY
if "messages" not in st.session_state:
    st.session_state.messages = []

# SIDEBAR
with st.sidebar:
    st.markdown("## ✦ ABLEX AI")
    st.caption("FUTURE INTELLIGENCE")

    st.divider()

    st.markdown("### Navigation")
    st.write("💬 AI Chat")
    st.write("🧠 Smart Assistant")
    st.write("🌐 Languages")
    st.write("⚙️ Settings")

    st.divider()

    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.caption("ABLEX AI • Version 2.0")

# WELCOME SCREEN
if not st.session_state.messages:
    st.markdown("## Welcome to ABLEX AI 👋")
    st.write("What would you like to explore today?")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("📚 Learning\n\nExplore new topics.")
    with col2:
        st.info("💡 Ideas\n\nDiscover creative ideas.")
    with col3:
        st.info("💻 Coding\n\nLearn programming.")

# DISPLAY CHAT HISTORY
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# USER INPUT
question = st.chat_input("Ask ABLEX AI anything...")

if question:
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("✦ ABLEX AI is thinking..."):
            try:
                conversation = []

                for msg in st.session_state.messages[-11:]:
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
                            "You are ABLEX AI, a friendly, intelligent "
                            "and responsible AI assistant. Give clear, "
                            "helpful and accurate answers."
                        )
                    }
                )

                answer = response.text or "I couldn't generate a response."
                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as error:
                st.error("ABLEX AI could not respond. Please try again.")
                st.caption(str(error))
                st.session_state.messages.pop()


