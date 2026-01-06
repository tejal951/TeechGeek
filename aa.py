import streamlit as st
import requests

# Replace this with the correct Ollama port after checking with `ollama list` or `ollama serve`
OLLAMA_URL = "http://localhost:11434/api/chat"


MODEL = "gemma:2b"

st.set_page_config(page_title="Ollama Chatbot", page_icon="🤖")
st.title("🤖 Ollama Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful AI assistant."}
    ]

# Display previous messages
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# Get user input
user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    payload = {
        "model": MODEL,
        "messages": st.session_state.messages,
        "stream": False
    }

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(OLLAMA_URL, json=payload, timeout=15)

                # Check if server responded
                if response.status_code == 200:
                    try:
                        reply = response.json()["message"]["content"]
                    except requests.exceptions.JSONDecodeError:
                        reply = "❌ Failed to decode JSON from Ollama."
                else:
                    reply = f"❌ Request failed with status code {response.status_code}:\n{response.text}"

            except requests.exceptions.ConnectionError:
                reply = (
                    f"❌ Could not connect to Ollama server at {OLLAMA_URL}.\n"
                    "Make sure Ollama is running and the port is correct."
                )
            except requests.exceptions.RequestException as e:
                reply = f"❌ Request failed:\n{e}"

            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
