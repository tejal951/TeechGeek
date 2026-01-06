import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GROOQ_API_KEY")
if not api_key:
    st.error("GROOQ_API_KEY not found in .env file")
    st.stop()

client = Groq(api_key=api_key)

st.title("🤖 AI Chatbot (KRISHNA GPT)")

user_input = st.text_input("Ask me anything:")

if st.button("Send"):
    if user_input:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # ✅ UPDATED MODEL
            messages=[
                {"role": "user", "content": user_input}
            ]
        )
        st.markdown("**AI Reply:**")
        st.write(response.choices[0].message.content)
    else:
        st.warning("Please type a question")