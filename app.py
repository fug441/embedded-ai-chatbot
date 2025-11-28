import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Embedded AI TA Chatbot", page_icon="🤖")

st.title("Embedded AI & Robotics TA Chatbot 🤖")
st.write("Ask anything about Arduino, sensors, motors, or tiny AI models!")

# Load Gemini API key from Streamlit secrets
api_key = st.secrets.get("GEMINI_API_KEY", None)
if api_key is None:
    st.error("GEMINI_API_KEY is not set. Add it in Streamlit Cloud → Settings → Secrets.")
    st.stop()

genai.configure(api_key=api_key)

# Initialise Gemini model
model = genai.GenerativeModel("gemini-1.5-pro")

# Initialise chat history (server-side memory)
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[
        {
            "role": "user",
            "parts": ["You are a friendly teaching assistant for an Embedded AI & Robotics lab. Explain things simply for first-year data science students."]
        }
    ])

# Display previous messages
for msg in st.session_state.chat.history:
    role = msg["role"]
    text = msg["parts"][0]

    if role == "user":
        with st.chat_message("user"):
            st.markdown(text)
    else:
        with st.chat_message("assistant"):
            st.markdown(text)

# Chat input
user_input = st.chat_input("Type your question here…")

if user_input:
    # Show the user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Send message to Gemini
    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            response = st.session_state.chat.send_message(user_input)
            st.markdown(response.text)
