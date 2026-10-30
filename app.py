
import streamlit as st

st.set_page_config(
    page_title="ABLEX AI",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 ABLEX AI")
st.subheader("Your Intelligent AI Assistant")

st.write("Welcome to ABLEX AI! Your AI journey starts here.")

question = st.text_input("What would you like help with?")

if st.button("Ask ABLEX AI"):
    if question.strip():
        st.info("Your question: " + question)
        st.write("AI connection will be added in our next development step.")
    else:
        st.warning("Please enter a question.")

st.sidebar.title("ABLEX AI")
st.sidebar.write("Version 1.0")
st.sidebar.write("Building the future with AI.")
