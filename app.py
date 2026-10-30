
import streamlit as st
from google import genai

st.set_page_config(
    page_title="ABLEX AI",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 ABLEX AI")
st.subheader("Your Intelligent AI Assistant")

st.markdown(
    "Welcome to ABLEX AI! Ask questions, learn new things "
    "and explore ideas."
)

# Securely read the API key
try:
    api_key = st.secrets.get("GEMINI_API_KEY", "")
except Exception:
    api_key = ""

if not api_key:
    st.error("Gemini API key is not configured.")
    st.info("Add GEMINI_API_KEY in Streamlit Settings → Secrets.")
    st.stop()

# Connect to Gemini
client = genai.Client(api_key=api_key)

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Ask ABLEX AI
question = st.chat_input("Message ABLEX AI...")

if question:
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("ABLEX AI is thinking..."):
            try:
                history = ""
                for msg in st.session_state.messages[-10:-1]:
                    role = "User" if msg["role"] == "user" else "ABLEX AI"
                    history += f"{role}: {msg['content']}\n"

                prompt = f"""
You are ABLEX AI, a friendly, helpful and responsible AI assistant.
Explain things clearly and accurately.
For school questions, use age-appropriate explanations.
If you are unsure about something, say so.

Previous conversation:
{history}

User question:
{question}
"""

                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt
                )

                answer = response.text or "I couldn't generate a response."
                st.markdown(answer)

                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )

            except Exception as e:
                st.error("Unable to connect to Gemini right now.")
                st.caption(str(e))
                st.info("Please check your API key, model access and internet connection.")

if st.sidebar.button("Clear chat"):
    st.session_state.messages = []
    st.rerun()

st.sidebar.title("About ABLEX AI")
st.sidebar.write("Version 1.0")
st.sidebar.write("Powered by Google Gemini.")

